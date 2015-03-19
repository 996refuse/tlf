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
    for u,g in items:
        ret.append({"url": gprice_url(g), "gurl": u})
    return ret

def stock_task_filter(items):
    #gstock_url = lambda pid,pno: 'http://www.111.com.cn/interfaces/specials.action?itemid=%r&pno=%r'%(pid,pno)
    ret = []
    for u,p in items:
        ret.append({
            "url": u,
            "price": p
        })
    return ret