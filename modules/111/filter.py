#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import pdb
import async_http
import re

def pager_filter(x):
    return {
            "url": x
            }

def list_filter(x):
    return {
            "url": x
            }

itemurl = "http://www.111.com.cn/product/%s.html"
def item_filter(items):
    ret = []
    for g in items:
        ret.append({"url": itemurl%g, "gid":g})
    return ret

gprice_url = 'http://www.111.com.cn/interfaces/item/itemPrice.action?itemids=%s'
def price_filter(items):
    ret = []
    for g,s in items:
        ret.append({"url": gprice_url%g, "gid":g, "stock": s})
    return ret
