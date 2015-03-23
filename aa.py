#!/usr/bin/python2

from _http import *
import async_http as ah
import zlib
import pdb
import redis
import sys
import re
import os

redis = redis.Redis(host='192.168.1.191')
result = "dp_"

gdict = dict()

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
    target = result + str(body['site_id'])
    print("grab: %s %s %r" % (body['site_id'], body['url'], body['resp_header']['status']))
    if body['resp_header']['status'] == 200:
        redis.lpush(target, zlib.compress(body['text']))
    else:
        redis.lpush(target, body['resp_header']['status'], body['url'])

def myheader():
    ret = dict(html_header)
    ret["User-Agent"] = ah.random_useragent()
    return ret

'''
def runtasks(f):
    l = f.readline()
    while l:
        c = 0
        tasks = []
        while c < 5000 and l:
            sid, url = l.split("\t")
            if sid != '2':
                l = f.readline()
                continue
            tasks.append({
                "url": reformat(sid, url.replace("\n", "")),
                "parser": page_parser,
                "site_id": sid,
                "header": myheader(),
                "retry": 0
            })
            c += 1
            l = f.readline()
        #print("dispatch tasks %r" % len(tasks))
        ah.dispatch_tasks(tasks)
'''

def runtask(sid, urls):
    cc = len(urls) // 5000 + (1 if len(urls) % 5000 else 0)
    for i in range(0, cc):
        tasks = []
        for url in urls[i*5000:(i+1)*5000]:
            tasks.append({
                "url": reformat(sid, url.replace("\n", "")),
                "parser": page_parser,
                "site_id": sid,
                "header": myheader(),
                "retry": 0
            })
        #pdb.set_trace()
        ah.dispatch_tasks(tasks)

def runtasks(gdict):
    for k,v in gdict.items():
        runtask(*v)

def gencats(s, filter):
    return  re.findall("(?<=\d\t).*"+filter+".*(?=\n)", s)

def daemon(cb, log=None, *args):
    if not os.fork():
        os.setsid()
        p = os.fork()
        if not p:
            sys.stdin = open("/dev/null", "r")
            if log:
                fobj = open(log, "a+", buffering=0)
                sys.stdout = fobj
                sys.stderr = fobj
            cb(*args)
        else:
            exit()
    else: 
        os.wait()
        exit() 

if __name__ == "__main__":
    def main(fn):
        buf = open(fn).read(-1)
        gdict['dangdang'] = ("2", gencats(buf, 'dangdang'))
        runtask(*gdict['dangdang'])

    formats["2"] = dangdang_r

    if len(sys.argv) < 2:
        print("usage: aa [-d] file")
    else:
        if sys.argv[1] == '-d':
            daemon(main, "log_ck", sys.argv[2])
        else:
            main(sys.argv[1])