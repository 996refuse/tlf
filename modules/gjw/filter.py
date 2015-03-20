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

def stock_filter(items):
	surl = lambda g: "http://www.gjw.com/Ajax/Order/OrderAdd-act-AddPro-ID-%s-Quantity-1.htm"%g
	if not items:
		return []
	ret = []
	for gh, p in items:
		g = re.search("\d+", gh).group()
		ret.append({
			"url": surl(g),
			"item": (gh,p)
		})
	return ret