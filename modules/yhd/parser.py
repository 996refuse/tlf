#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

def cats_parser(url, content,  rule):
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        for v in items:
            if not 'list.yhd.com' in v or '/b/' in v:
                continue
            ret.append(v)
    return ret

pgburl = 'http://list.yhd.com/searchPage/%s/b/a-s1-v0-p%s-price-d0-f0-m1-rt0-pid-mid0-k'
def pager(task, rule): 
    tree = etree.HTML(task["text"])
    count = tree.xpath(rule) 
    if not count:
        count = [1]
    count = int(count[0])
    ret = []
    cat = task['url'].split('/')
    while not cat[-1]:
        cat.pop(-1)
    cat = cat[-1]
    for i in range(1, count+1):
        ret.append(pgburl%(cat, str(i)))
    return ret

def list_parser(task, rule):
    try:
       #pdb.set_trace()
        j = json.loads(task["text"])
        t = etree.HTML(j['value'])
        nodes = t.xpath(rule)
    except:
        log_with_time("bad response %s"%task['url'])
        return []
    ret = []
    for node in nodes:
        pid = re.search("\d+", node.attrib['id']).group()
        price = node.xpath("div/p[@class='proPrice']/em")
        pdb.set_trace()
        if not pid or not price:
            log_with_time("bad response %s"%task['url'])
            continue
        price = etree.tostring(price[0])
        price = re.search("(?<=b\>)\d+\.\d+|(?<=b\>)\d+", price).group()
        ret.append((pid, price))
    return ret

def stock_parser(task, rule):
    j = json.loads(task["text"])
    if not j: 
        log_with_time("bad response: %s" % task["url"])
        return
    ret = []
    for i in j:
        if int(i["localStock"]):
            stock = 1
        else:
            stock = 0
        qid = str(i["productId"])
        ret.append((qid, task['price'][qid], stock))
    result = format_price(ret)
    return fret