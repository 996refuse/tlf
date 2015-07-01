#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

reqburl = 'http://list.mi.com/accessories/ajaxView/0-0-0-0-'

def cats_parser(url, res, rule):
    return [reqburl + '0-0']

def pager(task, rule):
    rr = re.search("items\(", task['text'])

    j = json.loads(task['text'][rr.end():-1])

    ret = []

    if not 'data' in j:
        log_with_time("bad response: %r" % task['url'])
        return ret

    pagenum = int(j['data']['total_pages'])

    for i in range(1, pagenum+1):
        ret.append(reqburl + str(i) + '-0')

    return ret

def list_parser(task, rule):
    ret = []

    dps = []
    rr = re.search("items\(", task['text'])
    if not rr:
        log_with_time("bad response: %r" % task['url'])
        return ret

    j = json.loads(task['text'][rr.end():-1])

    if not 'data' in j:
        log_with_time("bad response: %r" % task['url'])
        return ret

    for i in j['data']['product']:
        if not i['is_cos']:
            stock = 1
        else:
            stock = 0
        price = i['price_min']
        if not price:
            log_with_time("bad response: %r %r" % (task['url'], i['commodity_id']))
            continue
        dps.append((i["url"], ""))
        ret.append((i['url'], price, stock))

    fret = format_price(ret)
    return {
            "spider": fret,
            "dp": dps
            }
