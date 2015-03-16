#-*-encoding=utf-8-*-
import async_http
from lxml import etree
import json
import pdb
import re



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
