import re
from lxml import etree
from spider import format_price
from spider import log_with_time
import pdb

base = "http://category.vip.com/search-1-0-1.html?%s" 

def cats_parser(url, content, rule): 
    cats = set()
    for i in rule:
        cats = cats.union(set(re.findall(i, content))) 
    ret = []
    for c in cats:
        ret.append(base % c)
    return ret


def meizhuang_cats_parser(url, content, rule):
    pdb.set_trace()
    t = etree.HTML(content) 
    ret = []
    for node in t.xpath(rule[0]):
        #link
        link = node.xpath(rule[1])
        #price
        price = node.xpath(rule[2]) 
        if not link or not price:
            log_with_time("rule error: %s" % url)
        ret.append((link[0], price[0], 1))
    result = format_price(ret)
    return result
