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
	#pdb.set_trace()
	ret = []
	for i in items:
		ret.append({
			"url": i[0],
			"gid": i[1][0],
			"price": i[1][1]
		})
	return ret