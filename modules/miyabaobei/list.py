#-*-encoding=utf-8-*-
import pdb
import json
from spider import format_price
from spider import log_with_time

from lxml import etree 


def task_filter(x): 
    return {
            "url": x,
            } 


"""
http://www.miyabaobei.com/search/s?tid=372&cat=84&order=normal&sort=desc&per_page=40
"""

def pager(task): 
    rule = task["rule"]
    content = task["recv"].getvalue() 
    t = etree.HTML(content) 
    total = t.xpath(rule["rule"])
    if "找到0个商品" in content:
        log_with_time("search result 0: %s" % task["url"]) 
        return
    if not total:
        log_with_time("rule error: %s" % rule["rule"])
        return
    total = int(total[0])   
    page = rule["page"]
    num = total / page
    if total % page:
        num += 1 
    tasks = []
    for i in range(num):
        tasks.append(
            {
            "url": task["url"] + "&order=normal&sort=desc&per_page=%s" % (i * page),
            "old_url": task["url"],
            })
    return tasks

"""
http://www.miyabaobei.com/search/s?cat=84&tid=372
"""

def list_parser(task): 
    rule = task["rule"]
    content = task["recv"].getvalue() 
    t = etree.HTML(content) 
    nodes = t.xpath(rule["rule"]) 
    ret = []
    for node in nodes:
        qid = node.attrib["id"].split("_")
        link = node.xpath("a/@href")
        price = node.xpath("div[contains(@id, 'item_')]/div/div/span[contains(@id, 'sale_price')]/text()") 
        if not link or not price or not qid: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append(("http://www.miyabaobei.com" + link[0],
            qid[1], price[0]))
    return ret



def stock_task_filter(items):
    l = len(items)
    n = l / 40 
    if l % 40:
        n += 1 
    ret = []
    base ="http://www.miyabaobei.com/instant/item/getOutletsItemsInfo?ids="
    for i in range(n): 
        group = items[i*40:(i+1)*40] 
        ids = "-".join([k[1] for k in group]) + "-"
        ret.append({
                "url": base+ids
                })
    return ret

"""
http://www.miyabaobei.com/instant/item/getOutletsItemsInfo?ids=1001463-1014908-1004202-1007429-1007427-1005020-1000344-1000363-1000743-1000897-1000898-1000899-1000343-1000744-1001462-1002153-1002156-1002161-1002163-1002165-1002794-1002870-1003896-1004100-1004116-1004118-1004199-1004432-1004433-1005021-1005060-1005061-1007319-1007320-1007426-1010341-1012907-1012913-1013691-1013693-

"""

def stock_parser(task):
    j = json.loads(task["recv"].getvalue())
    if not j["res"]: 
        log_with_time("bad response: %s" % task["url"])
        return
    ret = []
    for i in j["data"]:
        if int(i["s"]):
            stock = 1
        else:
            stock = 0
        price = i["sp"]
        qid = i["id"]
        ret.append((qid, price, stock)) 
    result = format_price(ret)
    return result

