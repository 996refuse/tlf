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
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.attrib['itemid']
        stock = node.xpath("div[@class='buyInfo']/button[@class='buy']")
        if not gid:
            log_with_time("bad response: %r"%task['url'])
            continue
        if stock:
            stock = 1
        else:
            stock = 0
        ret.append((gid, stock))
    return ret

def price_parser(task, rule):
    try:
        price = re.search("(?<=price\:)\d+\.\d+(?=\,)", task['text']).group()
    except:
        log_with_time("bad response: %r"%task['url'])
        return []
    ret = [(task['gid'], price, task['stock'])]
    fret = format_price(ret)
    return fret
