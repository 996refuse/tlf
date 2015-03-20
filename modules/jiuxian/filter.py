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

def price_filter(items):
	if not items:
		return []
	url = "http://act.jiuxian.com/act/selectPricebypids.htm?ids="
	dstock = dict(items)
	url += ",".join(dstock.keys())
	return [{
		"url": url,
		"stock": dstock
	}]