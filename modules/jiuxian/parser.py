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
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("div/a[@class='proName']/@href")
        ostock = node.xpath("div/a[contains(@class, 'lack')]")
        if not gid:
            log_with_time("bad response: %r" % task['url'])
            return ret
        gid = re.search("\d+", gid[0]).group()
        if not ostock:
            stock = 1
        else:
            stock = 0
        ret.append((gid, stock))
    return ret

def price_parser(task, rule):
    gurl = lambda g: "http://www.jiuxian.com/goods-%s.html" % g
    j = json.loads(task['text'])
    stocks = task['stock']
    
    ret = []

    try:
        for k,v in j['data'].items():
            ret.append((gurl(k), v['np'], stocks[k]))
    except:
        return []
    
    format_price(ret)
    
    return ret