#-*-encoding=utf-8-*-
import lxml
from lxml import etree
from spider import async_http
from spider import log_with_time
import lxml
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json
import time

cookie_table = {
        31: 5,
        1031: 2,
        2031: 20,
        3031: 18,
        4031: 12
        }


lsturl = "http://list.yhd.com/%s-0-0"
ctgurl = "http://www.yhd.com/ctg/s2/%s-0-0"

def cats_parser(url, content,  rule):
    t = etree.HTML(content)
    ret = set()
    items = t.xpath(rule)
    for v in items:
        #pdb.set_trace()
        if '/c0-0/' in v:
            continue
        if '/ctg/s2/' in v:
            r = "(?<=/ctg/s2/).+"
            cat = re.search(r, v)
            if not cat:
                log_with_time("bad regex: %r %r" % (r, v))
                continue
            cat = cat.group().split('-')[0]
            ret.add(ctgurl % cat)
        elif 'list.yhd.com' in v:
            # http://list.yhd.com/.../
            r = "(?<=yhd\.com\/).+"
            cat = re.search(r, v)
            if not cat:
                log_with_time("bad regex: %r %r" % (r, v))
                continue
            cat = cat.group().split('-')[0]
            ret.add(lsturl % cat)
    return ret

pgburl = 'http://list.yhd.com/%s/b/a-s1-v0-p%s-price-d0-f0-m1-rt0-pid-mid0-k'
def pager(task, rule):
    try:
        tree = etree.HTML(task["text"])
    except:
        log_with_time("bad response %s" % task['url'])
        return []

    sspage = tree.xpath(rule)
    ret = []
    if not sspage:
        log_with_time("rule error:%s %s"%(rule, task['url']))
        return []
    try:
        cats, count = sspage
    except:
        log_with_time("rule error:%s %s"%(rule, task['url']))
        return []

    cats = cats.xpath("a[2]/@url")[0]
    if cats == '0': cats = 'searchPage/' + task['url'].split('/')[-1]
    else: cats = re.search("(?<=yhd\.com\/).+(?=\/b)", cats).group()

    try:
        count = int(re.search("(?<=/)\d+", etree.tostring(count)).group())
    except:
        count = 1
    for i in range(1, count+1):
        ret.append(pgburl%(cats, str(i)))
    return ret


re_price = re.compile("(?<=b\>)\d+\.\d+|(?<=b\>)\d+")
re_pid = re.compile("\d+")
def list_parser(task, rule):
    #pr.enable()
    try:
        j = json.loads(task["text"].decode("utf-8"))
        t = etree.HTML(j['value'])
    except:
        log_with_time("bad response: json decode error %s"%task['url'])
        return []
    ret = []
    dps = {}
    nodes = t.xpath(rule['nodes1'])
    if not nodes:
        nodes = t.xpath(rule['nodes2'])
        if not nodes:
            log_with_time("bad rules %s"%task['url'])
            return []
        price_rule = rule['price2']
    else:
        price_rule = rule['price1']
    for node in nodes:
        pid = re_pid.search(node.attrib['id']).group()
        price_node = node.xpath(price_rule)
        if not pid or not price_node:
            log_with_time("bad rules: %s %s"%(price_rule, task['url']))
            continue
        price_node = price_node[0]
        price = price_node.attrib.get("yhdprice")
        if not price:
            price = price_node.attrib.get("yhdPrice")
        if not price:
            price = price_node
        if type(price) == lxml.etree._Element:
            price = etree.tostring(price)
            price = re_price.search(price)
            if not price:
                log_with_time("bad response %s"%task['url'])
                continue
            price = price.group()
        ret.append((pid, price))
        dps[gid] = time.time()
    #pr.disable()
    #pr.print_stats()
    return {"stock":ret, "dps":dps}




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
    return result
