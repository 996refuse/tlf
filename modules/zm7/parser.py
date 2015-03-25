#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def cats_parser(url, content, rule):
    burl = "http://www.zm7.cn/"
    t = etree.HTML(content)
    ret = [burl + i for i in t.xpath(rule)]

    return ret

def pager(task, rule):
    pad = lambda n: "min0-max0-attr0-%d-sort_order-ASC.html" % n
    burl = task['url'][:-5] + '-'
    t = etree.HTML(task['text'])
    pagetxt = t.xpath(rule)

    ret = []
    
    if not pagetxt:
        log_with_time("bad response: %r" % task['url'])
        return ret

    pagetxt = pagetxt[0].text
    pagenum = re.findall("\d+", pagetxt)
    pagenum = int(pagenum[-1])
    for i in range(1, pagenum+1):
        ret.append(burl+pad(i))
    return ret

def list_parser(task, rule):
    burl = "http://www.zm7.cn/"
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("a/@href")
        price = node.xpath("p/span")
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = burl + gid[0]
        price = price[0].text
        price = re.search("\d+\.\d+", price).group()
        ret.append((gid, price))
    return ret

def stock_parser(task, rule):
    ret = []
    ostock = re.search("暂时无货", task['text'])

    gid = task["url"]
    price = task["price"]

    if ostock:
        stock = 0
    else:
        stock = 1

    ret = [(gid, price, stock)]
    fret = format_price(ret)
    return fret