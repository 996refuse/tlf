#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def pager(url, res, rule):
    content = res['text']
    burl = url
    tree = etree.HTML(content)
    pgs = tree.xpath(rule)
    
    if not pgs:
        pagenum = 1
    else:
        pagenum = int(tree.xpath(rule)[0].text)

    ret = []

    for i in range(1, pagenum+1):
        ret.append(burl + '/pg' + str(i))

    return ret

def list_parser(task, rule):
    tree = etree.HTML(task["text"])
    nodes = tree.xpath(rule["node"])
    ret = []
    for node in nodes:
        gidurl = node.xpath(rule['gidurl'])
        price = node.xpath(rule['price'])
        if not gidurl or not price:
            log_with_time("list parser err: %r" % task['url'])
            continue
        gidurl = gidurl[0]
        price = price[0].text[1:]
        ret.append((gidurl, price))
        ret = list(set(ret))
    return ret

def stock_parser(task, rule):
    t = etree.HTML(task["text"])
    stock = t.xpath(rule)
    ret = []
    if not stock:
        log_with_time("bad response: %s" % task["url"])
        return ret
    if int(stock[0].text):
        stock = 1
    else:
        stock = 0
    ret.append((task['url'], task['price'], stock))
    fret = format_price(ret)
    return fret