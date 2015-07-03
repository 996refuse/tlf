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

burl = "http://www.zhiwo.com"
def cats_parser(url, res, rule):
    content = res['text']
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

re_price = re.compile("\d+\.\d+")
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        price = node.xpath(rule['price'])
        stock = node.xpath(rule['stock'])
        if not gid or not price or not stock:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = burl + gid[0]
        price = re_price.search(price[0].text).group()
        stock = stock[0]
        if stock.find("add_to_cart"):
            stock = 1
        else:
            stock = 0
        ret.append((str(gid), str(price), stock))
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result":fret, "dps":dps}
