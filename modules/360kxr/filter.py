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

def price_filter(items):
    ret = []
    for g,s in items:
    	ret.append({
    		"url": g,
            "stock": s
    	})
    return ret