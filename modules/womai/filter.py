#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import pdb
import async_http
import spider


site_table = {
        32: { 
            "siteinfotemp": "0", 
            },
        1032: {
            "siteinfotemp": "100",
            },
        2032: {
            "siteinfotemp": "200",
            },
        }


mid_table = {
        32: 0,
        1032: 100, 
        2032: 200, 
        }


from_urls = {
        32: "http://www.womai.com/ProductList.htm",
        1032: "http://sh.womai.com/ProductList.htm",
        2032: "http://gz.womai.com/ProductList.htm",
        }

def from_filter(x): 
    return from_urls[spider.CONFIG["site_id"]] 


def pager_filter(x):
    return {
            "url": x,
            "cookie": site_table[spider.CONFIG["site_id"]],
            }

def list_filter(x):
    return {
            "url": x, 
            "cookie": site_table[spider.CONFIG["site_id"]],
            } 

api = 'http://price.womai.com/PriceServer/open/productlist.do?mid={mid}&usergroupid=100&prices=buyPrice&ids='
def stock_filter(items): 
    ret = [] 
    for i in split_list_iter(items, 30): 
    	ret.append({
    		"url": api.format(mid= mid_table[spider.CONFIG["site_id"]]) + ','.join(i)
        })
    return ret
