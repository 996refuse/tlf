#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def pager_parser(url, content, rule):
    url = 'http://s.vancl.com/p'
    t = etree.HTML(content)
    pagenum = int(re.search("\d+", t.xpath(rule)[0].text).group())
    return [url + str(i) + '.html' for i in range(1, pagenum+1)]

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("p/a/@href")
        price = node.xpath("div/span[@class='Sprice']")
        if not gid or not price:
            log_with_time("bad response %r"%task['url'])
            return ret
        price = re.search("\d+", price[0].text)
        if not price:
            price = node.xpath("div/div[1]")
            if not price:
                log_with_time("bad response %r"%task['url'])
                return []
            price = price[0].text
        else:
            price = price.group()
        ret.append((gid[0], price))
    return ret

def stock_parser(task, rule):
    t = etree.HTML(task['text'])
    if t.xpath(rule):
        stock = 1
    else:
        stock = 0
    ret = [(task['url'], task['price'], stock)]
    fret = format_price(ret)
    return fret