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

    try:
        #pdb.set_trace()
        pagenum = ''.join(t.xpath(rule))
        pagenum = re.search("\d+", pagenum).group()
        pagenum = int(pagenum)
    except:
        pagenum = 1

    ret = []

    for i in range(1, pagenum+1):
        ret.append(burl + str(i) + '.html')
    return ret

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    prices = []
    items = []
    #pdb.set_trace()
    for node in nodes:
        gid = node.attrib['itemid']
        stock = node.xpath(rule['stock'])
        if not gid:
            log_with_time("bad response: %r"%task['url'])
            continue
        if not stock:
            items.append(gid)
        else:
            if stock[0].attrib.get('class') != 'buy':
                stock = 0
            else:
                stock = 1
            prices.append((gid, stock))
    return {"prices": prices, "items": items}

def test_list(res):
    assert(res[0][1])

def item_parser(task, rule):
    try:
        t = etree.HTML(task['text'])
        btn = t.xpath(rule)[0]
        stock = 0 if btn.attrib.get('disabled') else 1
    except:
        log_with_time("bad response: %s"%task['url'])
        return
    return [(task['gid'], stock)]

def price_parser(task, rule):
    try:
        price = re.search("(?<=price\:)\d+\.\d+(?=\,)", task['text']).group()
    except:
        log_with_time("bad response: %r"%task['url'])
        return []
    ret = [(task['gid'], price, task['stock'])]
    fret = format_price(ret)
    return fret
