#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json
import time

def cats_parser(url, res, rule):
    content = res['text']
    t = etree.HTML(content)
    nodes = t.xpath(rule)

    ret = []

    for node in nodes:
        ret += node.split("|")

    return ret

def pager(task, rule):
    burl = task['url'].split("#")[0]
    t = etree.HTML(task['text'])
    lastpage = t.xpath(rule)

    ret = []

    if not lastpage:
        pagenum = 1
    else:
        lastpage = lastpage[0]
        pagenum = int(lastpage.text)

    for i in range(1, pagenum+1):
        ret.append(burl + '?pageNum=' + str(i) + '&')
    return ret

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        ostock = node.xpath(rule['ostock'])
        if not gid:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = re.search("\d+", gid[0]).group()
        if not ostock:
            stock = 1
        else:
            stock = 0
        ret.append((gid, stock))
    return ret

def test_list(res):
    assert(res[0][1])

itemurl = "http://www.jiuxian.com/goods-%s.html"
def price_parser(task, rule):
    j = json.loads(task['text'])
    stocks = task['stock']
    
    ret = []

    try:
        for k,v in j['data'].items():
            ret.append((itemurl%k, v['np'], stocks[k]))
    except:
        pdb.set_trace()
        return []
    
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result":fret, "dps":dps}