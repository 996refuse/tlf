#-*-encoding=utf-8-*- 
#db
import redis 
import MySQLdb 
import msgpack

#utils
import time 
import sqlite3 
import re 
import traceback
import datetime 
import subprocess 
import hashlib
import json
import zlib

#os libraries
import sys
import mmap 
import struct
import socket
import select
import os 
import io 
import pdb
import ctypes
import signal


from importlib import import_module
from lxml import etree 
from decimal import Decimal 

#my package
from spider import async_http
from spider import simple_http 

from spider import modules 
from spider import configs

from spider import llkv
from spider.urlcrc import get_urlcrc
from spider import filepack2

__all__ = ["test", "async_http", "simple_http", "llkv", "filepack2", "modules"] 

SPIDER_DIR = os.path.dirname(__file__)

CONNECTION_ERROR = redis.exceptions.ConnectionError 
RESPONSE_ERROR = redis.exceptions.ResponseError 

sys.path.append("/".join(os.path.dirname(__file__).split("/")[:-1])) 

LUA_LIST_POP_N = """
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


LUA_LIST_PUSH_N  = """ 
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



LUA_SET_PUSH_N = """
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



LUA_SET_POP_N = """
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



SCRIPTS = {
        "list_pop_n": LUA_LIST_POP_N,
        "list_push_n": LUA_LIST_PUSH_N,
        "set_pop_n": LUA_SET_POP_N,
        "set_push_n": LUA_SET_PUSH_N
        }


SCRIPT_IDS = {}


"""
在redis上执行lua脚本
以最小化的成本批量操作
"""



def load_lua_scripts(node): 
    for x,v in SCRIPTS.items(): 
        SCRIPT_IDS[x] = node.script_load(v) 



"""
list_pop_n(redis, "mykey", 10)
"""
def list_pop_n(redis, key, n): 
    return redis.evalsha(SCRIPT_IDS["list_pop_n"], 2, key, n) 


"""
list_pop_n(n, redis, "mykey", "1", "2", "3", "4")
"""
def list_push_n(redis, key, *args):
    return redis.evalsha(SCRIPT_IDS["list_push_n"], len(args)+1,  key, *args)



def set_pop_n(redis, key, n):
    return redis.evalsha(SCRIPT_IDS["set_pop_n"], 2, key, n)


def set_push_n(redis, key, *args):
    return redis.evalsha(SCRIPT_IDS["set_push_n"], len(args)+1,  key, *args)



def profile_func(func, *args):
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
    time_a = time.time()
    func(*args)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats() 
    print s.getvalue() 


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



def forward_keys(redis, result, dst):
    qname = dst["name"] 
    kp = dst.get("key_pat")
    if kp:
        pat, part = kp
        if part == "site_id":
            part = CONFIG["site_id"] 
        for k,v in result:
            key = pat % (k, part)
            redis.set(key, v)
    else:
        for k, v in result:
            redis.set(key, v)



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
    elif tp == "str":
        forward_keys(redis, result, dst)
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


PRICE_STRIPED = set((u"¥", " ", "\t", "\n", "`"))


def fix_price(text): 
    ret = []
    for i in text:
        if i not in PRICE_STRIPED:
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
        if stock > 0 and price < 0:
            log_with_time("bad price: %s" % str(i)) 
        if price < 0:
            stock = -1
            price = -1
        ret.append((site_id, urlcrc, price, stock))
    return ret 


QUERY_METHODS = set(("get", "head", "delete", "trace", "option"))
UPLOAD_METHODS = set(("post", "delete")) 


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
        if gt["method"] in QUERY_METHODS:
            h, c = do(l, query = gt.get("query")) 
        elif gt["method"] in UPLOAD_METHODS:
            h, c= do(l, payload = gt.get("payload"))
        else:
            log_with_time("unknown method: %s" % gt["method"])
            continue 
        if h["status"] != 200:
            log_with_time("get %s failed" % h) 
            exit(1) 
        result = parser(l, c, fromlist[l]) 
        if result and rule.get("price_range"):
            urls = load_price_range(rule["price_range"]) 
            result = replace_url_with_ranges(result, urls) 
        if result and rule.get("hotlimit"):
            result = hotzone_filter(result, rule)
        forward_dst(result, rule) 


def hotzone_filter(result, rule):
    d = result 
    limit = rule.get("hotlimit")
    result = []
    for i in d:
        result.append((i, limit))
    return result 


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



def replace_url_with_ranges(result, urls): 
    filtered = []
    for i in result:
        if i in urls:
            filtered.append(i)
            result.extend(urls[i]) 
    rset = set(result)
    for i in filtered:
        rset.remove(i)
    return list(rset)



def load_price_range(name): 
    if not name.startswith("/"):
        subdir = "modules/%s/%s" % (CONFIG["site"], name) 
        name = os.path.join(os.path.dirname(__file__), subdir) 
    items = open(name).read().split("#") 
    urls = {}
    for i in items:
        if not i:
            continue
        lines = []
        for j in i.split("\n"):
            j = j.strip(" \r")
            if not j:
                continue 
            lines.append(j) 
        urls[lines[0]] = lines[1:] 
    return urls 
    


def sleep_with_counter(n):
    for i in range(1, n+1):
        log_with_time("sleeping, cnt, %s" % i)
        time.sleep(1) 



def load_func(path): 
    import spider.modules
    parts = path.split(".") 
    if getattr(spider.modules, path, ""):
        return getattr(spider.modules, path)
    ms = os.listdir(os.path.join(SPIDER_DIR, "modules"))
    if len(parts) == 2 and parts[0] in ms: 
        module = import_module("spider.modules.%s" % parts[0]) 
    else: 
        module = import_module(".".join(parts[:-1]))
    return getattr(module, parts[-1])  



def forward_result(task):
    rule = CONFIG["rule"]
    try: 
        result = task["to"](task, rule.get("rule")) 
    except:
        traceback.print_exc()
        exit(1) 
    if not result:
        log_with_time("empty result: %s" % task["url"])
        return
    if result and ("dst" in rule or "multidst" in rule):
        log_with_time("result of %s" % task["url"])
        forward_dst(result, rule)



def forward_dp(task): 
    if "crc" not in task:
        log_with_time("lost crc: %s" % task["url"])
        return 
    status = task["resp_header"]["status"] 
    if CONFIG.get("proxy"):
        CONFIG["origin_node"].srem(CONFIG["origin"], task['origin'])
    if status != 200: 
        log_with_time("status: %s, %s" % (status, task["url"])) 
        return
    CONFIG["fpack"].add(task["url"], task["text"], crc=task["crc"]) 
    key = (CONFIG["site_id"] << 48) | ctypes.c_uint(task["crc"]).value
    CONFIG["lc"].set(key, 0) 
    log_with_time(task["url"]) 



def get_name_by_xpath(text, expr): 
    tree = etree.HTML(text)
    nodes = tree.xpath(expr)
    if not nodes:
        log_with_time("invalid xpath")
        return 
    return str(nodes[0])


def forward_file(task):
    fconfig = CONFIG["fconfig"]
    ftype = fconfig.get("type", "url")
    path = fconfig.get("path", "")
    text = task["text"] 
    if ftype == "url":
        name = task["url"]
    elif ftype == "xpath": 
        expr = fconfig.get("xpath")
        name = get_name_by_xpath(text, expr) 
        assert name
        name += fconfig.get("suffix", ".tmp")
    elif ftype == "hex":
        name = hashlib.sha1(task["url"]).hexdigest() 
    if fconfig.get("compress"):
        text = zlib.compress(text) 
    fname = os.path.join(path, name)
    f = open(fname, "w+")
    f.write(text)
    f.close() 


def forward_offshelf(task):
    if "crc" not in task:
        log_with_time("lost crc %s" % task["url"])
        return
    rule = CONFIG["rule"] 
    try:
        result = CONFIG["to_parser"](task, rule.get("rule"))
    except:
        traceback.print_exc()
        exit(1) 
    forward_dst(result, CONFIG["rule"])




def batch_parser(task): 
    rule = CONFIG["rule"]
    not200 = rule["get"].get("not200") 
    if CONFIG.get("proxy"):
        CONFIG["origin_node"].srem(CONFIG["origin"], task['origin'])
    if task["resp_header"]["status"] != 200:
        if not200 == "log": 
            log_with_time("not200: %s %s" % (task["resp_header"],
                task["url"]))
        elif not200 == "trace":
            pdb.set_trace() 
        return 
    qtype = rule.get("dst", {}).get("qtype", "redis") 
    if qtype == "redis": 
        forward_result(task)
    elif qtype == "file":
        forward_file(task)
    elif qtype == "dp":
        forward_dp(task) 
    elif qtype == "off":
        forward_offshelf(task)
    else:
        log_with_time("unknown dst qtype: %s" % qtype)
        exit(1) 



def async_config(rule): 
    args = rule["get"]["args"]
    for i in ("limit", "interval", "retry"):
        if i in args:
            async_http.config[i] = args[i]
    async_http.debug = args.get("debug") 
    default = ("url", "parser", "to", "origin",
            "method", "old_url", "payload", "proxy", "cookie", "crc", "limit")
    keys = set(args.get("keys", [])).union(set(default)) 
    prev_keys = set(async_http.copy_keys)
    keys = keys.union(prev_keys)
    async_http.copy_keys = tuple(keys) 



def split_list_iter(l, n):
    le = len(l)
    c = le / n
    if le % n:
        c += 1 
    for i in range(c):
        yield l[i*n:(i+1)*n] 



def apply_group_filter(items, model): 
    loader = CONFIG["src_loader"] 
    flt = CONFIG["src_filter"] 
    items = [loader(item) for item in items]
    tasks = [] 
    for i in flt(items): 
        i.update(model)
        tasks.append(i)
    return tasks



def apply_single_filter(items, model): 
    tasks = [] 
    guard = CONFIG.get("proxy")
    loader = CONFIG["src_loader"]
    flt = CONFIG["src_filter"]
    for i in items: 
        unpacked = loader(i)
        t = flt(unpacked)
        if guard:
            t["origin"] = i
        t.update(model.copy())
        tasks.append(t)
    return tasks



def task_with_randua(rule): 
    header = async_http.html_header.copy()
    header["User-Agent"] = async_http.random_useragent() 
    return {
            "method": rule["get"]["method"],
            "to": CONFIG["to_parser"],
            "parser": batch_parser, 
            "header": header 
            } 


def task_simple(rule):
    return {
            "method": rule["get"]["method"],
            "to": CONFIG["to_parser"],
            "parser": batch_parser, 
            "header": async_http.default_header.copy()
            } 


def setup_proxy(rule): 
    default_node = CONFIG["nodes"].get("default")
    if not default_node:
        return
    if rule["src"].get("proxy"):
        CONFIG["proxy"] = True 
        CONFIG["origin_node"] = node
        CONFIG["origin"] = rule["src"]["origin"]
    else:
        CONFIG["proxy"] = False 


def get_source_from_redis(src, node): 
    tp = src.get("type")
    qname = src["name"]
    batch = src.get("batch", 1) 
    if tp == "list":
        items = list_pop_n(node, qname, batch)
    elif tp == "set":
        items = set_pop_n(node, qname, batch)
    elif tp == "hash": 
        items = node.hgetall(qname) 
    else:
        log_with_time("unknown src type") 
        exit(1) 
    return items



def get_source_from_file(src): 
    pass



def get_source(src, node): 
    qtype = src.get("qtype", "redis")
    if qtype == "redis": 
        return get_source_from_redis(src, node)
    elif qtype == "file":
        return get_source_from_file(src)
    elif qtype == "loader":
        return CONFIG["src_loader"](src, node)
    elif qtype == "dp":
        return get_source_from_dps(src, node) 
    else:
        log_with_time("unknown qtype type") 
        exit(1) 



def apply_filter(rule, items): 
    randua = rule["get"].get("randua")
    group = rule["src"].get("group") 
    if randua: 
        md = task_with_randua(rule) 
    else:
        md = task_simple(rule) 
    if group:
        tasks = apply_group_filter(items, md)
    else:
        tasks = apply_single_filter(items, md) 
    return tasks 



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


def get_dp_items(src, origins): 
    dps_redis = get_node("dp_redis") 
    unpack = msgpack.unpackb
    qname = src["name"]
    b = []
    for i in list_pop_n(dps_redis, qname,  1000): 
        item = unpack(i)
        if CONFIG["proxy"]:
            origins[item[0]] = i
        b.append(item)
    return b



def get_dps_diffset(src): 
    diffset = [] 
    atime = time.time() 
    origins = {} 
    while True: 
        if time.time() - atime > 600: 
            log_with_time("wait timeout, got: %s" % len(diffset))
            break 
        b = get_dp_items(src, origins)
        if not b:
            log_with_time("sleeping")
            time.sleep(src.get("wait", 1)) 
            continue 
        diffset.extend(dp_diff(CONFIG["lc"], b)) 
        if len(diffset) >= 1000:
            break 
    return diffset, origins



def get_source_from_dps(src, node): 
    diffset, origins = get_dps_diffset(src) 
    tasks = [] 
    for crc, url in diffset: 
        task = { 
            "url": url, 
            "crc": int(crc), 
            } 
        tasks.append(task) 
    return tasks 



def clean_proxies(node, qname): 
    for v in async_http.failed_tasks.itervalues(): 
        if v.get("proxy"):
            log_with_time("invalid proxy: %s" % v["proxy"])
            node.srem(qname, v["proxy"]) 



def set_proxies(node,  qname, tasks):
    for t in tasks: 
        proxy = node.srandmember(qname) 
        if proxy:
            t["proxy"] = proxy



def setup_dp_env(): 
    client = CONFIG["client"] 
    default_node = client["nodes"]["default"]
    CONFIG["lc"] = llkv.Connection(**client["llkv_dp"])
    CONFIG["fpack"] = filepack2.FilePack(db = default_node,
        limit = 1000, site_id=CONFIG["site_id"],
        datadir="/mnt/mfs") 
    CONFIG["to_parser"] = batch_parser 



def setup_config(rule): 
    if rule["get"].get("args"):
        async_config(rule) 
    CONFIG["rule"] = rule
    setup_proxy(rule)
    src = rule["src"]
    if "filter" in src:
        CONFIG["src_filter"] = load_func(src["filter"])
    else:
        CONFIG["src_filter"] = lambda x: x
    qtype = src.get("qtype", "redis") 
    if qtype == "loader":
        CONFIG["src_loader"] = load_func(src["loader"])
    elif qtype == "redis":
        CONFIG["src_loader"] = msgpack.unpackb 
    elif qtype == "dp":
        CONFIG["src_loader"] = lambda x: x
        setup_dp_env()
    dst_parser = rule.get("get", {}).get("parser")
    if dst_parser:
        CONFIG["to_parser"] = load_func(dst_parser) 
    multidst = rule.get("multidst", {}) 
    for v in multidst.values():
        if v.get("qtype") == "file": 
            CONFIG["fconfig"] = dst 
    dst = rule.get("dst")
    if dst and dst.get("qtype") == "file":
        CONFIG["fconfig"] = dst 


def flush_dp_files():
    mlen = len(CONFIG["fpack"].meta) 
    if not mlen:
        return
    log_with_time("flush %s files to disk" % mlen) 
    CONFIG["fpack"].flush()
    time.sleep(5) 



def get_node(node=None): 
    if not node: 
        return CONFIG["nodes"].get("default")
    con = CONFIG["nodes"].get(node)
    if not con:
        return CONFIG["nodes"].get("default")
    return con



def run_batch(rule): 
    setup_config(rule)
    src = rule["src"] 
    node = get_node(src.get("node"))
    default_node = get_node()
    qtype = src.get("qtype", "redis") 
    wait = rule.get("wait")
    while True: 
        items = get_source(src, node) 
        tasks = apply_filter(rule, items) 
        if rule["type"] == "dp" and not tasks:
            flush_dp_files()
            continue 
        if qtype == "redis" and not tasks:
            if not wait: 
                log_with_time("%s done" % rule["name"])
                exit(0)
            else:
                log_with_time('sleeping')
                time.sleep(wait)
                continue 
        if CONFIG.get("proxy"):
            set_proxies(default_node, src["proxysrc"], tasks)
            async_http.dispatch_tasks(tasks) 
            clean_proxies(default_node, src["proxysrc"]) 
        else:
            async_http.repeat_tasks(tasks) 
        if qtype == "file" or qtype == "loader":
            log_with_time("sleeping") 
            time.sleep(rule.get("wait", 1)) 



def run_worker_food(rule): 
    if not rule.get("repeat", 0): 
        forward_dst(rule["food"], rule) 
        log_with_time("%s done" % rule["name"]) 
        exit(0) 
    while True: 
        forward_dst(rule["food"], rule) 
        log_with_time("sleeping") 
        sleep_with_counter(rule.get("repeat")) 


def run_worker_fetch(rule): 
    if not rule.get("src"):
        gt = rule["get"] 
        run_single_repeat(rule) 
    else: 
        run_batch(rule) 


def run_worker(rule): 
    worker_types = {
            "fetch": run_worker_fetch,
            "food": run_worker_food,
            "ips": run_ips,
            "guard": run_guard, 
            "diff_dps": run_diff_dps,
            } 
    rt = rule.get("type") 
    if rule.get("boot"):
        boot = load_func(rule["boot"])
        boot(rule)
    if rt in worker_types:
        worker_types[rt](rule)
    else:
        log_with_time("unknown worker type: %s" % rt)


def my_server_id(): 
    import platform
    if "SuSE" in platform.dist():
        output = subprocess.check_output("/sbin/ifconfig", shell=True)
    else:
        output = subprocess.check_output("ifconfig", shell=True)
    myid = re.compile("192.168.1.([0-9]{1,3})").findall(output) 
    if not myid:
        myid = re.findall("172.[0-9]+.[0-9]+.([0-9]+)", output) 
    if not myid:
        myid = re.findall("10.[0-9]+.[0-9]+.([0-9]+)", output) 
    if myid:
        return myid[0] 
    else: 
        return "local"




def connect_mysql(config): 
    if "mysql_con" in CONFIG:
        try:
            CONFIG["mysql_con"].close() 
        except Exception as e:
            log_with_time("close prev mysql con failed") 
    CONFIG["mysql_con"] = MySQLdb.connect(**config)
    CONFIG["mysql_cur"] = CONFIG["mysql_con"].cursor() 
    CONFIG["mysql_config"] = config




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
    try:
        msg = u"%s: %s" % (time.ctime(), obj)
    except UnicodeDecodeError:
        msg = u"%s: %s" % (time.ctime(), repr(obj))
    if not debug: 
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
            connect_mysql(CONFIG["mysql_config"])
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
    load_config()
    eval_lua_scripts_for_nodes(commit_rule)
    import llkv
    client = CONFIG["client"]
    CONFIG["llkv"] = llkv.Connection(**client["llkv_list"])
    connect_mysql(client["mysql"]) 
    redis = get_node()
    unpack = msgpack.unpackb 
    site_config = CONFIG["sites"]["idx"]
    replace_stdout(site_config.get("log", "/tmp/spider-commit.log")) 
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
    eval_lua_scripts_for_nodes(dp_idx_rule) 
    connect_mysql(CONFIG["client"]["dp_idx"])
    node = get_node()
    wait = dp_idx_rule.get("wait", 2) 
    site_config = CONFIG["sites"]["idx"]
    replace_stdout(site_config.get("log", "/tmp/spider-idx.log"))
    while True:
        l = node.lpop("dp_idx") 
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



def valid_tester(task):
    status = task["resp_header"]["status"] 
    if status != 200:
        log_with_time("bad proxy: %s" % task["proxy"]) 
        return 
    if not task["check"](task["resp_header"], task["text"]):
        log_with_time("no match: %s" % task["proxy"]) 
    else:
        log_with_time("match: %s" % task["proxy"]) 
        CONFIG["ips_node"].sadd(CONFIG["ips_qname"], task["proxy"]) 


proxy_src = "http://ff.daili666.com/ip/?tid=828576762586978&num=90000&foreign=none" 


def run_ips(rule): 
    if rule["get"].get("args"):
        async_config(rule)
    CONFIG["ips_node"] = CONFIG["nodes"]["default"]
    CONFIG["ips_qname"] = rule["dst"]["name"]
    url = rule.get("url", "http://www.jd.com")
    func = load_func(rule["get"]["parser"])
    while True:
        try:
            h,c = simple_http.get(proxy_src)
        except socket.error:
            time.sleep(1)
            log_with_time("sleeping")
            continue
        tasks = []
        ips = c.split("\n")
        log_with_time("got %s ips" % len(ips))
        for i in ips:
            if ":" not in i:
                continue
            t = {
                "url": url,
                "proxy": "http://%s" % i.strip("\r\n"),
                "parser": valid_tester,
                "check": func,
                }
            tasks.append(t)
        async_http.repeat_tasks(tasks)
        if not rule.get("wait"):
            log_with_time("ips done")
            break
        else:
            time.sleep(rule.get("wait"))
            log_with_time("sleeping") 



def run_guard(rule): 
    eval_lua_scripts_for_nodes(rule) 
    tp = rule["src"]["type"]
    qname = rule["src"]["name"] 
    node = CONFIG["nodes"][rule["dst"].get("node", "default")]
    dname = rule["dst"]["name"]
    wait = rule.get("wait", 2)
    assert tp == "set"
    while True:
        members = node.smembers(qname)
        if not members:
            log_with_time("sleeping") 
            time.sleep(wait)
            continue
        list_push_n(node, dname, *members)
        while True:
            dlen = node.llen(dname)
            if dlen == 0:
                log_with_time("get next group")
                break
            else:
                log_with_time("waiting: %s" % dlen) 
                time.sleep(wait) 



def get_promo_type(desc):
    """ Get the promo type.

    其他： 0
    满减： 1
    满返： 2
    满赠： 3
    加价购： 4
    多买优惠：5
    封顶促销：6
    第二件半价: 7
    """
    promo_type = 0
    if u'满' in desc and u'减' in desc:
        promo_type = 1
    elif u'券' in desc or u'返' in desc:
        promo_type = 2
    elif (u'满' in desc and u'赠' in desc) or (u'增' in desc) or (u'送' in desc):
        promo_type = 3
    #5, 6, 7 ->折扣, 11
    #白菜 -> 12
    #手机 -> 9
    #团购 -> 8
    #优惠券 -> 10 
    #elif u'加' in desc and u'加入' not in desc:
    #    promo_type = 4
    #elif u'多买' in desc or u'多折' in desc:
    #    promo_type = 5
    #elif u'封顶' in desc:
    #    promo_type = 6
    #elif u'第二件半价' in desc:
    #    promo_type = 7 
    return promo_type 



def flush_lines(): 
    if "conf" in globals() and len(CONFIG["line_buffer"]):
        print "\n".join(CONFIG["line_buffer"])



def load_site(site): 
    s = CONFIG["sites"].get(site)
    if not s:
        print "bad site: %s" % site
        exit(1) 
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


def diff_dps(rule): 
    load_config() 
    name = get_dst_by_node(CONFIG["module"], "dps_log") 
    if not name:
        log_with_time("no dps_log in dst")
        return
    node = CONFIG["nodes"]["dps_log"] 
    intime_crcs_set = load_intime_dps(node, name)
    path = "/price_b2c/%s.old" % CONFIG["site_id"] 
    price_dps = load_price_dps(path)
    path = "/pub_file/last_url/%s.txt" % CONFIG["site_id"]
    url_dps = load_history_dps(path)
    newset = price_dps.intersection(url_dps)
    del price_dps
    del url_dps
    target = newset.difference(intime_crcs_set)
    del newset 
    path = "/pub_file/last_url/%s.txt" % CONFIG["site_id"] 
    result = dump_urls_from_crcs(target, path) 
    del target
    cnt = 0
    for i in split_list_iter(result.items(), 1000):
        cnt += 1000
        log_with_time("final stage: %s/%s" % (cnt, len(result)))
        forward_dst(i, rule)



def run_diff_dps(rule): 
    wait = rule.get("wait", 20000)
    while True:
        diff_dps(rule)
        sleep_with_counter(wait) 



blt_worker = {
        "commit": run_commit,
        "idx": run_dp_idx, 
        } 




def import_all_sites():
    _ = os.path
    mdir = _.join(_.dirname(__file__), "modules")
    ms = {}
    for m in os.listdir(mdir): 
        if os.path.isdir(_.join(mdir, m)) and get_siteid(m):
            module = import_module("spider.modules.%s" % m) 
            ms[m] = module
    return ms


def get_dst_by_node(module, node): 
    site_id = get_siteid(CONFIG["site"])
    rule = getattr(module, "rule", [])
    for r in rule:
        target = r.get("dst", {})
        if target.get("node") == node:
            return target.get("name")
        dst = r.get("multidst", {}) 
        for n in dst.values(): 
            if n.get("node") == node:
                return n.get("name")
    return



def load_intime_dps(node, name): 
    dpids = node.hgetall(name)
    expires_time = int(time.time() - 3 * 24 * 3600)
    ret = set()
    unpackb = msgpack.unpackb 
    for k,v in dpids.items():
        if unpackb(v) < expires_time:
            node.hdel(name, k)
        else:
            ret.add(k)
    return ret


def load_history_dps(path): 
    pat = "[0-9]+\t%s\t([-0-9]+)\t" % CONFIG["site_id"]
    dp_pattern = re.compile(pat)
    m10 = 1024 * 1024 * 100
    cnt = 0
    fobj = open(path)
    target_set = set()
    t_add = target_set.add
    while True:
        data = fobj.read(m10)
        lastline = data.rfind("\n") 
        if lastline <= 0:
            break
        fobj.seek(lastline - len(data), io.SEEK_CUR)
        result = dp_pattern.findall(data) 
        for item in result: 
            t_add(item)
        print "load_history_dps", CONFIG["site_id"], len(target_set)
    return target_set 



def load_price_dps(path): 
    pat = '([0-9-]+)\t([0-9-]+)\t([0-9-]+)\n'
    list_pattern = re.compile(pat)
    m10 = 1024 * 1024 * 100
    cnt = 0
    fobj = open(path)
    target_set = set()
    t_add = target_set.add 
    while True:
        data = fobj.read(m10) 
        lastline = data.rfind("\n") 
        if lastline <= 0:
            break 
        fobj.seek(lastline - len(data), io.SEEK_CUR)
        result = list_pattern.findall(data) 
        for item in result:
            key, price, stock = item 
            try:
                price = int(price)
                stock = int(stock)
            except ValueError:
                print "garbage:", item
                continue
            if price > 0 and stock > 0:
                t_add(key) 
        print "load_price_dps", CONFIG["site_id"], len(target_set) 
    return target_set 



def dump_urls_from_crcs(crcs, path):
    pat = "%s\t([-0-9]+)\t(http.*)\t" % CONFIG["site_id"]
    dp_pattern = re.compile(pat)
    m10 = 1024 * 1024 * 100
    cnt = 0
    fobj = open(path)
    target = {}
    while True:
        data = fobj.read(m10)
        lastline = data.rfind("\n") 
        if lastline <= 0:
            break
        fobj.seek(lastline - len(data), io.SEEK_CUR)
        result = dp_pattern.findall(data) 
        for item in result: 
            crc, url = item
            target[crc] = url 
        print "dump_urls_from_crcs", CONFIG["site_id"], len(target)
    result = {}
    for crc in crcs: 
        if crc in target:
            result[crc] =target[crc] 
    return result 




def get_siteid(site):
    ret = []
    for k,v in CONFIG["sites"].items():
        if k.startswith(site): 
            ret.append(v["site_id"]) 
    if not ret:
        return 
    return min(ret)



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
        role = my_server_id() 
    try:
        config = import_module("spider.configs.%s" % role) 
    except Exception as e:
        print "import error: %s" % e 
        print "use config local instead."
        config = import_module("spider.configs.local") 
    config_module = CONFIG.get("config_module")
    if config_module:
        config = reload(config_module)
    else:
        CONFIG["config_module"] = config
    CONFIG["client"] =  config.CLIENT
    CONFIG["sites"] = config.SITES 


role = "" 


def load_config(): 
    CONFIG["myid"] = 170 
    CONFIG["line_cnt"] = 0
    CONFIG["line_buffer"] = [] 
    CONFIG["log_name"] = "-".join(sys.argv[1:]) 
    use_config(role)



def connect_redis(db): 
    con = redis.StrictRedis(**db) 
    load_lua_scripts(con)
    return con 


def eval_lua_scripts_for_node(redis_nodes, node): 
    nodes = CONFIG["client"]["nodes"] 
    qpat = node.get("queue_pat")
    if qpat: 
        pat, key = qpat
        if key == "site_id":
            node["name"] = pat % (node["name"],
                    str(CONFIG["site_id"]))
    node = node.get("node", "default")
    if node not in redis_nodes:
        redis_nodes[node] = connect_redis(nodes[node]) 



def eval_lua_scripts_for_nodes(rule): 
    redis_nodes = {} 
    CONFIG["nodes"] = redis_nodes 
    if not rule.get('dst') and not rule.get("multidst"):
        log_with_time("rule format error, no dst")
        exit(1); 
    for v in rule.get("multidst", {}).values():
        eval_lua_scripts_for_node(redis_nodes, v)
    dst = rule.get("dst")
    if dst:
        eval_lua_scripts_for_node(redis_nodes, dst)
    src = rule.get("src")
    if src and src.get("type") != "file": 
        eval_lua_scripts_for_node(redis_nodes, src)



def setup_site(site, cat): 
    load_config() 
    if site in blt_worker: 
        blt_worker[site]()
        exit(0)
    m = load_site(site) 
    #查找相应的worker
    rule = getattr(m, "rule") 
    target = get_cat_from_rule(rule, cat)
    if not target:
        print "worker %s not exists" % cat
        exit(1) 
    site_id = CONFIG["sites"][site]["site_id"]
    CONFIG["site_id"] = site_id
    CONFIG["site"] = site 
    CONFIG["module"] = m 
    eval_lua_scripts_for_nodes(target) 
    return target



def setup_subsite(rule, cat): 
    subsites = getattr(CONFIG["module"], "sites", {})
    if not subsites:
        run_worker(rule)
        exit(0)
    #顺序执行分站 
    if subsites.get("source") == "cats" and cat == "cats":
        repeat = rule.get("repeat")
        rule["old_dst"] = rule["dst"].copy()
        if not repeat:
            run_subsite(subsites, rule)
            exit(1) 
        while True:
            run_subsite(subsites, rule)
            sleep_with_counter(repeat)
    #修改分站队列名 
    site_id = CONFIG["site_id"]
    if site_id in subsites.get("sites", {}): 
        name = subsites["sites"][site_id] 
        if rule.get("dst") and rule["dst"].get("subsite"):
            rule["dst"]["name"] += "_" + name
        for v in rule.get("multidst", {}).values():
            if v.get("subsite"):
                v["name"] += "_" + name 
        if rule["src"].get("subsite"):
            rule["src"]["name"] += "_" + name 



def run_cat(site, cat): 
    import atexit
    atexit.register(flush_lines) 
    rule = setup_site(site, cat) 
    default_log = "/tmp/spider-%s-%s.log" % (site, cat) 
    site_config = CONFIG["sites"][site] 
    replace_stdout(site_config.get("log", default_log)) 
    setup_subsite(rule, cat)
    run_worker(rule) 



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
            start_worker(i, j)



def kill_workers(): 
    if not "workers" in CONFIG:
        return
    import signal
    for i,v in CONFIG["workers"].items():
        try:
            stop_worker(i)
            log_with_time("%s,  %s, %s killed" % (i, v[0], v[1]))
        except OSError:
            log_with_time("kill %s failed" % i) 



def run(): 
    load_config() 
    CONFIG["log_name"] = "/tmp/spider-all.log" 
    detach_and_set_log(CONFIG)
    workers = {}
    CONFIG["workers"] = workers 
    import atexit 
    atexit.register(kill_workers) 
    start_all_sites(workers) 
    run_master(workers)


def test_parser(case, rule): 
    parser = load_func(rule["get"]["parser"]) 
    if case.get("ignore"):
        log_with_time("ignore: %s" % case["url"]) 
        return
    url = case["url"] 
    func = load_func(case["check"])
    method = case.get("method", "get")
    h,c = getattr(simple_http, method)(url,
        query = case.get("query"),
        payload = case.get("payload"))
    if not h:
        raise IOError("request %s failed" % url)
    if not "src" in rule:
        func(parser(url, c, rule["from"][url])) 
    ctx = {"resp_header": h, "url": url, "text": c}
    ctx.update(case) 
    result = parser(ctx, rule.get("rule")) 
    func(result)


def test_parsers(site, cat, target): 
    print test_header_msg("test for [%s-%s]: " % (site, cat))
    test_header = "test for parser [%s]:"
    parser = target["get"]["parser"]
    for case in target["test"]: 
        try: 
            test_parser(case, target) 
            print test_pass_msg(test_header % parser)
        except: 
            print test_fail_msg(test_header % parser)
            traceback.print_exc()
            exit(1) 


def load_worker_and_test(site, cat): 
    global debug
    debug = True 
    load_config() 
    m = load_site(site) 
    if not m: 
        exit(1) 
    CONFIG["site_id"] = "test"
    rule = getattr(m, "rule") 
    target = get_cat_from_rule(rule, cat) 
    if not target:
        print "worker %s not exists" % cat
        exit(1) 
    eval_lua_scripts_for_nodes(target) 
    test = target.get("test")
    if not test:
        print "no test case"
        exit(1) 
    test_parsers(site, cat, target) 


def test_worker_pass(site, worker):
    if not os.fork():
        load_worker_and_test(site, worker) 
        exit(0) 
    pid, status, res = os.wait3() 
    sig = status & 0xf
    status = status >> 8 
    if not sig and status:
        return False
    return True 



def test_modules():
    config_dir = os.path.join(SPIDER_DIR, "configs") 
    configs = {} 
    for i in os.listdir(config_dir):
        if not i.endswith(".py") or "__init__" in i:
            continue
        name = i.split(".")[0] 
        m = import_module("spider.configs.%s" % name) 
        configs[name] = m 
    all_workers = {}
    for name, config in configs.items():
        for site, profile in config.SITES.items():
            if site not in all_workers:
                all_workers[site] = list(profile["workers"]) 
            else:
                all_workers[site].extend(list(profile["workers"])) 
    for site, workers in all_workers.items(): 
        print test_header_msg("test for site [%s]" % site)
        for worker in set(workers): 
            if site in blt_worker:
                continue
            if test_worker_pass(site, worker):
                print test_pass_msg(test_header)
            else:
                print test_fail_msg(test_header) 


class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m' 
    BLUE = '\033[94m'
    GREEN = '\033[92m' 
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    YELLOW = '\033[93m'
    RED = '\033[91m' 
    UNDERLINE = '\033[4m' 



def run_test_me():
    import traceback
    import test
    load_config()
    print test_header_msg("test functions:")
    for i, v in enumerate(test.all_cases):
        name, func = v
        test_header = "test for [%s]" % name
        try:
            func()
            print test_pass_msg(test_header)
        except:
            traceback.print_exc()
            print test_fail_msg(test_header)



def test_me():
    from spider import test
    spider_basic_test()
    run_test_me()


def test_pass_msg(msg):
    return "{:<40}{}pass{}".format(msg+":", bcolors.BLUE, bcolors.ENDC)


def test_fail_msg(msg):
    return "{:<40}{}failed{}".format(msg, bcolors.RED, bcolors.ENDC)


def test_header_msg(msg):
    return "%s%s%s" % (bcolors.YELLOW, msg, bcolors.ENDC)


def spider_basic_test(): 
    config_dir = os.path.join(SPIDER_DIR, "configs")
    module_dir = os.path.join(SPIDER_DIR, "modules") 
    configs = {}
    test_header = "syntax test for config [%s]"
    for i in os.listdir(config_dir):
        if not i.endswith(".py") or "__init__" in i:
            continue
        name = i.split(".")[0] 
        try:
            m = import_module("spider.configs.%s" % name)
        except: 
            print test_fail_msg(test_header % name)
            traceback.print_exc()
            exit(1)
        print test_pass_msg(test_header % name) 
        configs[name] = m 
    test_header = "syntax test for module [%s]" 
    for name, config in configs.items(): 
        print test_header_msg("syntax test for config [%s]:" % name) 
        for site in config.SITES.keys():
            if site in blt_worker:
                continue
            if "." in site:
                site = site.split(".")[0]
            try:
                import_module("spider.modules.%s" % site) 
            except:
                print test_fail_msg(test_header % site)
                traceback.print_exc()
                exit(1) 
            print test_pass_msg(test_header % site)



def stop_worker(pid): 
    os.kill(pid, signal.SIGKILL)
    del CONFIG["workers"][pid] 



def start_worker(site, worker): 
    l = set()
    for v in CONFIG["workers"].values():
        l.add("%s-%s" % v)
    if "%s-%s" % (site, worker) in l:
        log_with_time("already running %s, %s" % (site, worker))
        return
    pid = detach_worker(site, worker)
    CONFIG["workers"][pid] = (site, worker)



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
            stop_worker(pid)
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
    start_worker(site, worker) 



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



def is_worker_alive(pid, site, worker):
    try:
        data = open("/proc/%s/cmdline" % pid).read()
    except IOError:
        return False
    if site in data and worker in data:
        return True
    return False 



def command_refresh(**kwargs): 
    try:
        load_config()
    except Exception as e:
        return {
                "status": False,
                "msg": str(e)
                } 
    workers = CONFIG["workers"]
    sites = CONFIG["sites"]
    oldworkers = {}
    reload_workers = []
    outdate_workers = []
    new_workers = []
    for pid, value in workers.items():
        site, worker = value 
        #stop the outdate
        if site not in sites:
            stop_worker(pid)
            outdate_workers.append(value)
            continue
        if worker not in sites[site]["workers"]:
            outdate_workers.append(value)
            stop_worker(pid)
            continue 
        #reload the dead
        if not is_worker_alive(pid, site, worker):
            reload_workers.append(value)
            start_worker(site, worker) 
        if site in oldworkers: 
            oldworkers[site].append(worker)
        else:
            oldworkers[site] = [worker] 
    #load the new worker
    for site in sites: 
        for worker in sites[site]["workers"]:
            if worker not in oldworkers.get(site, []):
                new_workers.append((site, worker))
                start_worker(site, worker) 
    return {
            "status": True,
            "outdate": outdate_workers,
            "reload": reload_workers,
            "new": new_workers,
            } 


master_comamds = {
        "stopall": command_stopall,
        "startall": command_startall,
        "stop": command_stop, 
        "start": command_start,
        "statall": command_statall,
        "stat": command_stat, 
        "getall": command_getall,
        "refresh": command_refresh,
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
        start_worker(site, worker) 
