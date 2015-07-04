from lxml import etree
from spider import log_with_time
from spider import format_price
import re
import time
import json
import pdb 
import traceback


def cats_parser(url, res, rule): 
    try:
        t = etree.HTML(res["text"])
    except:
        traceback.print_exc()
        return 
    urls = t.xpath(rule[0])
    ret = []
    for url in urls:
	    if re.match('/bst.*',url):
	        ret.append(url)
    return ret

def page_parser(task, rule): 
    try:
        t = etree.HTML(task["text"])
    except:
        traceback.print_exc()
        return 

    tot = t.xpath(rule[0]) 
    total = re.findall("/([0-9]+)", "".join(tot))
    if not total:
        log_with_time("rule error: %s" % rule)
        return
    total = int(total[0])
    if total == 1:
    	return [{
				"url": task['url'],
            }]

    bas = t.xpath(rule[1])[0]
    base = re.findall("(^.*page=?)\d*", bas)[0]
    tasks = []
    for i in range(1, total+1): 
        tasks.append({
            "url": "http://www.likeface.com" + base + str(i),
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
        stock = 1
        if not link or not price: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append((str(link[0]), str(price[0][1:]), int(stock)) )
        #print (str(link[0]), str(price[0][1:]), int(stock))
    result = format_price(ret)
    return result 


