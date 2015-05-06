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

api = 'http://www.yougou.com/commodity/getGoodsDetail.sc?cNo=%s&rrdom=%s'
def stock_filter(items):
    ret = []
    inum = len(items)
    for i in items:
    	ret.append({
    		"url": api % (i[0], random.random()),
            "gurl": i[1],
            "price": i[2],
        })
    return ret