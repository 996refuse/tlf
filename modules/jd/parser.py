#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re

#http://list.jd.com/list.html?cat=670,671,672
#http://list.jd.com/670-677-678.html

base = "http://list.jd.com/list.html?cat=" 

def fix_url(url): 
    #图书类的不能修改
    if "/1713-" in url:
        return url
    x = re.findall("/([0-9\-]+)\.", url)
    if not x:
        return url
    return base + ",".join(x[0].split("-"))


def cats_parser(url, content, rule): 
    t = etree.HTML(content) 
    cats = t.xpath(rule[0])
    ret = []
    for i in cats:
        href = i.attrib["href"]
        if "list.jd" in href:
            url = fix_url(i.attrib["href"].encode("utf-8"))
            ret.append(url)
    return ret 


#http://list.jd.com/list.html?cat=670%2C671%2C672&page=2&JL=6_0_0
#http://list.jd.com/1713-3258-3307.html?s=15&t=1&p=2&JL=6_0_0

normal_base = "http://list.jd.com/list.html?cat=%s&page=%s&JL=6_0_0"
book_base = "http://list.jd.com/%s.html?s=15&t=1&p=%s&JL=6_0_0"


def pager(task, rule): 
    tree = etree.HTML(task["text"])
    count = tree.xpath(rule) 
    if not count:
        log_with_time("pager, no count: %s" % task["url"])
        return 
    #普通商品的翻页
    count = int(count[0]) 
    url = task["url"]
    cats =  re.findall("=([0-9,]+)", url) 
    ret = []
    if cats: 
        for i in range(1, count+1):
            ret.append(normal_base % (async_http.quote(cats[0]), i)) 
        return ret 
    #图书的翻页不同 
    pdb.set_trace()
    cats = re.findall("/([0-9\-]+)\.html", url) 
    if not cats:
        log_with_time("pager, no cats: %s" % task["url"])
        return
    for i in range(1, count+1):
        ret.append(book_base % (cats[0], i))
    return ret



def list_parser(task, rule): 
    tree = etree.HTML(task["text"])
    nodes = tree.xpath(rule["node"])
    ret = []
    for node in nodes:
        if node.attrib.get("data-sku"):
            ret.append(node.attrib["data-sku"]) 
    return ret 


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

        
stock_possible = set([65569, 65570, 65572, 65575, 65576, 1, 0])
stock_true = set([65569, 65575, 65576,  1])


def stock_parser(task, rule): 
    try:
        stock = jsonp_json(task["text"])
    except ValueError as e:
        log_with_time("stock_parser: jsonp_json: %s" % task["text"])
        return 
    stocks = {} 
    for key,value in stock.items():
        s = value["stockvalue"] 
        if s not in stock_possible:
            log_with_time("stock value error: %s, %s" % (key, value))
            continue
        if s in stock_true:
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
