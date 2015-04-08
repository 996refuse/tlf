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
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("p/a/@href")
        price = node.xpath("div/span[@class='Sprice']")
        if not gid or not price:
            log_with_time("bad response %r"%task['url'])
            return ret
        gid = re.search("\d+", gid[0]).group()
        price = re.search("\d+", price[0].text)
        if not price:
            price = node.xpath("div/div[1]")
            if not price:
                log_with_time("bad response %r"%task['url'])
                continue
            price = price[0].text
        else:
            price = price.group()

        ret.append((murl+gid, price))
    return ret

def stock_parser(task, rule):
    if '售罄' in task['text']:
        stock = 0
    else:
        stock = 1
    ret = [(task['url'], task['price'], stock)]
    fret = format_price(ret)
    return fret