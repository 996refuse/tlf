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
    burl = 'http://www.360kxr.com'
    t = etree.HTML(content)
    return [ burl+i for i in t.xpath(rule) ]

def pager(task, rule):
    burl = 'http://www.360kxr.com/category/'
    bpath = '-1-4-2-2-0,999999-all-9-all-all-all-'
    rr = re.search("(?<=category/)[0-9]+(?=-)", task['url'])

    t = etree.HTML(task['text'])
    pagenum = t.xpath(rule)

    ret = []

    if not rr:
        log_with_time("bad response %r" % task['url'])
        return ret

    cat = rr.group()

    if not pagenum:
        pagenum = 1
    else:
        pagenum = int(re.search("\d+", pagenum[0].text).group())

    for i in range(1, pagenum+1):
        ret.append(burl + cat + bpath + str(i) + '.html')
    return ret

def list_parser(task, rule):
    burl = "http://www.360kxr.com"
    t = etree.HTML(task['text'])
    nodes = [ burl + i for i in t.xpath(rule) ]
    return nodes

def stock_parser(task, rule):
    t = etree.HTML(task["text"])
    price = t.xpath(rule['kxrprice'])
    out_of_stock = re.search("(?<=isRX:).+(?=,)", task['text'])
    ret = []
    if not price or not out_of_stock:
        log_with_time("bad response %r" % task['url'])
        return ret
    out_of_stock = int(out_of_stock.group())
    if not out_of_stock:
        stock = 1
    else:
        stock = 0
    price = price[0].text
    ret = [(task['url'], price, stock)]
    fret = format_price(ret)
    return fret