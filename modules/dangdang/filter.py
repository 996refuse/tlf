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

itmurl = "http://m.dangdang.com/h5product/color_size.php?pid=%s&is_catalog_product=1"
stkurl = "http://product.dangdang.com/pricestock/callback.php?type=stockv2&product_id=%s&fourarea=true"
def stock_filter(items):
    ret = []
    for i in items:
    	ret.append({
    		"url": stkurl%i[0],
    		"info": i,
    	})
    return ret