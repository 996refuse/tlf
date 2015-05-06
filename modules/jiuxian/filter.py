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

rurl = "http://act.jiuxian.com/act/selectPricebypids.htm?ids="
def price_filter(items):
	if not items:
		return []
	dstock = dict(items)
	url = rurl + ",".join(dstock.keys())
	return [{
		"url": url,
		"stock": dstock
	}]