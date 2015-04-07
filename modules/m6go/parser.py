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

gid_html = "http://www.m6go.com/product_%s.html"
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.attrib["goodsid"]
        price = node.attrib['price'][1:]
        ostock = node.xpath("div/input[@class='addCarNone']")
        if not gid or not price:
            log_with_time("bad response %r"%task['url'])
            continue
        if ostock:
            stock = 0
        else:
            stock = 1
        ret.append((gid_html%gid, price, stock))
    fret = format_price(ret)
    return fret