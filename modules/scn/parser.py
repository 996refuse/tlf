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
    return [url]

def pager(task, rule):
    burl = task['url']
    tree = etree.HTML(task["text"])
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
        url = node.xpath("dd/a/@href")
        price = node.xpath("dd/a/ul/li[@class='r1']/i[@class='price']")
        if not url or not price:
            log_with_time("list parser err: %r" % task['url'])
            continue
        url = url[0]
        price = price[0].text[1:]
        ret.append((url, price))
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
    ret.append((task['url'], int(float(task['info'])*100), stock))
    fret = format_price(ret)
    return fret