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
    burl = task['url']
    t = etree.HTML(task['text'])
    lastpage = t.xpath(rule)

    ret = []

    if not lastpage:
        pagenum = 1
    else:
        lastpage = lastpage[0]
        pagenum = int(re.search("(?<=pageno\=)\d+", lastpage).group())

    for i in range(1, pagenum+1):
        ret.append(burl + '&pageno=' + str(i))
    return ret

def list_parser(task, rule):
    surl1 = "http://www.d1.com.cn/ajax/flow/listInCart.jsp"
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("div[@class='g_title']/span/a/@href")
        price = node.xpath("div[@class='g_price']/span/font")
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            return ret
        gid = re.search("(?<=product/)\d+", gid[0]).group()
        price = re.search("\d+", price[0].text).group()
        ret.append({
            "url": surl1,
            "gid": gid,
            "price": price,
            "payload": {
                "id": gid,
                "type": "0",
                "count": "1"
            }
        })
    return ret

def stock_parser(task, rule):
    surl2 = lambda g,s: 'http://m.d1.cn/ajax/flow/InCartnew.jsp?gdsid=%s&count=1&skuId=%s'%(g,s)
    code = re.search("(?<=code\"\:)\d+(?=,)", task['text'])
    message = re.search('(?<=message).+(?=\")', task['text'])
    success = re.search("(?<=success\":).+(?=,)", task['text'])

    url = ""
    stock = 0

    if code:
        code = int(code.group())
        if code == 0:
            stock = 1
        elif code == 3:
            if message:
                try:
                    skuid = re.search("\d+", message.group()).group()
                    url = surl2(task['gid'], skuid)
                except:
                    return []

    if success and success.group() == 'true':
            stock = 1
    
    if url:
        return [(url, (task['gid'], task['price']))]

    ret = [(task['gid'], task['price'], stock)]

    fret = format_price(ret)
    return fret