#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def boot_parser(burl, content, rule):
    if 'www.yundun.cn' in content:
        urlexprs = re.search("(?<=\">).+(?=window)", content).group()
        urlexprs = urlexprs.replace("var", "")
        exec urlexprs
        return [burl + url]
    return [burl]

def cats_parser(task, rule):
    t = etree.HTML(task['text'])
    ret = t.xpath(rule)
    return ret

def pager(task, rule):
    burl = task['url'][:-1]
    t = etree.HTML(task['text'])
    lastpage = t.xpath(rule)

    ret = []

    if not lastpage:
        pagenum = 1
    else:
        lastpage = lastpage[0]
        pagenum = int(re.search("\d+", lastpage).group())

    for i in range(1, pagenum+1):
        ret.append(burl + '-search-page-' + str(i) + '.htm')
    return ret

def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("p/a/@href")
        price = node.xpath("p/em/@title")
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            continue
        ret.append((gid[0], price[0]))
    return ret

def stock_parser(task, rule):
    try:
        j = json.loads(task['text'])
        j = j[0]
    except:
        log_with_time("bad response: %r"%task['url'])
        return []

    info = task['item']

    ret = []

    if j['Success'] == 'True':
        stock = 1
    else:
        stock = 0

    ret.append((info[0], info[1], stock))

    fret = format_price(ret)
    
    return fret
