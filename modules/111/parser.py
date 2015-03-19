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
    ret = t.xpath(rule)

    return ret

def pager(task, rule):
    burl = task['url'][:-6]
    t = etree.HTML(task['text'])

    pagenum = t.xpath(rule)

    ret = []

    if not pagenum:
        pagenum = 1
    else:
        pagenum = int(pagenum[0])

    for i in range(1, pagenum+1):
        ret.append(burl + str(i) + '.html')
    return ret

def list_parser(task, rule):
    burl = "http://www.111.com.cn/product/"
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.attrib['itemid']
        if not gid:
            log_with_time("bad response: %r"%task['url'])
            return ret
        ret.append((burl+gid+'.html',gid))
    return ret

def price_parser(task, rule):
    try:
        price = re.search("(?<=price\:)\d+\.\d+(?=\,)", task['text']).group()
    except:
        log_with_time("bad response: %r"%task['url'])
        return []
    ret = [(task['gurl'], price)]
    return ret

def stock_parser(task, rule):
    t = etree.HTML(task['text'])
    ostock = t.xpath(rule)
    if ostock:
        stock = 0
    else:
        stock = 1
    ret = [(task['url'], task['price'], stock)]
    fret = format_price(ret)
    return fret