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
    t = etree.HTML(content)
    return ["http://www.m6go.com" + i for i in t.xpath(rule)]

def pager(task, rule):
    burl = task['url']
    t = etree.HTML(task['text'])
    pagenum = t.xpath(rule)

    ret = []

    if not pagenum:
        pagenum = 0
    else:
        pagenum = int(re.search("\d+", pagenum[0]).group())

    for i in range(0, pagenum+1, 36):
        ret.append(burl + '/' + str(i))
    return ret

def list_parser(task, rule):
    burl = "http://www.m6go.com/product_"
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.attrib["goodsid"]
        price = node.attrib['price'][1:]
        ret.append((burl+gid+'.html', price))
    return ret

def stock_parser(task, rule):
    t = etree.HTML(task["text"])
    price = task["price"]
    stock = t.xpath(rule['stock'])
    ret = []
    if not stock:
        log_with_time("bad response %r" % task['url'])
        return ret
    stock = stock[0]
    stock = re.search("\d+", stock.text)
    if stock:
        stock = 1
    else:
        stock = 0
    ret = [(task['url'], price, stock)]
    fret = format_price(ret)
    return fret