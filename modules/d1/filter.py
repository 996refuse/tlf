#-*-encoding=utf-8-*-
from spider import split_list_iter
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

def stock2_filter(items):
	#pdb.set_trace()
	if not items:
		return []
	ret = []
	for a,b,c in items:
		ret.append({
			"url": a,
			"gid": b,
			"price": c
		})
	return ret