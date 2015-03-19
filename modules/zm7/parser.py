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
    burl = "http://www.zm7.cn/"
    t = etree.HTML(content)
    ret = [burl + i for i in t.xpath(rule)]

    return ret

def pager(task, rule):
    # eg: http://www.zm7.cn/category-21-b0-min0-max0-attr0-2-sort_order-ASC.html
    pad = lambda n: "min0-max0-attr0-%d-sort_order-ASC.html" % n
    burl = task['url'][:-5] + '-'
    t = etree.HTML(task['text'])
    pagetxt = t.xpath(rule)

    ret = []
    
    if not pagetxt:
        log_with_time("bad response: %r" % task['url'])
        return ret

    pagetxt = pagetxt[0].text
    pagenum = re.findall("\d+", pagetxt)
    pagenum = int(pagenum[-1])
    for i in range(1, pagenum+1):
        ret.append(burl+pad(i))
    return ret

def payload(gid):
    return json.dumps({
        "quick": 1,
        "spec": [],
        "goods_id": gid,
        "number": 1,
        "parent": 0
    })

def list_parser(task, rule):
    purl = "http://www.zm7.cn/flow.php?step=add_to_cart"
    burl = "http://www.zm7.cn/"
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule)
    ret = []
    for node in nodes:
        gid = node.xpath("a/@href")
        price = node.xpath("p/span")
        if not gid or not price:
            log_with_time("bad response: %r" % task['url'])
            return ret
        gid_html = gid[0]
        gid = re.search("\d+", gid_html).group()
        price = price[0].text
        price = re.search("\d+\.\d+", price).group()
        ret.append({
            "url": purl,
            "info": (burl+gid_html, price),
            "payload": {
                "goods": payload(gid)
            }
        })
    return ret

def stock_parser(task, rule):
    ret = []
    try:
        j = json.loads(task["text"])
    except:
        log_with_time("bad response: %r" % task['url'])
        return ret

    gid = task['info'][0]
    price = task["info"][1]

    if j.get("error"):
        stock = 0
    else:
        stock = 1

    ret = [(gid, price, stock)]
    fret = format_price(ret)
    return fret