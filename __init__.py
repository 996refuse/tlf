#-*-encoding=utf-8-*- 
import redis 
import MySQLdb 
import msgpack

import os 
import time 
import sqlite3 
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
import ctypes
import signal
import subprocess

import async_http
import simple_http

from lxml import etree 
from decimal import Decimal 

from spider import modules 
from spider import configs

from spider import llkv
from spider.urlcrc import get_urlcrc
from spider import filepack2


__all__ = ["modules"] 

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


sids = {}


"""
在redis上执行lua脚本
以最小化的成本批量操作
"""



def load_lua_scripts(node): 
    for x,v in scripts.items(): 
        sids[x] = node.script_load(v) 



"""
list_pop_n(redis, "mykey", 10)
"""
def list_pop_n(redis, key, n): 
    return redis.evalsha(sids["list_pop_n"], 2, key, n) 


"""
list_pop_n(n, redis, "mykey", "1", "2", "3", "4")
"""
def list_push_n(redis, key, *args):
    return redis.evalsha(sids["list_push_n"], len(args)+1,  key, *args)



def set_pop_n(redis, key, n):
    return redis.evalsha(sids["set_pop_n"], 2, key, n)


def set_push_n(redis, key, *args):
    return redis.evalsha(sids["set_push_n"], len(args)+1,  key, *args)


CONFIG = {}


def jsonp_json(content):
    a = content.find("(")
    b = content.rfind(")")
    if a < 0 or b < 0:
        return
    return json.loads(content[a+1:b])


def log_result(tp, result): 
    if tp =="hash":
        b = []
        for k,v in result.iteritems():
            b.append("%s: %s" % (k, v))
        log_with_time("\n".join(b)) 
    else:
        log_with_time("\n".join([repr(i) for i in result])) 


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
    if not tp:
        return
    qname = dst["name"] 
    if dst.get("log", True):
        log_result(tp, result)
    if dst.get("pack", True): 
        b = pack_result(tp, result)
    else:
        if tp == "hash":
            b = result
    if tp == "list":
        list_push_n(redis, qname, *b) 
    elif tp == "set":
        set_push_n(redis, qname, *b)
    elif tp == "hash": 
        redis.hmset(qname, dict(b))
    else:
        log_with_time("unknown dst type")
        return 


def forward_dst(result, rule): 
    for k,v in rule.get("multidst", {}).items():
        if k in result: 
            r = CONFIG["nodes"][v.get("node", "default")]
            forward_one(r, result[k], v) 
    if not "dst" in rule:
        return 
    dst = rule["dst"]
    r = CONFIG["nodes"][dst.get("node", "default")]
    forward_one(r, result,  dst) 


price_striped = set((u"¥", " ", "\t", "\n", "`"))


def fix_price(text): 
    ret = []
    for i in text:
        if i not in price_striped:
            ret.append(i)
    return "".join(ret)


sp_site = set((25, 1025, 2025, 3025, 31, 1031, 2031, 3031, 4031)) 


def format_price(result): 
    site_id = CONFIG["site_id"]
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
            log_with_time("price format error: %s" % i[1])
            continue
        if not isinstance(i[2], int):
            log_with_time("stock format error: %s" % i[2])
            continue
        stock = i[2]
        if price < 0:
            stock = -1
            price = -1
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
        return 
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
    l = path.split(".")
    m = l.pop(0)
    module = getattr(spider.modules, m)
    if not l: return module
    __import__("spider.modules.%s" % m)
    return getattr(module, l[0]) 



def batch_parser(task): 
    not200 = task["rule"]["get"].get("not200")
    if task["resp_header"]["status"] != 200 and not200 == "log":
        if not200 == "log": 
            log_with_time("not200: %s %s" % (task["resp_header"],
                task["url"]))
        elif not200 == "trace":
            pdb.set_trace() 
        return 
    try:
        result = task["to"](task, task["rule"].get("rule")) 
        if CONFIG.get("task_guard"):
            CONFIG["origin_node"].srem(CONFIG["origin"], task['origin'])
    except:
        traceback.print_exc()
        exit(1) 
    if not result:
        log_with_time("empty result: %s" % task["url"])
        return
    if result and (task["rule"].get("dst") or
            task["rule"].get("multidst")):
        log_with_time("result of %s" % task["url"])
        forward_dst(result, task["rule"]) 



def default_filter(x):
    return x



def async_config(rule): 
    args = rule["get"]["args"]
    for i in ("limit", "interval", "retry"):
        if i in args:
            async_http.config[i] = args[i]
    async_http.debug = args.get("debug") 
    default = ("url", "parser", "to", "origin",
            "method", "rule", "old_url", "payload")
    keys = set(args.get("keys", [])).union(set(default)) 
    if "pool" in args: 
        async_http.sconf.update(args["pool"]) 
    async_http.copy_keys = tuple(keys) 



def split_list(l, n):
    le = len(l)
    c = le / n
    if le % n:
        c += 1 
    ret = []
    for i in range(c):
        ret.append(l[i*n:(i+1)*n])
    return ret



def apply_group_filter(items, flt, model): 
    unpackb = msgpack.unpackb
    items = [unpackb(item) for item in items]
    tasks = [] 
    for i in flt(items): 
        i.update(model)
        tasks.append(i)
    return tasks



def apply_single_filter(items, flt, model): 
    tasks = [] 
    guard = CONFIG["task_guard"]
    unpackb = msgpack.unpackb
    for i in items: 
        unpacked = unpackb(i)
        t = flt(unpacked)
        if guard:
            t["origin"] = i
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
    qname = src["name"] 
    group = src.get("group") 
    randua = rule["get"].get("randua")
    node = CONFIG["nodes"][src.get("node", "default")] 
    if rule["src"].get("strict"):
        CONFIG["task_guard"] = True 
        CONFIG["origin_node"] = node
        CONFIG["origin"] = rule["src"]["origin"]
    else:
        CONFIG["task_guard"] = False
    if rule["get"].get("args"):
        async_config(rule) 
    unpack = msgpack.unpackb 
    tp = src["type"] 
    if "filter" in src:
        flt = load_func(src["filter"])
    else:
        flt = default_filter 
    while True: 
        if tp == "list":
            items = list_pop_n(node, qname, src.get("batch", 1)) 
        elif tp == "set":
            items = set_pop_n(node, qname, src.get("batch", 1))
        else:
            log_with_time("unknown src type") 
            exit(1) 
        if randua: 
            md = model_with_randua(rule) 
        else:
            md = model_simple(rule)
        if group:
            tasks = apply_group_filter(items, flt, md)
        else:
            tasks = apply_single_filter(items, flt, md) 
        if not tasks and wait_or_die(rule): 
            log_with_time("%s done" % rule["name"])
            break 
        if not tasks:
            log_with_time("sleeping")
            continue
        async_http.loop_until_done(tasks) 
        async_http.stats = [] 



def run_worker(rule): 
    rt = rule.get("type") 
    if rule.get("boot"):
        boot = load_func(rule["boot"])
        boot(CONFIG)
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
    elif rt == "generator":
        func = load_func(rule["generator"])
        if not rule.get("repeat", 0):
            ret = func()
            log_with_time("%s done" % rule["name"]) 
            exit(0) 
        while True: 
            forward_dst(func(), rule) 
            log_with_time("sleeping") 
            sleep_with_counter(rule.get("repeat")) 
    elif rt == "dp":
        run_dp(rule)
    elif rt == "guard":
        run_guard(rule)
    else:
        log_with_time("unknown worker type: %s" % rt)



def my_server_id():
    output = subprocess.check_output("ifconfig", shell=True)
    myid = re.compile("192.168.1.([0-9]{1,3})").findall(output)[0]
    return myid 



def connect_mysql(config): 
    if "mysql_con" in CONFIG:
        try:
            CONFIG["mysql_con"].close() 
        except Exception as e:
            log_with_time("close prev mysql con failed") 
    CONFIG["mysql_con"] = MySQLdb.connect(**config)
    CONFIG["mysql_cur"] = CONFIG["mysql_con"].cursor() 




def replace_log(name): 
    old_name = name+".old"
    os.rename(name, old_name) 
    replace_stdout(name) 
    try:
        cmd = "7z a %s.7z %s" % (old_name, old_name)
        print subprocess.check_output(cmd, shell=True)
        os.remove(old_name) 
    except OSError as e:
        print "7z: compress log failed: %s" % e 



def log_with_time(obj): 
    if not isinstance(obj, str): 
        obj = repr(obj) 
    if not debug: 
        #5行写磁盘,  减少压力 
        try:
            msg = u"%s: %s" % (time.ctime(), obj)
        except UnicodeDecodeError:
            msg = u"%s: %s" % (time.ctime(), repr(obj))
        CONFIG["line_buffer"].append(msg)
        CONFIG["line_cnt"] += 1
        if CONFIG["line_cnt"] > 4:
            print "\n".join(CONFIG["line_buffer"]) 
            CONFIG["line_cnt"] = 0 
            CONFIG["line_buffer"] = []
    else:
        print u"%s: %s" % (time.ctime(), obj)
    if "log_file" in CONFIG and CONFIG["log_file"].tell() > 536870912: 
        fobj = CONFIG["log_file"]
        name = fobj.name
        fobj.close()
        try:
            replace_log(name)
        except OSError as e:
            print "replace_log error: %s" % e 



def detach_worker(site, cat): 
    pid = os.fork()
    if not pid: 
        os.execvp("python", ["python",
            os.path.dirname(__file__), site, cat]) 
        #dont't invoke cleanup 
        os._exit(0)
    return pid 



def detach_and_set_log(CONFIG): 
    if not os.fork():
        os.setsid()
        p = os.fork()
        if not p:
            sys.stdin = open("/dev/null", "r")
            fobj = open(CONFIG["log_name"], "a+", buffering=0)
            sys.stdout = fobj
            sys.stderr = fobj
            CONFIG["log_file"] = fobj
        else:
            exit()
    else: 
        os.wait()
        exit() 



def update_llkv(site_id,  key, price, stock):
    if stock > 1:
        stock = 1
    if stock < 0:
        stock = 0
    if price > 0x7fffffffffffffffL:
        log_with_time("price out of range: %s" % price)
        return
    if price < 0:
        price = 0
    ll_key = (site_id << 48) | ctypes.c_uint(key).value
    CONFIG["llkv"].set(ll_key, price | (stock << 63)) 




INSERT_PRICE_SQL = 'insert into T_PriceStock (site_id, url_crc, update_date,  price, stock, update_time, server_id) values(%s, %s, "%s", %s, %s, "%s", %s) on duplicate key update price = %s, stock = %s, update_date="%s", update_time="%s", server_id=%s'




def update_mysql(site_id, key, price, stock): 
    now = datetime.datetime.strftime(datetime.datetime.now(),
            '%Y-%m-%d %H:%M:%S')
    date = now.split(' ')[0] 
    sql = INSERT_PRICE_SQL % (site_id, key, date, price, stock, now, CONFIG["myid"], price, stock, date, now, CONFIG["myid"])
    log_with_time(sql) 
    _safe_insert_sql(sql)
    update_llkv(site_id, key, price, stock)



def _safe_insert_sql(sql): 
    while True:
        try:
            CONFIG["mysql_cur"].execute(sql)
            break
        except Exception as e: 
            if len(e.args) > 1:
                msg = e.args[1]
            else:
                msg = ""
            if "gone away" in msg or "lost" in msg:
                wait_for_mysql()
            else: 
                log_with_time("bug, _safe_insert_sql: %s %s" % (e,  sql)) 
                return 



def _safe_commit(): 
    while True:
        try:
            CONFIG["mysql_con"].commit()
            break
        except Exception as e:
            if len(e.args) > 1:
                msg = e.args[1]
            else:
                msg = ""
            if "gone away" in msg or "lost" in msg:
                wait_for_mysql()
            else: 
                log_with_time("bug, _safe_commit: %s" % e)
                return 



def wait_for_mysql():
    while True: 
        log_with_time("bug: wait_for_mysql: reconnect mysql") 
        try:
            connect_mysql(CONFIG["client"]["mysql"]) 
            break
        except Exception as e:
            log_with_time("waiting mysql: %s" % e) 
            time.sleep(5) 


TT_INFO = re.compile("p>([\-0-9]+).*s>([0-9]+)") 



def format_style_group(main_url, urls): 
    site_id = CONFIG["site_id"] 
    main_crc = get_urlcrc(site_id, main_url)
    crcs = []
    for k in urls:
        crcs.append(str(get_urlcrc(site_id, k))) 
    return main_crc, ",".join(crcs)



def update_db(items): 
    llkv = CONFIG["llkv"] 
    prices = {}
    for i in items:
        prices[i[1]] = i[2:] + [i[0]]
    keys = []
    for site_id, crc, _, _ in items:
        unsigned_crc = ctypes.c_uint(int(crc)).value
        keys.append((int(site_id) << 48) | unsigned_crc) 
    d = llkv.multi_get(keys) 
    for key, value in d.items():
        k2 = ctypes.c_int(key & 0xffffffff).value
        if k2 not in prices:
            log_with_time("k2 not in prices")
            continue
        price, stock, site_id = prices[k2] 
        del prices[k2] 
        if not value:
            log_with_time("llkv empty key, %s" % key)
            update_mysql(site_id, k2, price, stock)
            continue 
        s = value >> 63
        p = value & 0x7fffffffffffffffL
        if p != price or s != stock:
            update_mysql(site_id, k2, price, stock) 
    for key, value in prices.items():
        price, stock, site_id = value 
        update_mysql(site_id, key, price, stock) 


commit_rule = {
            "name": "commit",
            "dst": {
                "node": "default",
                "name": "spider_result",
                "type": "list" 
                }
            }


def run_commit(): 
    import atexit
    atexit.register(flush_lines) 
    load_config()
    apply_config(commit_rule)
    import llkv
    client = CONFIG["client"]
    CONFIG["llkv"] = llkv.Connection(**client["llkv_list"])
    connect_mysql(client["mysql"]) 
    load_lua_scripts(CONFIG["nodes"].get("default")) 
    CONFIG["log_name"] = "/tmp/spider-commit.log" 
    replace_stdout(CONFIG["sites"]["commit"].get("log",
        "/tmp/spider-commit.log"))
    redis = CONFIG["nodes"]["default"] 
    unpack = msgpack.unpackb 
    while True: 
        b = []
        items = list_pop_n(redis, "spider_result",  1000)
        for i in items:
            item = msgpack.unpackb(i) 
            if len(item) != 4: 
                log_with_time("result format error %s" % item) 
                continue 
            b.append(item) 
        if not b: 
            log_with_time("sleeping")
            time.sleep(2)
            continue
        n = len(b) / 1000
        if len(b) % 1000:
            n += 1
        for i in range(n):
            items = b[i*1000: (i+1) * 1000]
            update_db(items) 
        _safe_commit() 


def dp_parser(task):
    status = task["resp_header"]["status"]
    if status != 200: 
        log_with_time("status: %s" % status) 
        return 
    if "crc" not in task:
        log_with_time("crc missing: %s" % task["url"])
        return 
    CONFIG["fpack"].add(task["url"], task["text"], crc=task["crc"]) 
    key = (CONFIG["site_id"] << 48) | ctypes.c_uint(task["crc"]).value
    CONFIG["lc"].set(key, 0)
    log_with_time(task["url"])



def dp_diff(lc, items): 
    site_id = CONFIG["site_id"]
    crcs = {}
    for item in items: 
        li = len(item)
        if li == 2:
            url, title = item 
            crc = get_urlcrc(site_id, url)
        elif li == 3:
            url, crc, title = item 
            crc = int(crc)
        else:
            log_with_time("unknown dp format") 
            continue
        key = ctypes.c_uint(crc).value | site_id << 48
        crcs[key] = (crc, url) 
    d = lc.multi_get(crcs.keys())
    ret = []
    for k,v in d.items():
        if v == None:
            ret.append(crcs[k])
    return ret



def get_dp_tasks(redis, qname): 
    b = [] 
    for i in list_pop_n(redis, qname,  1000): 
        b.append(msgpack.unpackb(i)) 
    if not b:
        return
    crcs = {} 
    diffset = dp_diff(CONFIG["lc"], b)
    tasks = [] 
    for crc, url in diffset:
        hdr = async_http.html_header.copy()
        hdr["User-Agent"] = async_http.random_useragent()
        task = { 
            "url": url, 
            "crc": int(crc),
            "header": hdr,
            "parser": dp_parser
            }
        tasks.append(task) 
    return tasks 



def dp_fetch_tasks(tasks):
    async_http.loop_until_done(tasks) 



def run_dp(rule): 
    client = CONFIG["client"]
    CONFIG["lc"] = llkv.Connection(**client["llkv_dp"])
    CONFIG["fpack"] = filepack2.FilePack(db = client["nodes"]["default"],
            limit = 1000, site_id=CONFIG["site_id"], datadir="/mnt/mfs")
    async_http.copy_keys = ("url", "parser", "header", "site_id", "crc") 
    node = CONFIG["nodes"].get("default") 
    load_lua_scripts(node)
    CONFIG["dp_redis"] = redis
    qname = rule["src"]["name"]
    if rule["get"].get("args"):
        async_config(rule) 
    while True: 
        tasks = get_dp_tasks(node, qname)
        if not tasks:
            time.sleep(5)
            CONFIG["fpack"].flush()
            log_with_time("sleeping")
            continue
        dp_fetch_tasks(tasks) 


dp_idx_rule = { 
        "name": "dp_idx",
        "dst": {
            "node": "default",
            "name": "dp_idx",
            "type": "list" 
            }
        } 


def run_dp_idx(): 
    load_config()
    apply_config(dp_idx_rule) 
    connect_mysql(CONFIG["client"]["dp_idx"])
    r = CONFIG["nodes"].get("default")
    wait = dp_idx_rule.get("wait", 2) 
    replace_stdout(CONFIG["sites"]["idx"].get("log",
        "/tmp/spider-idx.log"))
    while True:
        l = r.lpop("dp_idx") 
        if not l:
            log_with_time("sleeping")
            time.sleep(wait) 
            continue
        sqls = msgpack.unpackb(l) 
        for sql in sqls:
            log_with_time(sql)
            _safe_insert_sql(sql)
        _safe_commit() 



def run_rt(rule):
    pass


def run_guard(rule):
    tp = rule["src"]["type"]
    qname = rule["src"]["name"] 
    node = rule["dst"]["node"]
    dname = rule["dst"]["name"]
    wait = rule["wait"]
    assert tp == "set"
    while True:
        members = node.smembers(name)
        if not membser:
            log_with_time("sleeping") 
            time.sleep(wait)
            continue
        list_push_n(dname, members)
        while True:
            dlen = node.llen(dname)
            if dlen == 0:
                log_with_time("tasks done")
                break
            else:
                log_with_time("waiting: %s" % dlen) 
                time.sleep(wait) 



def flush_lines(): 
    if "conf" in globals() and len(CONFIG["line_buffer"]):
        print "\n".join(CONFIG["line_buffer"])



def load_site(site): 
    s = CONFIG["sites"].get(site)
    if not s:
        print "bad site: %s" % site
        return 
    if "." in site:
        site = site.split('.')[0]
    try:
        __import__("spider.modules.%s" % site)
    except IndexError:
        print "site %s not exists" % site 
        return 
    m = getattr(modules, site)
    return m 

debug = False 

def run_test_cases(cases, rule): 
    parser = load_func(rule["get"]["parser"]) 
    for case in cases: 
        url = case["url"]
        func = load_func(case["check"])
        method = case.get("method", "get")
        h,c = getattr(simple_http, method)(url,
            query = case.get("query"),
            payload = case.get("payload"))
        if h["status"] != 200:
            print "request %s failed" % url
            exit(1) 
        if not "src" in rule:
            func(parser(url, c, rule["from"][url])) 
        ctx = {"url": url, "text": c}
        ctx.update(case) 
        func(parser(ctx, rule.get("rule"))) 


def run_module_test(site, cat): 
    global debug
    debug = True 
    load_config() 
    m = load_site(site) 
    if not m: 
        return
    rule = getattr(m, "rule") 
    target = get_cat_from_rule(rule, cat) 
    if not target:
        print "cat %s not exists" % cat
        return 
    apply_config(target) 
    test = target.get("test")
    if not test:
        print "I don't known how to test"
        exit(1) 
    run_test_cases(test, target)


blt_worker = {
        "commit": run_commit,
        "idx": run_dp_idx,
        }



def replace_stdout(log): 
    if not debug: 
        sys.stdin = open("/dev/null", "r")
        fobj = open(log, "a+", buffering=0)
        sys.stdout = fobj
        sys.stderr = fobj
        CONFIG["log_file"] = fobj 



def get_cat_from_rule(rule, cat): 
    target = 0
    for c in rule:
        if c["name"] == cat:
            return c



def use_config(role): 
    if not role:
        try:
            role = my_server_id() 
        except:
            role = "local"
    import importlib 
    try:
        config = importlib.import_module("spider.configs.%s" % role) 
    except ImportError as e:
        print "import error: %s" % e
        exit(1) 
    CONFIG["client"] =  config.CLIENT
    CONFIG["sites"] = config.SITES

role = "" 

def load_config(): 
    CONFIG["myid"] = 170 
    CONFIG["line_cnt"] = 0
    CONFIG["line_buffer"] = []
    use_config(role)



def apply_config(rule): 
    redis_nodes = {} 
    nodes = CONFIG["client"]["nodes"] 
    if not rule.get('dst') and not rule.get("multidst"):
        log_with_time("rule format error, no dst")
        exit(1); 
    for v in rule.get("multidst", {}).values():
        node = v.get("node", "default")
        redis_nodes[node] = redis.StrictRedis(**nodes[node])
    if "dst" in rule: 
        node = rule["dst"].get("node", "default")
        redis_nodes[node] = redis.StrictRedis(**nodes[node]) 
    CONFIG["nodes"] = redis_nodes 


def run_cat(site, cat): 
    import atexit
    atexit.register(flush_lines) 
    load_config() 
    if site in blt_worker: 
        blt_worker[site]()
        exit(0)
    m = load_site(site)
    if not m: 
        return
    #查找相应的worker
    rule = getattr(m, "rule") 
    target = get_cat_from_rule(rule, cat)
    if not target:
        print "cat %s not exists" % cat
        return 
    apply_config(target) 
    site_id = CONFIG["sites"][site]["site_id"]
    CONFIG["site_id"] = site_id
    CONFIG["site"] = site 
    load_lua_scripts(CONFIG["nodes"].get("default")) 
    if not debug:
        replace_stdout(CONFIG["sites"][site].get("log",
            "/tmp/spider-%s-%s.log" % (site, cat)))
    #无分站 
    subsites = getattr(m, "sites", {})
    if not subsites:
        run_worker(target)
        exit(0)
    #顺序执行分站 
    if subsites.get("source") == "cats" and cat == "cats":
        repeat = target.get("repeat")
        target["old_dst"] = target["dst"].copy()
        if not repeat:
            run_subsite(subsites, target)
            exit(1) 
        while True:
            run_subsite(subsites, target)
            sleep_with_counter(repeat)
    #修改分站队列名 
    if site_id in subsites.get("sites", {}): 
        name = subsites["sites"][site_id] 
        if target.get("dst") and target["dst"].get("subsite"):
            target["dst"]["name"] += "_" + name
        for v in target.get("multidst", {}).values():
            if v.get("subsite"):
                v["name"] += "_" + name 
        target["src"]["name"] += "_" + name 
    run_worker(target) 



def run_subsite(subsites, rule): 
    for site_id, name in subsites["sites"].items(): 
        CONFIG["site_id"] = site_id
        CONFIG["site"] = name 
        new_name = rule["old_dst"]["name"] + "_" + name
        rule["dst"]["name"] = new_name
        repeat = rule.get("repeat", 60)
        rule["repeat"] = 0
        log_with_time("run site: %s" % name)
        run_worker(rule) 
        rule["repeat"] = repeat
        sleep_with_counter(repeat) 


def start_all_sites(workers): 
    for i,v in CONFIG["sites"].items(): 
        if v.get("ignore"):
            log_with_time("skip: %s" % i)
            continue
        if i not in blt_worker and "." not in i:
            try:
                __import__("spider.modules.%s" % i)
            except ImportError:
                log_with_time("site %s not exists" % i) 
                return 
        for j in v.get("workers"): 
            pid = detach_worker(i, j) 
            workers[pid] = (i, j) 



def kill_workers(): 
    if not "workers" in CONFIG:
        return
    import signal
    for i,v in CONFIG["workers"].items():
        try:
            os.kill(i, signal.SIGKILL)
            del CONFIG["workers"][i]
            log_with_time("%s,  %s, %s killed" % (i, v[0], v[1]))
        except OSError:
            log_with_time("kill %s failed" % i) 



def run(): 
    load_config() 
    CONFIG["line_cnt"] = 0
    CONFIG["line_buffer"] = [] 
    CONFIG["log_name"] = "/tmp/spider-all.log" 
    detach_and_set_log(CONFIG)
    workers = {}
    CONFIG["workers"] = workers 
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
    for pid,v in CONFIG["workers"].items():
        site,worker = v 
        if s and w and site == s and worker == w: 
            to.append((pid, site,worker))  
    for pid, site, worker in to:
        try:
            os.kill(pid, signal.SIGKILL) 
            del CONFIG["workers"][pid]
            log_with_time("%s,  %s, %s killed" % (pid, site, worker))
        except OSError:
            log_with_time("kill %s failed" % pid) 


def command_start(**kwargs): 
    site = kwargs.get("site")
    worker = kwargs.get("worker") 
    if not CONFIG["sites"].get(site):
        log_with_time("site not allowed")
        return
    if worker not in CONFIG["sites"][site]["workers"]:
        log_with_time("worker not allowed")
        return 
    pid = detach_worker(site, worker) 
    CONFIG["workers"][pid] = (site, worker) 



def command_startall(**kwargs): 
    start_all_sites(CONFIG["workers"]) 



def command_statall(**kwargs):
    pass 



def command_stat(**kwargs): 
    pass 



def command_getall(**kwargs):
    workers = []
    for pid, value in CONFIG["workers"].items():
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



def udp_event(sock, pollobj): 
    for fd, event in pollobj.poll(1):
        if event & select.EPOLLERR:
            log_with_time("epollerr, master die")  
            exit(1)
        if event & select.EPOLLIN:
            try:
                handle_control_msg(sock) 
            except (KeyError, ValueError, OSError) as e:
                log_with_time("udp: %s" % e) 



def run_master(workers):
    ep = select.epoll()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 9966)) 
    ep.register(s.fileno(), select.EPOLLIN|select.EPOLLERR) 
    while True: 
        udp_event(s, ep)
        try:
            pid, status, res = os.wait3(os.WNOHANG) 
        except OSError:
            log_with_time("no worker running")
            continue
        if not pid: 
            print_workers(workers) 
            continue 
        if pid not in workers:
            log_with_time("pid: %s not in workers" % pid)
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
