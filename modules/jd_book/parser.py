#-*-encoding=utf-8-*-
from lxml import etree
from spider import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import time

#http://list.jd.com/list.html?cat=670,671,672
#http://list.jd.com/670-677-678.html

book_base = "http://list.jd.com/list.html?cat=%s&area=1,72,4137&page=%s&delivery=0&stock=0&sort=sort_winsdate_desc&JL=4_6_0"


old_url_pat = re.compile("([0-9-]+)\.")

def cats_parser(url, content, rule): 
    tree = etree.HTML(content.decode("gbk"))
    links = tree.xpath(rule)
    ret = [] 
    for link in links:
        l = link.attrib["href"] 
        cat = old_url_pat.findall(l)[0].replace("-",",")
        ret.append(book_base.format(cat, 0))
    return ret


book_base = "http://list.jd.com/list.html?cat={0}&area=1,72,4137&page={1}&delivery=0&stock=0&sort=sort_winsdate_desc&JL=4_6_0"


def pager(task, rule): 
    tree = etree.HTML(task["text"]) 
    count = tree.xpath(rule["book"]) 
    if count:
        count = int(count[0])
    else: 
        log_with_time("pager, no count: %s" % task["url"])
        return 
    if count > 450:
        log_with_time("need split page: %s" % task["url"]) 
    ret = []
    #图书的翻页不同 
    cats = re.findall("cat=([0-9,]+)&", task["url"]) 
    if not cats:
        log_with_time("pager, no cats: %s" % task["url"])
        return
    price_range = re.findall("(ev=.*%40)", task["url"])
    if price_range: 
        base = "%s&%s" % (book_base, price_range[0])
    else:
        base = book_base
    cat = cats[0].replace("-", ",")
    for i in range(1, count+1):
        ret.append(base.format(cat, i))
    return ret 


def test_list(items):
    pdb.set_trace()

dp_base = "http://item.jd.com/%s.html" 

def list_parser(task, rule): 
    tree = etree.HTML(task["text"])
    nodes = tree.xpath(rule["book"]) 
    prices = []
    dps = []
    dps_log = {}
    now = int(time.time()) 
    for node in nodes: 
        sku = node.attrib.get("data-sku")
        title = node.xpath(rule["title"]) 
        if not title:
            title = [""]
        if sku:
            dps_log[sku] = now 
            dps.append((dp_base % sku, title[0].strip("\r\n ")))
            prices.append(sku)
    return {
            "dps_log": dps_log,
            "dp": dps,
            "price": prices
            }


def price_parser(task, rule): 
    try:
        items = jsonp_json(task["text"])
    except ValueError as e:
        log_with_time("price_parser: jsonp_json: %s" % task["text"]) 
        return 
    d = {}
    for item in items:
        d[item["id"].split("_")[1]] =  item["p"]
    return [d] 



def stock_parser(task, rule): 
    try:
        stock = jsonp_json(task["text"].decode("gbk"))
    except ValueError as e:
        log_with_time("stock_parser: jsonp_json: %s" % task["text"])
        return 
    stocks = {} 
    for key,value in stock.items():
        s = value["StockStateName"] 
        if u"现货" in s or u"有货" in s: 
            stocks[key] = 1
        else: 
            stocks[key] = 0 
    ret = [] 
    prices = task["price"]
    for key,price in prices.items():
        if key not in stocks:
            log_with_time("key not in stocks: %s" % task["url"])
            continue
        ret.append((key, price, stocks[key])) 
    result = format_price(ret)
    return result 
