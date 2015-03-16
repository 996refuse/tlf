from lxml import etree
from spider import log_with_time
from spider import format_price
import re
import json
import pdb


def task_filter(x): 
    return {
            "url": x
            }



def page_parser(task): 
    rule = task["rule"]
    t = etree.HTML(task["recv"].getvalue()) 
    ret = t.xpath(rule["rule"]) 
    total = re.findall("/([0-9]+)", "".join(ret)) 
    if not total:
        log_with_time("rule error: %s" % rule["rule"])
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

def list_parser(task): 
    rule = task["rule"]
    content = task["recv"].getvalue() 
    ret = []
    dyn_items = re.findall('({.*?sell_price.*?}),', content) 
    for i in dyn_items:
        try:
            item = json.loads(i)
        except ValueError:
            continue
        link = item_base % item["id"]
        price = item["sell_price"] 
        ret.append((link, price, 1)) 
    t = etree.HTML(content)
    nodes = t.xpath(rule["rule"]) 
    for node in nodes:
        link = node.xpath("div[@class = 'cat-item-pic']/a/@href")
        price = node.xpath("figcaption[@class = 'cat-item-inf']/p/span[@class = 'cat-pire-nub']/text()")
        if not link or not price: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append((link[0], price[0], 1)) 
    result = format_price(ret)
    return result 

