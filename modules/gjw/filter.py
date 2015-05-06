#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import pdb
import async_http
import re

def cats_filter(x):
	return {
		"url": x
	}

def pager_filter(x):
    return {
            "url": x
        	}

def list_filter(x):
    return {
            "url": x
            }

surl = "http://www.gjw.com/Ajax/Order/OrderAdd-act-AddPro-ID-%s-Quantity-1.htm"
def stock_filter(items):
	if not items:
		return []
	ret = []
	for gh, p in items:
		g = re.search("\d+", gh).group()
		ret.append({
			"url": surl%g,
			"item": (gh,p)
		})
	return ret