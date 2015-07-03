from lxml import etree
from spider import log_with_time
from spider import format_price
import re
import time
import json
import pdb 
import traceback


def cats_parser(url, res, rule): 
    content = res['text']
    catsInt = []
    for i in rule:
	    catsInt += re.findall(i, content)
    return catsInt

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

    tasks = []
    for i in range(1, total+1): 
        tasks.append({
            "url": "http://www.tootoo.cn/list-s1-"+str(task['catsInt'])+"-0-0-0-0-0-"+str(i)+"-0-0-0-1,2,3,0-zh_cn.html", 
            })
    return tasks

  
def list_parser(task, rule): 
    try:
        t = etree.HTML(task["text"])
    except:
        traceback.print_exc()
        return 

    ret = []
    nodes = t.xpath(rule["node"])
    #print etree.tostring(nodes[0])
    #print len(nodes)
    for node in nodes:

        link  = node.xpath(rule["link"])
        price = node.xpath(rule["price"])
        stock = "none" in str(node.xpath(rule["stock"])[0])
        if not link or not price: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append((str(link[0]), str(price[0][1:]), int(stock)) )
        #print (str(link[0]), str(price[0][1:]), int(stock))
    result = format_price(ret)
    return result 


