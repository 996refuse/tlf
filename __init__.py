#-*-encoding=utf-8-*- 
import redis
import os 
import time
import msgpack
import sqlite3 
import MySQLdb
import pyrant
import re
import sys
import traceback
import datetime
import hashlib
import mmap 
import struct
import socket
import select
import json
import pdb
import signal

import async_http
import simple_http

from config import CLIENT
from config import SITES
from lxml import etree 
from spider import modules
from spider import config 
from decimal import Decimal
from spider.urlcrc import get_urlcrc


__all__ = ["modules"]


record_exists = pyrant.exceptions.RecordExists
host_not_found = pyrant.exceptions.HostNotFound
connection_error = redis.exceptions.ConnectionError 
response_error = redis.exceptions.ResponseError


lua_list_pop_n = """
local key = KEYS[1]
local num = tonumber(KEYS[2]) 
local i = 1 
local a = {}
while i <= num do
    local k = redis.pcall("lpop", key) 
    if not k then
        break
    end
    a[i] = k
    i = i + 1 
end
return a
""" 


lua_list_push_n  = """ 
local key = KEYS[1] 
local i = 1 
while 1 do
    local v = KEYS[1+i]
    if not v then
        break
    end
    redis.pcall("lpush", key,  v)
    i = i + 1 
end
return nil
""" 



lua_set_push_n = """
local key = KEYS[1] 
local i = 1 
while 1 do
    local v = KEYS[1+i]
    if not v then
        break
    end
    redis.pcall("sadd", key,  v)
    i = i + 1 
end
return nil
"""



lua_set_pop_n = """
local key = KEYS[1]
local num = tonumber(KEYS[2]) 
local i = 1 
local a = {}
while i <= num do
    local k = redis.pcall("spop", key) 
    if not k then
        break
    end
    a[i] = k
    i = i + 1 
end
return a 
""" 


scripts = {
        "list_pop_n": lua_list_pop_n,
        "list_push_n": lua_list_push_n,
        "set_pop_n": lua_set_pop_n,
        "set_push_n": lua_set_push_n
        }



"""
在redis上执行lua脚本
以最小化的成本批量操作
"""


def load_lua_scripts(): 
    redis = conf["nodes"]["default"]
    #redis.script_flush()
    for x,v in scripts.items(): 
        scripts[x] = redis.script_load(v) 



"""
list_pop_n(redis, "mykey", 10)
"""
def list_pop_n(redis, key, n): 
    return redis.evalsha(scripts["list_pop_n"], 2, key, n) 



"""
list_pop_n(n, redis, "mykey", "1", "2", "3", "4")
"""
def list_push_n(redis, key, *args):
    return redis.evalsha(scripts["list_push_n"], len(args)+1,  key, *args)



def set_pop_n(redis, key, n):
    return redis.evalsha(scripts["set_pop_n"], 2, key, n)


def set_push_n(redis, key, *args):
    return redis.evalsha(scripts["set_push_n"], len(args)+1,  key, *args)



def jsonp_json(content):
    a = content.find("(")
    b = content.rfind(")")
    if a < 0 or b < 0:
        return
    return json.loads(content[a+1:b])



def log_result(tp, result): 
    if tp =="hash":
        for i in result.iteritems():
            log_with_time(i)
    else:
        for i in result:
            log_with_time(i)


def pack_result(tp, result): 
    b = []
    pack = msgpack.packb 
    if tp == "hash":
        for k,v in result.iteritems(): 
            b.append((k, pack(v))) 
    else:
        for r in result: 
            b.append(pack(r)) 
    return b


def forward_one(redis, result, dst): 
    b = []
    if not result: 
        return
    tp = dst["type"] 
    if dst.get("log", True):
        log_result(tp, result)
    if dst.get("pack", True): 
        b = pack_result(tp, result)
    else:
        if tp == "hash":
            b = result
    if tp == "list":
        list_push_n(redis, dst["name"], *b) 
    elif tp == "set":
        set_push_n(redis, dst["name"], *b)
    elif tp == "hash": 
        redis.hmset(dst["name"], dict(b))
    else:
        log_with_time("unknown dst type")
        return 


def forward_dst(result, rule): 
    for k,v in rule.get("multidst", {}).items():
        if k in result: 
            r = conf["nodes"][v.get("node", "default")]
            forward_one(r, result[k], v) 
    if not "dst" in rule:
        return
    dst = rule["dst"]
    r = conf["nodes"][dst.get("node", "default")]
    forward_one(r, result,  dst) 



sp_site = set((25, 1025, 2025, 3025, 31, 1031, 2031, 3031, 4031)) 


def format_price(result): 
    site_id = conf["site_id"]
    ret = [] 
    for i in result: 
        if site_id in sp_site:
            urlcrc = int(i[0])
        else:
            urlcrc = get_urlcrc(site_id, i[0]) 
        if not urlcrc:
            log_with_time("format_price, bug urlcrc, %s, %s" % (site_id, i))
            continue 
        try:
            price = int(Decimal(i[1]) * 100)
        except:
            log_with_time("price format error: %s" % i)
            continue
        if not isinstance(i[2], int):
            log_with_time("stock format error: %s" % i)
            continue
        stock = i[2]
        if price < 0:
            stock = -1
        ret.append((site_id, urlcrc, price, stock))
    return ret 


query_methods = set(("get", "head", "delete", "trace", "option"))
upload_methods = set(("post", "delete")) 


def run_single(rule): 
    gt = rule["get"]
    do = getattr(simple_http, gt["method"])
    parser = load_func(gt["parser"])
    fromlist = rule["from"]
    for l in fromlist:
        if gt["type"] == "simple":
            hdr = simple_http.default_header.copy() 
        elif gt["type"] == "ajax": 
            hdr = simple_http.json_header.copy()
        else:
            log_with_time("unknown type: %s" % gt["type"])
            continue
        if gt["method"] in query_methods:
            h, c = do(l, query = gt.get("query")) 
        elif gt["method"] in upload_methods:
            h, c= do(l, payload = gt.get("payload"))
        else:
            log_with_time("unknown method: %s" % gt["method"])
            continue 
        if h["status"] == 200: 
            result = parser(l, c, fromlist[l]) 
            forward_dst(result, rule) 
        else:
            log_with_time("get %s failed" % l) 



def run_single_repeat(rule):
    repeat = rule.get("repeat", 0)
    if not repeat:
        run_single(rule)
        log_with_time("%s done" % rule["name"])
        exit(0)
    while True:
        run_single(rule)
        log_with_time("sleeping") 
        sleep_with_counter(repeat) 
    


def sleep_with_counter(n):
    for i in range(1, n+1):
        log_with_time("sleeping, cnt, %s" % i)
        time.sleep(1)




def load_func(path):
    import spider.modules
    m, r = path.split(".")
    __import__("spider.modules.%s" % m)
    module = getattr(spider.modules, m)
    return getattr(module, r) 



def batch_parser(task): 
    not200 = task["rule"]["get"].get("not200")
    if task["resp_header"]["status"] != 200 and not200 == "log":
        log_with_time("not200: %s %s" % (task["resp_header"], task["url"]))
        return 
    result = task["to"](task, task["rule"].get("rule"))
    if result and (task["rule"].get("dst") or task["rule"].get("multidst")):
        forward_dst(result, task["rule"]) 



def default_filter(x):
    return x




def async_config(rule): 
    args = rule["get"]["args"]
    for i in ("limit", "interval", "retry"):
        if i in args:
            async_http.config[i] = args[i]
    async_http.debug = args.get("debug") 
    default = ("url", "parser", "to", "method", "rule", "old_url", "payload")
    async_http.copy_keys = tuple(set(args.get("keys", [])).union(set(default))) 


def split_list(l, n):
    le = len(l)
    c = le / n
    if le % n:
        c += 1 
    ret = []
    for i in range(c):
        ret.append(l[i*n:(i+1)*n])
    return ret


def apply_group_task_filter(items, flt, model):
    tasks = [] 
    for i in flt(items): 
        i.update(model)
        tasks.append(i)
    return tasks


def apply_single_task_filter(items, flt, model): 
    tasks = []
    for i in items: 
        t = flt(i)
        t.update(model.copy())
        tasks.append(t)
    return tasks



def model_with_randua(rule): 
    header = async_http.html_header.copy()
    header["User-Agent"] = async_http.random_useragent() 
    return {
            "method": rule["get"]["method"],
            "to": load_func(rule["get"]["parser"]),
            "parser": batch_parser,
            "rule": rule,
            "header": header 
            } 



def model_simple(rule):
    return {
            "method": rule["get"]["method"],
            "to": load_func(rule["get"]["parser"]),
            "parser": batch_parser,
            "rule": rule,
            "header": async_http.default_header.copy()
            } 



def wait_or_die(rule):
    wait = rule.get("wait")
    if not wait:
        return True
    if wait:
        log_with_time("sleeping") 
        time.sleep(wait) 
    return False



def run_batch(rule): 
    src = rule["src"]  
    node = src["name"] 
    if "filter" in src:
        flt = load_func(src["filter"])
    else:
        flt = default_filter 
    group = src.get("group") 
    randua = rule["get"].get("randua")
    redis = conf["nodes"][src.get("node", "default")] 
    if rule["get"].get("args"):
        async_config(rule) 
    unpack = msgpack.unpackb 
    tp = src["type"] 
    while True: 
        if tp == "list":
            items = list_pop_n(redis, node, src.get("batch", 1)) 
        elif tp == "set":
            items = set_pop_n(redis, node, src.get("batch", 1))
        else:
            log_with_time("unknown src type") 
            exit(1) 
        b = [unpack(x) for x in items] 
        if randua: 
            md = model_with_randua(rule) 
        else:
            md = model_simple(rule)
        if group:
            tasks = apply_group_task_filter(b, flt, md)
        else:
            tasks = apply_single_task_filter(b, flt, md) 
        if not tasks and wait_or_die(rule): 
            log_with_time("%s done" % rule["name"])
            break 
        async_http.loop_until_done(tasks) 



def run_worker(rule): 
    rt = rule.get("type")
    if rt == "fetch":
        if not rule.get("src"):    
            gt = rule["get"] 
            run_single_repeat(rule) 
        else: 
            run_batch(rule) 
    elif rt == "food": 
        if not rule.get("repeat", 0): 
            forward_dst(rule["food"], rule) 
            log_with_time("%s done" % rule["name"])
            exit(0) 
        while True:
            forward_dst(rule["food"], rule) 
            log_with_time("sleeping") 
            sleep_with_counter(rule.get("repeat")) 
    else:
        log_with_time("unknown rule type: %s" % rt)



def my_server_id():
    output = subprocess.check_output("ifconfig", shell=True)
    myid = re.compile("192.168.1.([0-9]{1,3})").findall(output)[0]
    return myid



def connect_mysql(config): 
    if "mysql_con" in conf:
        try:
            conf["mysql_con"].close() 
        except Exception as e:
            log_with_time("close prev mysql con failed") 
    conf["mysql_con"] = MySQLdb.connect(**config)
    conf["mysql_cur"] = conf["mysql_con"].cursor() 



def connect_tt(config):
    return pyrant.Tyrant(**config)



def load_conf(rule): 
    #变量环境,  避免污染全局,  又不用创建一个管理类
    globals()["conf"] = {} 
    conf["commit_delay"] = 0 
    conf["myid"] = 170 
    conf["line_cnt"] = 0
    conf["line_buffer"] = []
    nodes = CLIENT["nodes"]
    redis_nodes = {} 
    if not rule.get('dst') and not rule.get("multidst"):
        log_with_time("rule format error, no dst")
        exit(1); 
    for v in rule.get("multidst", {}).values():
        node = v.get("node", "default")
        redis_nodes[node] = redis.StrictRedis(**nodes[node])
    if "dst" in rule: 
        node = rule["dst"].get("node", "default")
        redis_nodes[node] = redis.StrictRedis(**nodes[node]) 
    conf["nodes"] = redis_nodes



def load_dbs(): 
    load_conf({
            "name": "commit",
            "dst": {
                "node": "default",
                "name": "spider_result",
                "type": "list" 
                }
            })
    connect_mysql(CLIENT["mysql"])
    conf["tt"] = connect_tt(CLIENT["tt"]) 



def replace_log(fobj): 
    name = fobj.name
    fobj.close()
    old_name = name+".old"
    os.rename(name, old_name) 
    new_fobj = open(name, "a+", buffering=0)
    sys.stdout = new_fobj
    sys.stdout = new_fobj
    if os.fork():
        os.execvp("tar", ["tar",
            "-Pcjf", old_name+".tar.bz2", old_name, "--remove-files"]) 
        exit(0)        
    conf["log_rotate"] = True 




def log_with_time(obj): 
    conf["line_cnt"] += 1
    #5行写磁盘,  减少压力
    conf["line_buffer"].append(u"%s: %s" % (time.ctime(), repr(obj)))
    if conf["line_cnt"] > 4:
        print "\n".join(conf["line_buffer"]) 
        conf["line_cnt"] = 0 
        conf["line_buffer"] = []
    if "log_file" in conf and conf["log_file"].tell() > 536870912: 
        #500M日志rotate
        try:
            replace_log(conf["log_file"])
            conf["log_rotate"] = True
        except OSError as e:
            print e 



def detach_worker(site, cat): 
    pid = os.fork()
    if not pid: 
        os.execvp("python", ["python",
            os.path.dirname(__file__), site, cat]) 
        #dont't invoke cleanup 
        os._exit(0)
    return pid 



def detach_and_set_log(conf): 
    if not os.fork():
        os.setsid()
        p = os.fork()
        if not p:
            sys.stdin = open("/dev/null", "r")
            fobj = open(conf["log_name"], "a+", buffering=0)
            sys.stdout = fobj
            sys.stderr = fobj
            conf["log_file"] = fobj
        else:
            exit()
    else: 
        os.wait()
        exit() 


INSERT_PRICE_SQL = 'insert into T_PriceStock (site_id, url_crc, update_date,  price, stock, update_time, server_id) values(%s, %s, "%s", %s, %s, "%s", %s) on duplicate key update price = %s, stock = %s, update_date="%s", update_time="%s", server_id=%s'


def update_mysql(site_id, key, price, stock): 
    now = datetime.datetime.strftime(datetime.datetime.now(),
            '%Y-%m-%d %H:%M:%S')
    date = now.split(' ')[0] 
    sql = INSERT_PRICE_SQL % (site_id, key, date, price, stock, now, conf["myid"], price, stock, date, now, conf["myid"])
    log_with_time(sql)
    try: 
        conf["mysql_cur"].execute(sql) 
    except Exception as e: 
        if len(e.args) <= 1: 
            log_with_time("bug, udpate_mysql: %s %s" % (e,  sql)) 
            return
        msg = e.args[1] 
        if ("gone away" in msg or "lost" in msg): 
            wait_for_mysql() 



def wait_for_mysql():
    while True: 
        log_with_time("bug: udpate_mysql: reconnect mysql") 
        try:
            connect_mysql(CLIENT["mysql"]) 
            break
        except:
            log_with_time("waiting mysql")
            time.sleep(5) 




TT_INFO = re.compile("p>([\-0-9]+).*s>([0-9]+)") 



def format_style_group(main_url, urls): 
    site_id = conf["site_id"] 
    main_crc = get_urlcrc(site_id, main_url)
    crcs = ",".join([str(get_urlcrc(site_id, k)) for k in urls]) 
    return main_crc, crcs 



def update_db(items): 
    try:
        ret = conf["tt"].multi_get(["%s-%s" % (item[1], item[0]) for item in items])
    except (record_exists, host_not_found) as e: 
        log_with_time("bug: ttserver: %s" % e)
        return 
    prices = {}
    for i in items:
        prices[i[1]] = i[2:] + (i[0], ) 
    for item in ret:
        key, value = item
        x = key.rfind("-")
        k2 = int(key[:x])
        if k2 not in prices: 
            continue
        price, stock, site_id = prices[k2]
        del prices[k2]
        try:
            p, s = TT_INFO.findall(value)[0] 
            if int(p) != price or int(s) != stock:
                update_mysql(site_id, k2, price, stock)
        except (ValueError, IndexError):
            update_mysql(site_id, k2, price, stock)
    for key, value in prices.items():
        price, stock, site_id = value 
        update_mysql(site_id, key, price, stock) 



def run_commit(): 
    load_dbs()
    load_lua_scripts() 
    conf["log_name"] = "/tmp/spider-commit.log" 
    conf["log_rotate"] = False
    detach_and_set_log(conf)
    redis = conf["nodes"]["default"] 
    unpack = msgpack.unpackb 
    while True: 
        b = []
        for i in list_pop_n(redis, "spider_result",  10000):
            item = msgpack.unpackb(i) 
            if len(item) != 4: 
                log_with_time("result format error %s" % item) 
                continue 
            #site_id, key, price, stock 
            b.append(item) 
        if not b: 
            if conf.get("log_rotate"):
                res = os.wait3(os.WNOHANG) 
                log_with_time("rotate log done")
                conf["log_rotate"] = False
            log_with_time("sleeping")
            time.sleep(2)
            continue
        n = len(b) / 1000
        if len(b) % 1000:
            n += 1
        for i in range(n):
            items = b[i*1000: (i+1) * 1000]
            update_db(items) 
        try:
            conf["mysql_con"].commit() 
        except Exception as e: 
            log_with_time("error, mysql commit: %s" % e) 



debug = False


def flush_lines(): 
    if "conf" in globals():
        print "\n".join(conf["line_buffer"])



def run_cat(site, cat): 
    import atexit
    atexit.register(flush_lines)
    s = SITES.get(site)
    if not s:
        print "bad site: %s" % site
        return 
    try:
        __import__("spider.modules.%s" % site)
    except IndexError:
        print "site %s not exists" % site 
        return
    m = getattr(modules, site)
    rule = getattr(m, "rule")
    ok = 0
    for c in rule:
        if c["name"] == cat:
            ok = c 
            break
    if not ok:
        print "cat %s not exists" % cat
        return 
    load_conf(ok)
    conf["site_id"] = s["site_id"] 
    load_lua_scripts() 
    if not debug:
        log = s.get("log", "/tmp/spider-%s-%s.log" % (site, cat))
        sys.stdin = open("/dev/null", "r")
        fobj = open(log, "a+", buffering=0)
        sys.stdout = fobj
        sys.stderr = fobj
        conf["log_obj"] = fobj
    run_worker(ok) 



def start_all_sites(workers): 
    for i,v in SITES.items(): 
        if v.get("ignore"):
            log_with_time("skip: %s" % i)
            continue
        try:
            __import__("spider.modules.%s" % i)
        except IndexError:
            log_with_time("site %s not exists" % i) 
            return 
        for j in v.get("workers"): 
            pid = detach_worker(i, j)
            workers[pid] = (i, j) 



def kill_workers(): 
    if not "workers" in conf:
        return
    import signal
    for i,v in conf["workers"].items():
        try:
            os.kill(i, signal.SIGTERM)
            del conf["workers"][i]
            log_with_time("%s,  %s, %s killed" % (i, v[0], v[1]))
        except OSError:
            log_with_time("kill %s failed" % i) 


def run(): 
    globals()["conf"] = {}
    conf["line_cnt"] = 0
    conf["line_buffer"] = [] 
    conf["log_rotate"] = False
    conf["log_name"] = "/tmp/spider-all.log" 
    detach_and_set_log(conf)
    workers = {}
    conf["workers"] = workers 
    import atexit 
    atexit.register(kill_workers) 
    start_all_sites(workers)
    run_master(workers) 



def print_workers(workers): 
    for i,v in workers.items():
        log_with_time("running, site: %s worker: %s pid: %s" % (v[0], v[1], i)) 



def command_stopall(**kwargs): 
    kill_workers()
        


def command_stop(**kwargs): 
    s = kwargs.get("site")
    w = kwargs.get("worker")
    to = []
    for pid,v in conf["workers"].items():
        site,worker = v 
        if s and w and site == s and worker == w: 
            to.append((pid, site,worker))  
        elif s and site == s:
            to.append((pid, site, worker))
        elif w and worker == w:
            to.append((pid, site, worker))
    for pid, site, worker in to:
        try:
            os.kill(pid, signal.SIGTERM) 
            del conf["workers"][pid]
            log_with_time("%s,  %s, %s killed" % (pid, site, worker))
        except OSError:
            log_with_time("kill %s failed" % pid) 


def command_start(**kwargs): 
    site = kwargs.get("site")
    worker = kwargs.get("worker")
    pid = detach_worker(site, worker) 
    conf["workers"][pid] = (site, worker) 



def command_startall(**kwargs): 
    start_all_sites(conf["workers"]) 



def command_statall(**kwargs):
    pass 



def command_stat(**kwargs): 
    pass 



def command_report(**kwargs):
    pass



def command_getall(**kwargs):
    workers = []
    for pid, value in conf["workers"]:
        workers.append({
            "pid": pid,
            "site": value[0],
            "worker": value[1]
                })
    return {
            "status": True,
            "workers": workers
            }


master_comamds = {
        "stopall": command_stopall,
        "startall": command_startall,
        "stop": command_stop, 
        "start": command_start,
        "statall": command_statall,
        "stat": command_stat, 
        "report": command_report,
        "getall": command_getall,
        } 



def die_msg(sk, addr, msg):
    sk.sendto(
            json.dumps({
                "status": False,
                "msg": msg
            }), 
            addr) 


def handle_control_msg(sk): 
    data, addr = sk.recvfrom(4096)
    try:
        control = json.loads(data)
    except ValueError:    
        log_with_time("illegal packet: %s" % data)
        return
    if not "id" in control or not "cmd" in control:
        log_with_time("packet format error: %s" % data)
        return 
    cmd = control.get("cmd")
    if not cmd in master_comamds:
        die_msg(sk, addr, "unknown command")
        return 
    fn = master_comamds[cmd]
    try:
        d = fn(**control)
    except ValueError as e:
        die_msg(sk, addr, "command failed: %s" % e)
        return 
    if not d:
        d = {}
        d["status"] = True
    d["id"] = control.get("id") 
    d["cmd"] = cmd
    sk.sendto(json.dumps(d), addr) 



def run_master(workers): 
    ep = select.epoll()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 9966)) 
    ep.register(s.fileno(), select.EPOLLIN|select.EPOLLERR) 
    while True: 
        for fd, event in ep.poll(1):
            if event & select.EPOLLERR:
                log_with_time("epollerr, master die")  
                exit(1)
            if event & select.EPOLLIN:
                handle_control_msg(s) 
        try:
            pid, status, res = os.wait3(os.WNOHANG) 
        except OSError:
            log_with_time("no working running")
            continue
        if not pid: 
            print_workers(workers) 
            continue 
        if pid not in workers:
            continue
        site, worker = workers[pid] 
        sig = status & 0xf
        status = status >> 8 
        if not sig and status:
            log_with_time("%s %s die with exception: %s" % (site, worker, status)) 
        del workers[pid] 
        log_with_time("reloading %s %s" % (site, worker))
        pid = detach_worker(site, worker)
        workers[pid] = (site, worker) 
