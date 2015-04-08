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
    burl = "http://www.bookschina.com"
    t = etree.HTML(content)
    ret = [burl + i for i in t.xpath(rule)]

    # a bug from www.bookschina.com
    # 2015/03/19
    if 'kinderwj' in ret[-1]:
        ret[-1] = burl + '/kinder/' + re.search("\d+", ret[-1]).group() +'/'

    return ret

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
        ret.append(burl + '_5_1_' + str(i) + '/')
    return ret

listburl = "http://www.bookschina.com"
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("div[@class='wordContent']/a[@class='titlein']/@href")
        price = node.xpath("div[@class='wordContent']/span")
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = gid[0]
        price = price[0].text
        price = re.search("\d+\.\d+", price).group()
        ret.append((listburl+gid, price, 1))
    pdb.set_trace()
    fret = format_price(ret)
    pdb.set_trace()
    return fret