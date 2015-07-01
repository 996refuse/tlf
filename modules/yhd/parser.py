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

listurl = "http://list.yhd.com/%s"

def cats_parser(url, res,  rule): 
    content = res['text']
    t = etree.HTML(content) 
    items = t.xpath(rule) 
    ret = set()
    for v in items: 
        url = re.findall("/(v?c[0-9]+-[0-9]+-[0-9]+)/", v) 
        if url:
            ret.add(listurl % url[0]) 
    return ret


parta_base = "http://list.yhd.com/searchPage/{cat}/b/a-s1-v4-p{page}-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp{cb}&&isLargeImg=1"

partb_base = "http://list.yhd.com/searchPage/{cat}/b/a-s1-v4-p{page}-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp{cb}&?isGetMoreProducts=1&isLargeImg=1"

virta_base = "http://list.yhd.com/searchVirCateAjax/{cat}/b/a-s1-v4-p{page}-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp{cb}&&isLargeImg=1"

virtb_base = "http://list.yhd.com/searchVirCateAjax/{cat}/b/a-s1-v4-p{page}-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp{cb}&?isGetMoreProducts=1&isLargeImg=1"



def pager(task, rule):
    try:
        tree = etree.HTML(task["text"])
    except:
        log_with_time("bad response %s" % task['url'])
        return 
    page = re.findall("/([0-9]+)", " ".join(tree.xpath(rule)))
    if not page:
        log_with_time("page rule error")
        return 
    cat = re.findall("/(v?c[0-9]+-[0-9]+-[0-9]+)", task["url"])[0] 
    ret = [] 
    for i in range(1, int(page[0]) + 1):
        if cat.startswith("vc"):
            url_a = virta_base.format(cat = cat, page=i, cb = int(time.time() * 1000)) 
            url_b = virtb_base.format(cat = cat, page=i, cb = int(time.time() * 1000)) 
        else:
            url_a = parta_base.format(cat = cat, page=i, cb = int(time.time() * 1000)) 
            url_b = partb_base.format(cat = cat, page=i, cb = int(time.time() * 1000))
        ret.append(url_a)
        ret.append(url_b) 
    return ret

def list_test(items):
    pdb.set_trace()

dp_base = "http://item.yhd.com/item/%s" 

def list_parser(task, rule): 
    try:
        j = jsonp_json(task["text"].decode("utf-8"))
        t = etree.HTML(j['value'])
    except Exception as e:
        import traceback
        traceback.print_exc() 
        exit(1)
    ret = []
    dps = {}
    dp = []
    comments = {}
    shop = {}
    #dp, comment, shopid, price
    nodes = t.xpath(rule['node']) 
    now = int(time.time()) 
    for node in nodes: 
        price = node.xpath(rule["price"]) 
        if not price:
            log_with_time("price rule error: %s" % task["url"])
            continue
        price = price[0]
        gid = re.findall("_([0-9]+)", node.attrib["id"])[0] 
        comment = node.xpath(rule["comment"]) 
        if comment: 
            comments[gid] = re.findall("\d+", "".join(comment))[0]
        shop_link = node.xpath(rule["shop"]) 
        if shop_link: 
            shop_link = shop_link[0]
            store_id = re.findall("/m-([0-9]+)\.", shop_link.attrib.get("href"))[0] 
            shop[gid] = "%s,%s" % (store_id, shop_link.attrib.get("title")) 
        ret.append((gid, price))
        dps[gid] = now
        pmids = node.xpath(rule["link"])
        if not pmids:
            log_with_time("dp rule error: %s" % task["url"])
            continue
        dp.append((dp_base % pmids[0], gid, "")) 
    return {
            "stock":ret,
            "dps":dps,
            "comment": comments,
            "shop": shop,
            "dp": dp,
            } 


def stock_parser(task, rule):
    try:
        j = json.loads(task["text"])
    except ValueError:
        log_with_time("json error: %s, %s" % (task["url"],task["text"]))
        return
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
