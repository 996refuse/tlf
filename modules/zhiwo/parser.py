#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

burl = "http://www.zhiwo.com"
def cats_parser(url, content, rule):
    t = etree.HTML(content)
    ret = [ burl + i for i in t.xpath(rule) ]

    return ret

def pager(task, rule):
    burl = task['url'].replace(".html", "/")
    t = etree.HTML(task['text'])
    lastpage = t.xpath(rule)

    ret = []

    if not lastpage:
        pagenum = 1
    else:
        lastpage = lastpage[0]
        pagenum = int(lastpage.text)

    for i in range(1, pagenum+1):
        ret.append(burl + str(i) + '.html')
    return ret

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("div/a/@href")
        price = node.xpath("p/span")
        stock = node.xpath("p/a/img/@src")
        if not gid or not price or not stock:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = burl + gid[0]
        price = re.search("\d+\.\d+", price[0].text).group()
        if re.search("add_to_cart", stock[0]):
            stock = 1
        else:
            stock = 0
        ret.append((gid, price, stock))
    fret = format_price(ret)
    return fret