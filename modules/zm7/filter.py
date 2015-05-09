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

def stock_filter(items):
	ret = []
	for i in items:
		ret.append({
			"url": i[0],
			"price": i[1]
		})
	return ret