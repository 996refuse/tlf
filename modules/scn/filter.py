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

def stock_task_filter(items):
    ret = []
    for u,p in items:
    	ret.append({
    		"url": u,
    		"price": p
    		})
    return ret