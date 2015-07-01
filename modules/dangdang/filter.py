#-*-encoding=utf-8-*-
from spider import split_list_iter
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

itmurl = "http://m.dangdang.com/h5product/color_size.php?pid=%s&is_catalog_product=1"
stkurl = "http://product.dangdang.com/pricestock/callback.php?type=stockv2&product_id=%s&fourarea=true"
def stock_filter(items):
    ret = []
    for i in items:
    	ret.append({
    		"url": stkurl%i[0],
    		"info": i,
    	})
    return ret

priceurl = "http://category.dangdang.com/Standard/Search/Extend/hosts/api/get_price.php"
def off_filter(items): 
    gids = [item[0] for item in items] 
    tasks = []
    for i in split_list_iter(gids, 60):
        offcheck_hdr = async_http.json_header.copy()
        offcheck_hdr["Referer"] = "http://category.dangdang.com" 
        tasks.append({ 
            "url": priceurl,
            "payload": {
                "pids": ",".join(i),
                "time": str(int(time.time())),
                "type": "get_price",
                }, 
            "header": offcheck_hdr
            }) 
    return tasks
