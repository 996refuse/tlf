#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

catsburl = 'http://www.360kxr.com'
def cats_parser(url, content, rule):
    t = etree.HTML(content)
    return [catsburl+i for i in t.xpath(rule) ]

pagerburl = 'http://www.360kxr.com/category/'
re_cat = re.compile("(?<=category/)[0-9]+(?=-)")
def pager(task, rule):
    bpath = '-1-4-2-2-0,999999-all-9-all-all-all-'
    cat = re_cat.search(task['url'])

    t = etree.HTML(task['text'])
    pagenum = t.xpath(rule)

    ret = []

    if not cat:
        log_with_time("bad response %r" % task['url'])
        return ret

    cat = cat.group()

    if not pagenum:
        pagenum = 1
    else:
        pagenum = int(re.search("\d+", pagenum[0].text).group())
    ret.append(task['url'])
    for i in range(2, pagenum+1):
        ret.append(pagerburl + cat + bpath + str(i) + '.html')
    return ret

listburl = "http://www.360kxr.com"
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        stock = node.xpath(rule['stock'])
        if not gid:
            log_with_time("bad response %r"%task['url'])
            continue
        if stock:
            stock = 1
        else:
            stock = 0
        ret.append((listburl+gid[0], stock))
    pdb.set_trace()
    return ret

def test_list(res):
    assert(res[0][1])

def price_parser(task, rule):
    t = etree.HTML(task["text"])
    price = t.xpath(rule['kxrprice'])
    ret = []
    if not price:
        log_with_time("bad response %r" % task['url'])
        return ret
    price = price[0].text
    ret = [(task['url'], price, task['stock'])]
    fret = format_price(ret)
    return fret