#-*-encoding=utf-8-*-
from lxml import etree
import pdb 
import json
from spider import format_price
from spider import log_with_time


base = "http://www.miyabaobei.com"


def cats_parser(url, res, rule): 
    content = res['text']
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        ret.extend([base+j for j in items if not j.startswith("http")]) 
    return ret


"""
http://www.miyabaobei.com/search/s?tid=372&cat=84&order=normal&sort=desc&per_page=40
"""

def pager(task, rule): 
    content = task["text"]
    t = etree.HTML(content)
    total = t.xpath(rule[0])
    if "找到0个商品" in content:
        log_with_time("search result 0: %s" % task["url"]) 
        return
    if not total:
        log_with_time("rule error: %s" % rule[0])
        return
    total = int(total[0])   
    page = rule[1]
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


def list_parser(task, rule): 
    t = etree.HTML(task["text"]) 
    nodes = t.xpath(rule["node"])
    ret = []
    for node in nodes:
        qid = node.attrib["id"].split("_")
        link = node.xpath(rule["link"])
        price = node.xpath(rule["price"])
        if not link or not price or not qid: 
            log_with_time("rule error: %s" % task["url"])
            continue
        ret.append(("http://www.miyabaobei.com" + link[0],
            qid[1], price[0]))
    return ret



def stock_parser(task, rule):
    text = task["text"]
    if not text.startswith("{"):
        text = text[text.find("{"):]
    j = json.loads(text)
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
