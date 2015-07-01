from lxml import etree 
from spider import simple_http
from spider import format_price
from spider import log_with_time
import re

def cats_parser(url, res,  rule): 
    content = res['text']
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        ret.extend(items)
    return ret


def pager(task, rule): 
    t = etree.HTML(task["text"])
    total = t.xpath(rule["count"])
    if not total:
        log_with_time("rule error: %s" % rule)
        return
    total = int(total[0])   
    num = total / 20
    if total % 20:
        num += 1 
    tasks = []
    url = url_generator(task["url"], rule["url"])
    for i in range(num):
        tasks.append({
                "payload": payload_generator(i),
                "url": url,
                "old_url": task["url"]
                })
    return tasks

        

def payload_generator(page):
    payload = {
            "beginIndex": str(page * 20),
            "brandId": "0",
            "facet": "",
            "orderBy": "18",
            "pageSize": "20",
            "resultType": "products",
            "xFaceFilter": "" 
            }
    return payload

    
        
def url_generator(url, base):
    cat = re.findall("/([0-9]+)_", url)
    if not cat: 
        return 
    args = {
            "categoryId": cat[0],
            "filterFacet": "",
            "langId": "-7",
            "metaData": "",
            "resultCatEntryType": "",
            "sType": "SimpleSearch",
            "searchTerm": "",
            "searchType": "",
            "storeId": "10001"
            } 
    return base + "?" + simple_http.generate_query(args) 




def fix_price(price):
    p = re.findall('[0-9\.]+', price)
    if not p:
        log_with_time("price format error: %s" % price) 
        return 
    return p[0] 



def list_parser(task, rule): 
    t = etree.HTML(task["text"])
    nodes = t.xpath(rule["node"])
    ret = []
    for node in nodes:
        link = node.xpath(rule["link"])
        price = node.xpath(rule["price"])
        if not link or not price:
            log_with_time("rule error: %s" % task["old_url"])
            continue
        p = fix_price(price[0]) 
        ret.append((link[0], p, 1)) 
    result = format_price(ret)
    return result 
