#-*-encoding=utf-8-*-
from spider import split_list
import random
import time
import pdb
import async_http

def pager_filter(x):
    return {
            "url": x
            }

def list_filter(x):
    return {
            "url": x
            } 

stburl ="http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite=1&provinceId=1&"
def stock_task_filter(items):
    prices = dict(items)
    ret = []
    base = stburl + "&".join(["productIds=" + i for i in prices.keys()])
    ret.append({
            "url": base,
            "price":  prices,
            })
    return ret