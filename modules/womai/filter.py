#-*-encoding=utf-8-*-
from spider import split_list_iter
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

api = 'http://price.womai.com/PriceServer/open/productlist.do?prices=buyPrice&ids='
def stock_filter(items):
    ret = []
    inum = len(items)
    step = 10
    for i in range(0, inum, step):
    	ret.append({
    		"url": api + ','.join(items[i:i+step]),
        })
    return ret