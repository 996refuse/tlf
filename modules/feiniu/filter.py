#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import pdb
import async_http
import re

def pager_filter(x):
    return {
            "url": "http://www.feiniu.com/" + x
        	}

def list_filter(x):
    return {
            "url": x
            }

def price_filter(x):
    return {
            "url": x
            }
