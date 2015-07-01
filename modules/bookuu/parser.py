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
    t = etree.HTML(res['text'])
    nodes = t.xpath(rule)

    ret = []

    for node in nodes:
        node = node.replace(".html", '-pager_80.html')
        ret.append(node)
        #ret += [node + str(i) + '.html' for i in range(1, 51)]
    return ret

def test_cats(res):
    pdb.set_trace()

def pager(task, rule):
    t = etree.HTML(task['text'])
    pages = t.xpath(rule)
    if not pages:
        pages = 1
    else:
        try:
            pages = int(re.search("(?<=/)\d+", pages[0]).group())
        except:
            pages = 1
    u = task['url']
    u = u.replace(".html", "-p_")
    return [u + str(i) + '.html' for i in range(1, pages+1)]

itemurl = 'http://detail.bookuu.com/%s.html'
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    dps = {}
    for node in nodes:
        gid = node.xpath("h3/a/@href")
        price = node.xpath("div/p/b")
        stock = node.xpath("div/div/a[1]/@class")
        
        if not gid or not price or not stock:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = gid[0]
        price = re.search("\d+\.\d+|\d+", price[0].text).group()
        if "getCart" in stock[0]:
            stock = 1
        else:
            stock = 0
        ret.append((gid, price, stock))
    fret = format_price(ret)
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result": fret, "dps": dps}