from lxml import etree
from spider import log_with_time
from spider import format_price
import re
#import time
#import json
#import pdb 
import traceback
import simple_http

def cats_parser(url, res, rule): 
    try:
        t = etree.HTML(res['text'].decode('gb18030'))
    except:
        traceback.print_exc()
        return 
    return t.xpath(rule[0]) 

def page_parser(task, rule): 
    try:
        t = etree.HTML(task["text"].decode('gb18030'))
    except:
        traceback.print_exc()
        return 

    ret = t.xpath('//li[contains(@class, "page")]/span')
    s = etree.tostring(ret[0])
    total = re.findall("</em>/(\d+?)</span>",s)
    if not total:
        log_with_time("rule error: %s" % rule)
        return
    total = int(total[0])

    tasks = []
    for i in range(1, total+1): 
        tasks.append({
            "url": task['url'][:-4] + "_y"+ str(i) +".htm", 
            })
    return tasks

  
def list_parser(task, rule): 
    try:
        t = etree.HTML(task["text"].decode('gb18030'))
    except:
        traceback.print_exc()
        return 

    nodes = t.xpath(rule["node"])
    
    ret = list()
    for node in nodes:
        link  = node.xpath(rule["link"])
        price = node.xpath(rule["price"])
        stock = 1
        if not link or not price: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append((str(link[0]), str(price[0][1:]), int(stock)) )

        print (str(link[0]), str(price[0][1:]), int(stock))
    result = format_price(ret)
    return result 


