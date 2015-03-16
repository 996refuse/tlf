#-*-encoding=utf-8*- 
import json
import re
import pdb 
import async_http
from lxml import etree
from spider import format_price
from spider import log_with_time
from spider import format_style_group

base = "http://www.gome.com.cn/p/asynSearch"

def task_filter(x): 
    pt = payload(x, 1)
    return { 
            "old_url": x,
            "url": base,
            "payload": pt
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
    item = json.loads(c) 
    if "pageBar" not in item:
        log_with_time("no pageBar: %s" % task["old_url"])
        return
    m = item["pageBar"]
    ret = [] 
    if not m.get("totalCount", 0):
        log_with_time("empty category: %s" % task["old_url"])
        return ret
    for i in range(1, m["totalPage"]+1):
        pt = payload(task["old_url"], i)
        ret.append({
            "payload": pt,
            "url": base, 
            "old_url": task["old_url"],
            })
    return ret


GET_CAT = re.compile("/(cat[0-9]+)") 


def payload(url, page): 
    cat =GET_CAT.findall(url)
    if not cat:
        raise ValueError("url error %s" % url) 
    param = {
            "mobile": False,
            "catId": cat[0],
            "catalog": "coo8Store",
            "siteId": "coo8Site", 
            "shopId": "",
            "regionId": "23010500", 
            "pageName": "list", 
            "et": "",
            "XSearch": False,
            "startDate": 0,
            "endDate": 0,
            "pageNumber": 1,
            "pageSize": 48,
            "state": 4,
            "weight": 0,
            "more": 0,
            "sale": 0,
            "instock": 0,
            "filterReqFacets": None,
            "rewriteTag": False,
            "atgregion": "",
            "userId": "",
            "priceTag": 0,
            "t": "&amp;cache=4&amp;parse=6"
            } 
    args = {
            "module": "product",
            "from": "category",
            "page": str(page),
            "paramJson": json.dumps(param)
            } 
    return args



def list_parser(task, rule): 
    item = json.loads(task["text"]) 
    rows = [] 
    style_groups = [] 
    if "products" not in item:
        log_with_time("found nothing: %s" % task["old_url"])
        return
    for p in item["products"]: 
        try: 
            s = p["skus"] 
            price = s["price"]
            mainurl = s["sUrl"] 
        except KeyError:
            print s
            continue
        if s["stock"] > 0:
            stock = 1
        else:
            stock = 0 
        if len(p.get("images", [])) > 1: 
            style_group = []
            for j in p["images"]:
                url = j["sUrl"]
                style_group.append(url)
                rows.append((url, price, stock)) 
            style_groups.append(format_style_group(mainurl, style_group))
        else: 
            rows.append((mainurl, price, stock)) 
    result = format_price(rows) 
    return {
            "spider": result,
            "group": style_groups
            }
