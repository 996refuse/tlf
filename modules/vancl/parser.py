#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

purl = 'http://s.vancl.com/p'
def pager_parser(url, content, rule):
    t = etree.HTML(content)
    pagenum = int(re.search("\d+", t.xpath(rule)[0].text).group())
    return [purl + str(i) + '.html' for i in range(1, pagenum+1)]

murl = 'http://m.vancl.com/style/index/'
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        price = node.xpath(rule['price1'])
        if not gid or not price:
            log_with_time("bad response %r"%task['url'])
            return ret
        gid = re.search("\d+", gid[0]).group()
        price = re.search("\d+", price[0].text)
        if not price:
            price = node.xpath(rule['price2'])
            if not price:
                log_with_time("bad response %r"%task['url'])
                continue
            price = price[0].text
        else:
            price = price.group()

        ret.append((murl+gid, price))
    return ret

def stock_parser(task, rule):
    t = etree.HTML(task['text'])
    s = etree.tostring(t)
    if '售罄' in s:
        stock = 0
    else:
        stock = 1
    ret = [(task['url'], task['price'], stock)]
    fret = format_price(ret)
    return fret