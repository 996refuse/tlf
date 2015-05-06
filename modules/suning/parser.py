#-*-encoding=utf-8-*-

from lxml import etree
import re
import os
import time 
from spider import log_with_time 
from spider import async_http 
from spider import format_price
from spider import fix_price
import _tess
import pdb 
import spider
import getpass


_tess.set_config({
"datadir": "/home/%s/project/tess-build/bin" % getpass.getuser(),
"lang": "eng"})


site_id = 25

def set_id(rule): 
    global site_id
    site_id = spider.CONFIG["site_id"]

city_table = {
        25: 9173,
        1025: 9017,
        2025: 9041,
        3025: 9265
        } 

district_table = {
        25: 10106,
        1025: 11305,
        2025: 10278,
        3025: 12134
        } 


invalid_cats = set((u"电影", u"食品酒水", u"商品团", u"婚庆", u"丽人", u"生活", u"娱乐", u"美食"))


def cats_parser(url, content, rule): 
    x = etree.HTML(content)
    n = x.xpath(rule) 
    ret = [] 
    city_id = str(city_table[site_id])
    for i in n:
        href = i.attrib["href"].encode("utf-8") 
        url_parts = re.findall("/[0-9]-[0-9]+-[0-9]-[0-9]-[0-9]-[0-9]+",
                href) 
        if url_parts and not city_id in href: 
            continue
        if i.attrib.get("title") in invalid_cats:
            continue 
        #过滤多余的分类
        if not "list.suning" in href: 
            continue 
        if "/0-500" in href:
            continue 
        if "_" in href:
            continue
        ret.append((fix_url(href), i.text.encode("utf-8"))) 
    url_filter = {} 
    for url,n in ret: 
        if url in url_filter: 
            continue
        else:
            url_filter[url] = n 
    return url_filter.keys() 


def test_cats_parser(args): 
    pdb.set_trace()



def fix_url(origin): 
    origin = origin.replace("0-1-0", "0-0-0")
    #不是旧版url不处理
    if not re.findall("/[0-9]-[0-9]+-0\.", origin): 
        return origin 
    #添加城市编号
    url = origin.replace(".html", "-0-0-%s.html" % city_table[site_id])
    return url



def pager(task, rule): 
    url = task["url"] 
    cat = re.findall("/[0-9]-([0-9]{1,10})-", url)[0] 
    tree = etree.HTML(task["text"]) 
    if cat.startswith("26"): 
        count =  tree.xpath(rule["book_a"]) 
        if not count:
            count = tree.xpath(rule["book_b"]) 
        page = int(count[0].split("/")[-1])
    else: 
        count = tree.xpath(rule["normal"])
        if not count:
            page = 1 
        else:
            page = int(count[0]) 
        if page > 90:
            log_with_time("need split page: %s" % url)
    log_with_time("%s: %d" % (task["url"], page)) 
    cats = re.findall("/([0-9]-[0-9]+-)([0-9]+)", url) 
    if not cats:
        log_with_time("url format error: %s" % url)
        return
    cats, pg = cats[0]
    old_cats = cats + str(pg)
    ret = []
    for i in range(page):
        ret.append(url.replace(old_cats, cats + str(i)))
    return ret 



def list_test(items):
    pdb.set_trace() 


suning_p_base = "http://product.suning.com/%s.html"


def extract_normal(url, tree, rule): 
    result = []
    dps = [] 
    now = int(time.time())
    dps_log = {} 
    nodes = tree.xpath(rule["normal_node"]) 
    for node in nodes: 
        title = node.xpath(rule["normal_title"]) 
        p_img = node.xpath(rule["normal_price"])
        stock = node.xpath(rule["normal_stock"]) 
        if not title or not p_img or not stock: 
            log_with_time("rule error: %s" % url)
            continue 
        if u"有货" in stock[0]:
            s = 1
        else:
            s = 0
        qids = node.xpath(rule["qid"]) 
        for qid in qids: 
            link = suning_p_base % qid.attrib["name"]
            q = qid.attrib["val"] 
            dps_log[q] = now
            dps.append((link, q, title[0])) 
            result.append((link, q, p_img[0], s))
        if not qids:
            qid = node.attrib["class"].split(" ")[0]
            link = suning_p_base % int(node.attrib["name"])
            dps_log[qid] = now 
            dps.append((link, qid, title[0]))
            result.append((link, qid, p_img[0], s))
    return {
            "price": result,
            #"dp": dps,
            "dps_log": dps_log
            } 


def extract_book(url, tree, rule): 
    result = []
    dps = [] 
    now = int(time.time())
    dps_log = {} 
    nodes = tree.xpath(rule["book_node"]) 
    for node in nodes:
        qid = node.attrib["class"].split(" ")[0] 
        link_node = node.xpath(rule["book_title"]) 
        stock = node.xpath(rule["book_stock"]) 
        price = node.xpath(rule["book_price"])
        if not link_node or not stock or not price: 
            log_with_time("rule error: %s" % url)
            continue 
        link_node = link_node[0]
        link = link_node.attrib["href"]
        title = link_node.text
        if u"有货" in stock[0]:
            s = 1
        else:
            s = 0 
        dps_log[qid] = now
        dps.append((link, qid, title))
        result.append((link, qid, price[0], s)) 
    return {
            "price": result,
            #"dp": dps,
            "dps_log": dps_log,
            } 



def list_parser(task, rule): 
    tree = etree.HTML(task["text"].decode("utf-8")) 
    if not re.findall("/[0-1]-26", task["url"]):
        return extract_normal(task["url"], tree, rule)
    else:
        return extract_book(task["url"], tree, rule) 



def price_parser(task, rule):
    price = _tess.recognize(task["text"], _tess.IMAGE_PNG, 32)
    p = fix_price(price)
    if not p:
        log_with_time("no price: %s" % task["link"]) 
        return 
    log_with_time("%s %s %d" % (task["link"], p, task["stock"]))
    ret = [(task["qid"], p, task["stock"])] 
    return format_price(ret) 
    

