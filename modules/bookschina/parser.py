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

burl = "http://www.bookschina.com"
def cats_parser(url, res, rule):
    t = etree.HTML(res['text'])
    ret = [burl + i for i in t.xpath(rule)]

    # a bug from www.bookschina.com
    # 2015/03/19
    #if 'kinderwj' in ret[-1]:
    #    ret[-1] = burl + '/kinder/' + re.search("\d+", ret[-1]).group() +'/'

    return ret[:-1]

def test_cats(res):
    assert(len(res) > 30)

def pager(task, rule):
    burl = task['url']
    if burl[-1] == '/':
        burl= burl[:-1]
    t = etree.HTML(task['text'])
    lastpage = t.xpath(rule)

    ret = []

    if not lastpage:
        pagenum = 1
    else:
        pagenum = int(re.search("(?<=_5_1_)\d+(?=/)", lastpage[0]).group())

    for i in range(1, pagenum+1):
        ret.append(burl + '_AA_5_1_' + str(i) + '/')
    return ret

itemurl = "http://www.bookschina.com"
re_price = re.compile("\d+\.\d+")
def list_parser(task, rule):
    t = etree.HTML(task['text'].decode('gbk', 'replace'))
    nodes = t.xpath(rule['nodes'])
    ret = []
    dps = {}

    for node in nodes:
        gid = node.xpath(rule['gid'])
        price = node.xpath(rule['price'])
        if not gid or not price:
            log_with_time("bad rules: %r" % task['url'])
            continue
        gid = gid[0]
        price = price[0].text
        price = re_price.search(price).group()
        ret.append((itemurl+gid, price, 1))
    fret = format_price(ret)
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result":fret, "dps":dps}

def test_list(res):
    assert(res['result'] > 20)