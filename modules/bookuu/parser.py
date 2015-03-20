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
        node = node.replace(".html", '-p_')
        ret += [node + str(i) + '.html' for i in range(1, 51)]
    return ret

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("h3/a/@href")
        price = node.xpath("div/p/b")
        stock = node.xpath("div/div/a[1]/@class")
        
        if not gid or not price or not stock:
            log_with_time("bad response: %r" % task['url'])
            return ret
        gid = gid[0]
        price = re.search("\d+\.\d+|\d+", price[0].text).group()
        if "getCart" in stock[0]:
            stock = 1
        else:
            stock = 0
        ret.append((gid, price, stock))
    pdb.set_trace()
    format_price(ret)
    return ret