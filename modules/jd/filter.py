#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time
import pdb
import re
from spider import async_http


def pager_filter(x):
    if isinstance(x, list):
        url, limit = x
        return {
                "url": url,
                "limit": limit,
                }
    return {
            "url": x
            } 


def list_filter(x):
    return {
            "url": x
            } 


dp_base = "http://item.jd.com/%s.html"


def styles_filter(x): 
    return {
            "url": dp_base % x
            }


price_url = "http://p.3.cn/prices/mgets?type=1&skuIds=%s&area=1_72_2799&callback=JQuery%s&_=%s" 


#stock_url = "http://search.jd.com/stock?skus=%s&district=1_72_2799&callback=get_sotck_cb&callback=jQuery%s&_=%s" 

stock_url = "http://st.3.cn/gsis.html?type=getstocks&skuids=%s&provinceid=1&cityid=72&areaid=2799&callback=jsonp%s&_=%s"


#两个组过滤
def price_filter(items): 
    ret = []
    for group in split_list_iter(items, 60):
        url = price_url % (",".join("J_"+ i for i in group), 
                random.randint(1000000, 10000000),
                int(time.time() * 1000)) 
        ret.append({ "url": url})
    return ret 



def stock_filter(items): 
    keys = async_http.quote(",".join(items.keys()))
    url = stock_url % (keys, random.randint(1000000, 10000000),
                int(time.time() * 1000)) 
    return {
            "url": url,
            "price": items
            } 


GET_QID = re.compile("/([0-9]+)\.") 


def off_filter(items): 
    qids = []
    for item in items: 
        url = item[1]
        if "360buy" in url or "book" in url: 
            qid = GET_QID.findall(url)[0] 
        else: 
            qid = item[0]
        qids.append(qid) 
    ret = []
    for group in split_list_iter(qids, 60):
        url = price_url % (",".join("J_"+ i for i in group), 
                random.randint(1000000, 10000000),
                int(time.time() * 1000)) 
        ret.append({ "url": url})
    return ret 

