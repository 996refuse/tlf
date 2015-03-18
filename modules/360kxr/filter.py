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

def stock_task_filter(items):
    ret = []
    for i in items:
    	ret.append({
    		"url": i
    		})
    return ret