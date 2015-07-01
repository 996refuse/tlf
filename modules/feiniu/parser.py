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

def cats(url, res, rule):
    t = etree.HTML(res['text'])
    nodes = t.xpath(rule)
    return set(nodes)

def pager(task, rule):
    t = etree.HTML(task['text'])
    pages = t.xpath(rule)
    if not pages:
        pages = 1
    else:
        pages = int(pages[0])
    u = task['url']
    return [u + '/?page=' + str(i) for i in range(1, pages+1)]

dp_base = "http://www.feiniu.com/item/%s"

priceurl = 'http://www.feiniu.com/category/get_item_promo/'
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    dps = {}
    dp = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        if not gid:
            log_with_time("bad rules: %r" % task['url'])
        _gid = re.search("(?<=item/).+", gid[0])
        if not _gid:
            _gid = re.search("(?<=com/).+", gid[0])
            if not id: 
                log_with_time("bad regex: %r" % task['url'])
                continue
        gid = _gid.group()
        dp.append((dp_base % gid, "")) 
        ret.append(gid) 
    return {
            "price":  [
                {
                "url": priceurl,
                "payload": {
                    "itemid": ','.join(ret)
                }
                }],
            "dp": dp
            }

itemurl = 'http://www.feiniu.com/item/%s'
def price_parser(task, rule):
    try:
        j = json.loads(task['text'])
    except:
        log_with_time("bad response: %s"%task['url'])
        return
    if not j:
        log_with_time("bad request: %s"% task["payload"])
        return
    ret = []
    for k,v in j.items():
        stock = 1 if v['cart_class'] else 0
        ret.append([itemurl%k, v['price'], stock])
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result": fret, "dps": dps}
