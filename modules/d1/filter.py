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
	pdb.set_trace()
	return [{
		'url': items[0],
		"gid": items[1][0],
		"price": items[1][1]
	}]