#!/usr/bin/python2

from _http import *
from filepack import *

import MySQLdb as mysqldb

import async_http as ah
import sqlite3
import zlib
import pdb
import redis
import sys
import re
import os
import atexit

REDIS_SERVER = '192.168.1.191'
MYSQL_SERVER = '192.168.1.192'

LOCALHOST = '127.0.0.1'

gcount = type("gcount",(),{"count": 0})

redis = redis.Redis(host=REDIS_SERVER)
result = "dp_"

gdict = {
    "2": "dangdang"
}
pack = None

ah.config['limit'] = 100

formats = dict()

def dangdang_r(url):
    pattern = lambda x: 'http://product.dangdang.com/%s.html' % x
    if not 'aspx' in url:
        return url
    gid = re.search("(?<=product_id=)\d+", url).group()
    return pattern(gid)

def reformat(rid, url):
    if not rid in formats:
        return
    return formats[rid](url)

def page_parser(body):
    pack = body['filepack']
    sid = body['site_id']
    url = body['url']
    status = body['resp_header']['status']
    target = result + str(sid)
    #print("grab: %s %s %r" % (sid, url, status))
    if status == 200:
        pack.add(int(body['site_id']), body['url'], body['text'])
    else:
        print("err: %s %s %r" % (sid, url, status))

def myheader():
    ret = dict(html_header)
    ret["User-Agent"] = ah.random_useragent()
    return ret

def runtask(sid):
    rid = 'idx_'+ gdict[sid]
    pdb.set_trace()
    url = redis.lpop(rid)
    tasks = []
    while url:
        tasks.append({
            "url": reformat(sid, url.replace("\n", "")),
            "parser": page_parser,
            "site_id": sid,
            "header": myheader(),
            "retry": 0,
            "filepack": pack
        })
        if len(tasks) >= 5000:
            ah.dispatch_tasks(tasks)
            tasks = []
        url = redis.lpop(rid)
    if tasks:
        ah.dispatch_tasks(tasks)

def gencats(s, filter):
    rt = re.findall("(?<=\d\t).*"+filter+".*(?=\n)", s)
    sid = rt[0].split("\t")[0]
    le = len(rt)
    i = 0
    while i < le:
        redis.lpush('idx_'+filter, *rt[i:i+1000])
        i += 1000

def daemon(cb, log=None, *args):
    if not os.fork():
        os.setsid()
        p = os.fork()
        if not p:
            sys.stdin = open("/dev/null", "r")
            if log:
                fobj = open("log", "a+", buffering=0)
                sys.stdout = fobj
                sys.stderr = fobj
            cb(*args)
        else:
            exit()
    else: 
        os.wait()
        exit()

def eflush():
    pack.flush()

if __name__ == "__main__":

    formats["2"] = dangdang_r
    
    margs = {"host":MYSQL_SERVER, "db":'dp_idx', "user":'minishop', "passwd":"MiniShop!@#"}
    pack = FilePack(margs)

    atexit.register(eflush)

    if len(sys.argv) < 2:
        print("usage: aa [-d] file")
    else:
        if sys.argv[1] == '-d':
            daemon(runtask, "log", sys.argv[2])
        if sys.argv[1] == '-g':
            gencats(gdict, open(sys.argv[2]).read(-1), "dangdang")
        else:
            runtask(sys.argv[1])