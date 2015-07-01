import re
import time
import pdb
from lxml import etree
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
 
def cats_parser(url, res, rule):
    t = etree.HTML(res["text"])
    return t.xpath(rule)

def cats_test(items):
    assert items 

page_base = "http://www.muyingzhijia.com/Shopping/subcategory.aspx?cateID={cat}&page={page}" 

def pager(task, rule): 
    t = etree.HTML(task["text"]) 
    page = t.xpath(rule)
    if not page:
        log_with_time("page rule error")
        return
    ret = [task["url"]] 
    num = re.findall("\d+", " ".join(page))
    cat = re.findall("cateID=(\d+)", task["url"])[0]
    for i in range(2, int(num[0]) + 1):
        ret.append(page_base.format(cat=cat, page=i))
    return ret 


def pager_test(items):
    assert items 



def list_parser(task, rule):
    t = etree.HTML(task["text"]) 
    nodes = t.xpath(rule["node"]) 
    if not nodes:
        log_with_time("node rule error: %s" % task["url"])
        return 
    dp = []
    dps = {}
    ret = [] 
    now = int(time.time()) 
    for node in nodes:
        link = node.xpath(rule["link"])
        gid = node.xpath(rule["gid"]) 
        if not link or not gid:
            log_with_time("rule error: %s" % task["url"])
            continue 
        gid = gid[0]
        dp.append((link[0], ""))
        ret.append(gid)
        dps[gid] = now 
    return {
            "dps_log": dps,
            "dp": dp,
            "price": ret,
            } 
    

def list_test(items):
    assert items 


def stock_test(items):
    pdb.set_trace()



def stock_parser(task, rule): 
    try:
        j = jsonp_json(task["text"].decode("utf-8"))
    except Exception as e:
        log_with_time("response error: %s %s" % (task["url"], e)) 
        return 
    ret= [] 
    for item in j.get("PromPriceList", []): 
        pid = str(item["ProductId"])
        price = item["PromPriceShow"] 
        if item["Stock"]:
            stock = 1
        else:
            stock = 0 
        ret.append((pid, price, stock)) 
    return format_price(ret)
