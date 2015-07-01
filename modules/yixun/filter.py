#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import spider
import pdb
import async_http

site_id = 15 

def set_siteid(CONFIG): 
    global site_id 
    site_id = spider.CONFIG["site_id"]


site_table = {
        15: {
            'wsid': '1', 
            "prid": "1598_1591",
            'loc': "2_1_320000_320100_320102_0",
            }, 
        1015: {
            'wsid': '1', 
            "prid": "31293_131",
            'loc': "2_1_110000_110100_110101_31293"
            },
        2015: {
            'wsid': '1', 
            "prid": "422_403",
            'loc': '2_1_440000_440300_440304_0',
            },
        3015: {
            'wsid': '1', 
            "prid": "28869_1323",
            'loc': '2_1_420000_420100_420102_28869',
            },
        4015: {
            'wsid': '1', 
            "prid": "5039_158",
            'loc': "2_1_500000_500100_500233_5039"
            },
        5015: {
            'wsid': '1', 
            "prid": "6066_2212",
            'loc': "2_1_610000_610100_610125_6066"
            }
        }


def pager_filter(x):
    return {
            "url": x,
            "cookie": site_table[site_id],
            }


def list_filter(x): 
    return {
            "url": x,
            "cookie": site_table[site_id]
            } 


def stock_filter(items):
    ret = []
    for i in items:
    	ret.append({
    		"url": i[0],
    		"price": i[1],
                "cookie": site_table[site_id]
    	})
    return ret
