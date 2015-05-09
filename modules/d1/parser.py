#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import demjson
import time

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

surl1 = "http://www.d1.com.cn/ajax/flow/listInCart.jsp"
re_gid = re.compile("(?<=product/)\d+")
re_price = re.compile("\d+")
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes'])
    ret = []
    dps = {}
    for node in nodes:
        gid = node.xpath(rule['gid'])
        price = node.xpath(rule['price'])
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            continue
        gid = re_gid.search(gid[0]).group()
        price = re_price.search(price[0].text).group()
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
        dps[gid] = time.time()
    return {"stock": ret, "dps": dps}

surl2 = lambda g,s: 'http://m.d1.cn/ajax/flow/InCartnew.jsp?gdsid=%s&count=1&skuId=%s'%(g,s)
def stock1_parser(task, rule):
    try:
        j = demjson.decode(task['text'])
    except:
        log_with_time("bad response: %r"%task['url'])
        return []
    code = j['code']
    message = j['message']

    url = ""
    ret = {"spider":[], 'stock2':[]}

    if code == 3 and message:
        try:
            skuid = re.search("\d+", message).group()
            url = surl2(task['gid'], skuid)
        except:
            return []
    if url == "":
        #print(task['text'])
        stock = 1 if j.get('totalAmount') else 0
        ret['spider'] = format_price([(itemurl+task['gid'], task['price'], stock)])
    else:
        ret['stock2'] = [(url, task['gid'], task['price'])]

    return ret

itemurl = 'http://www.d1.com.cn/product/'
def stock2_parser(task, rule):
    success = re.search("(?<=success\":).+(?=,)", task['text'])

    if success and success.group() == 'true':
        stock = 1
    else:
        stock = 0

    ret = [(itemurl%task['gid'], task['price'], stock)]
    fret = format_price(ret)
    return fret
