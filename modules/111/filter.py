#-*-encoding=utf-8-*-
from spider import split_list
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

def price_filter(items):
    gprice_url = lambda i: 'http://www.111.com.cn/interfaces/item/itemPrice.action?itemids=%s'%i
    ret = []
    for g,s in items:
        ret.append({"url": gprice_url(g), "gid":g, "stock": s})
    return ret
