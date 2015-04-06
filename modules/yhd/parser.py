#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def cats_parser(url, content,  rule):
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        oo = []
        for v in items:
            if 'list' in v:
                p = 'http://list.yhd.com/'
                s = v[len(p):]
                ti = s.index('/')
                if ti == len(s)-1 or s[ti+1] == '/':
                    oo.append(p+s[:ti])
        o1 = set(oo)
        ret.extend(list(o1))
    return ret

def pager(task, rule): 
    burl = 'http://list.yhd.com/searchPage/c30786-0-81933/b/a-s1-v0-p%s-price-d0-f0-m1-rt0-pid-mid0-k'
    tree = etree.HTML(task["text"])
    count = tree.xpath(rule) 
    if not count:
        log_with_time("pager, no count: %s" % task["url"])
        return []
    count = int(count[0])
    ret = []
    for i in range(1, count+1):
        ret.append(burl%str(i))
    return ret

def list_parser(task, rule):
    try:
        j = json.loads(task["text"])
        t = etree.HTML(j['value'])
        nodes = t.xpath(rule["node"])
    except:
        log_with_time("bad response %s"%task['url'])
        return []
    ret = []
    for node in nodes:
        pid = node.xpath(rule['pid'])
        price = node.xpath(rule['price'])
        if not pid or not price:
            log_with_time("wrong rule. please fix. %r %r %r"%(pid,price,stock))
            continue
        ret.append((pid[0], price[0]))
    return ret

def stock_parser(task, rule):
    j = json.loads(task["text"])
    if not j: 
        log_with_time("bad response: %s" % task["url"])
        return
    ret = []
    for i in j:
        if int(i["localStock"]):
            stock = 1
        else:
            stock = 0
        qid = str(i["productId"])
        ret.append((qid, task['price'][qid], stock))
    result = format_price(ret)
    return ret