#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def pager(task, rule):
    burl = 'http://list.mi.com/accessories/ajaxView/0-0-0-0-'
    rr = re.search("items\(", task['text'])

    j = json.loads(task['text'][rr.end():-1])

    ret = []

    if not 'data' in j:
        log_with_time("bad response: %r" % task['url'])
        return ret
    
    pagenum = int(j['data']['total_pages'])

    for i in range(1, pagenum+1):
        ret.append(burl + str(i) + '-0')

    return ret

def list_parser(task, rule):
    ret = []
    rr = re.search("items\(", task['text'])
    if not rr:
        log_with_time("bad response: %r" % task['url'])
        return ret

    j = json.loads(task['text'][rr.end():-1])

    if not 'data' in j:
        log_with_time("bad response: %r" % task['url'])
        return ret

    for i in j['data']['product']:
        stock = i['is_cos']
        if stock:
            stock = 0
        else:
            stock = 1
        price = i['price_min']
        if not price:
            log_with_time("bad response: %r %r" % (task['url'], i['commodity_id']))
            continue

        ret.append((i['url'], price, stock))

    fret = format_price(ret)
    return fret