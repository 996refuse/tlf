import tornado.web
import tornado.websocket
import tornado.ioloop
import json

import redis 
import pdb
import spider 
import msgpack 

REDIS_CONS = {} 

class RedisHandler(tornado.websocket.WebSocketHandler): 
    def check_origin(self, origin):
        return True 

    def on_message(self, message): 
        j = json.loads(message) 
        cmd = j.get("cmd")
        if not cmd:
            return {
                    "errno": 1,
                    "data": "args error"
                    } 
        res = None
        data = j.get("data")
        if cmd == "pop":
            res = self.pop_items(data)
        elif cmd == "push":
            res = self.push_items(data)
        elif cmd == "connect":
            res = self.connect_redis(data) 
        res["cmd"] = cmd
        self.write_message(json.dumps(res))


    def pop_items(self, data):
        pdb.set_trace()
        data = json.loads(data)
        for i in ("batch", "node", "type", "key"):
            if i not in data:
                return {
                        "errno": 1,
                        "data":  "args error: %s" % data
                        } 
        batch = data["batch"]
        node = data["node"]
        type = data["type"]
        key = data["key"]
        r = REDIS_CONS.get(node)
        if not r: 
            return {
                    "errno": 1,
                    "node": "%s not found" % node,
                    } 
        if type == "list":
            items = spider.list_pop_n(r, key, batch)
        elif type == "set":
            items = spider.set_pop_n(r, key, batch)
        else: 
            return {
                    "errno": 1,
                    "type": "%s is not allowed" % type,
                    } 
        b = []
        for item in items:
            b.append(msgpack.unpackb(item))
        return {
                "errno": 0,
                "data": json.dumps(b)
                } 
        

    def connect_redis(self, data):
        j = json.loads(data)
        if "node" not in j or  "db" not in j:
            return {
                    "errno": 1,
                    "data": "args error" % j
                } 
        con = redis.StrictRedis(**j["db"])
        spider.load_lua_scripts(con)
        REDIS_CONS[j["node"]] = con
        return {
                "errno": 0,
                "data":  "connected: %s"  % j
                } 


    def push_items(self, data):
        data = json.loads(data)
        result = data.get("result")
        dst = data.get("dst")
        multi_dst = data.get("multidst")
        if not data or (not rule and not multi_dst):
            return {
                    "errno": 1,
                    "data": "args error"
                    } 
        rule = {}
        if dst:
            rule['dst'] = json.loads(dst)
        if multidst:
            rule["multidst"] = json.loads(multi_dst) 
        spider.forward(json.loads(result), rule) 
        return {
                "errno": 0,
                "data": None
                }


application = tornado.web.Application([
    (r"/redis_proxy", RedisHandler), 
]) 



def run(): 
    application.listen(8866) 
    tornado.ioloop.IOLoop.instance().start() 

