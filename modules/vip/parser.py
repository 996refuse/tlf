from lxml import etree
from spider import log_with_time
from spider import format_price
import re
import time
import json
import pdb 
import traceback


base = "http://category.vip.com/search-1-0-1.html?%s" 

def cats_parser(url, res, rule): 
    content = res['text']
    cats = set()
    for i in rule:
        cats = cats.union(set(re.findall(i, content))) 
    ret = []
    for c in cats:
        ret.append(base % c)
    return ret


def meizhuang_cats_parser(url, content, rule): 
    t = etree.HTML(content) 
    ret = []
    for node in t.xpath(rule[0]):
        #link
        link = node.xpath(rule[1])
        #price
        price = node.xpath(rule[2]) 
        if not link or not price:
            log_with_time("rule error: %s" % url)
        ret.append((link[0], price[0], 1))
    result = format_price(ret)
    return result


def page_parser(task, rule): 
    try:
        t = etree.HTML(task["text"])
    except:
        traceback.print_exc()
        return 
    ret = t.xpath(rule) 
    total = re.findall("/([0-9]+)", "".join(ret)) 
    if not total:
        log_with_time("rule error: %s" % rule)
        return
    total = int(total[0])
    url = task["url"]
    tasks = []
    for i in range(1, total+1): 
        tasks.append({
            "url": url.replace("1.html", "%s.html" % i), 
            })
    return tasks
    

item_base = "http://www.vip.com/detail-0-%s.html" 


def list_parser(task, rule): 
    ret = [] 
    dyn_items = re.findall('({.*?sell_price.*?}),', task["text"]) 
    dps = []
    for i in dyn_items:
        try:
            item = json.loads(i)
        except ValueError:
            continue
        link = item_base % item["id"]
        dps.append((link, ""))
        price = item["sell_price"] 
        ret.append((link, str(price), 1)) 
    try:
        t = etree.HTML(task["text"])
    except:
        traceback.print_exc()
        return 
    nodes = t.xpath(rule["node"])
    for node in nodes:
        link = node.xpath(rule["link"])
        price = node.xpath(rule["price"])
        if not link or not price: 
            log_with_time("rule error: %s" % task["url"])
            continue
        dps.append((link[0], "")) 
        ret.append((link[0], price[0], 1)) 
    result = format_price(ret)
    now = int(time.time())
    dps_log = {}
    for i in result:
        dps_log[i[1]] = now
    return {
            "spider": result ,
            "dp": dps,
            "dps_log": dps_log,
            }
