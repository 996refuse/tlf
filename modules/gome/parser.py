#-*-encoding=utf-8*- 
import json
import re
import pdb 
import time
from spider import async_http
from lxml import etree
from spider import format_price
from spider import log_with_time
from spider import format_style_group 
from spider import jsonp_json

def pager_filter(x): 
    cat =re.findall("/(cat[0-9]+)\.", x) 
    url = payload(cat[0], 1)
    return { 
            "url": url,
            "cat": cat[0],
            } 


def remove_gap(url):
    b = []
    for i in url:
        if i in ("\t\n \r"):
            continue
        b.append(i)
    return "".join(b)


def cats_parser(url, content, rule): 
    t = etree.HTML(content)
    ret = []
    filter = {}
    for i in rule:
        for j in t.xpath(i): 
            href = remove_gap(j.attrib["href"]) 
            if href in filter:
                continue 
            else:
                filter[href] = None
            ret.append(href)
    return ret 


GET_COUNT =re.compile(u"共([0-9]+)") 


def pager(task, rule): 
    c = task["text"].decode("utf-8")
    item = jsonp_json(c)
    if "pageBar" not in item:
        log_with_time("no pageBar: %s" % task["url"])
        return
    m = item["pageBar"]
    ret = [] 
    if not m.get("totalCount", 0):
        log_with_time("empty category: %s" % task["url"])
        return ret 
    for i in range(1, m["totalPage"]+1): 
        ret.append({ 
            "url": payload(task['cat'], i)
            }) 
    return ret


ajax_base = "http://search.gome.com.cn/cloud/asynSearch?callback=callback_product&module=product&from=category&page={page}&paramJson=%7B+%22mobile%22+%3A+false+%2C+%22catId%22+%3A+%22{cat}%22+%2C+%22catalog%22+%3A+%22coo8Store%22+%2C+%22siteId%22+%3A+%22coo8Site%22+%2C+%22shopId%22+%3A+%22%22+%2C+%22regionId%22+%3A+%2223010100%22+%2C+%22pageName%22+%3A+%22list%22+%2C+%22et%22+%3A+%22%22+%2C+%22XSearch%22+%3A+false+%2C+%22startDate%22+%3A+0+%2C+%22endDate%22+%3A+0+%2C+%22pageSize%22+%3A+48+%2C+%22state%22+%3A+4+%2C+%22weight%22+%3A+0+%2C+%22more%22+%3A+0+%2C+%22sale%22+%3A+0+%2C+%22instock%22+%3A+0+%2C+%22filterReqFacets%22+%3A++null++%2C+%22rewriteTag%22+%3A+false+%2C+%22userId%22+%3A+%22%22+%2C+%22priceTag%22+%3A+0+%2C+%22cacheTime%22+%3A+1+%2C+%22parseTime%22+%3A+2%7D&_={time}"

#page, cat, time 


def payload(cat, page): 
    ajax = ajax_base.format(time= str(int(time.time() * 1000000)), 
            page = int(page),
            cat = cat,
            )
    return ajax


def test_list(items):
    pdb.set_trace()


url_pat = re.compile("product/(.*)\.")
gome_base = "http://item.gome.com.cn/%s.html"


def list_parser(task, rule): 
    item = jsonp_json(task["text"]) 
    skus = [] 
    groups = [] 
    dp_pairs = [] 
    if "products" not in item: 
        log_with_time("found nothing: %s" % task["url"])
        return
    now = int(time.time())
    dps_log = {} 
    for p in item["products"]: 
        try: 
            s = p["skus"] 
            price = s["price"]
            url = s["sUrl"]
            title = s["name"]
        except KeyError:
            log_with_time("rule error: %s" % task["text"])
            continue 
        dp_pairs.append((url, title))
        if s["stock"] > 0:
            stock = 1
        else:
            stock = 0 
        skus.append((url, price, stock)) 
    result = format_price(skus) 
    for r in result:
        dps_log[r[1]] = now
    return {
            "spider": result,
            "dp": dp_pairs,
            "dps_log": dps_log,
            }
