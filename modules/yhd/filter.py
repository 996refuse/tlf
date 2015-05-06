#-*-encoding=utf-8-*-
from spider import split_list_iter
import random
import time 
from spider import async_http
import spider

cookie_table = {
        31: "5",
        1031: "2",
        2031: "20",
        3031: "18",
        4031: "12"
        } 

province_id = 5 


def set_province_id(rule): 
    global province_id
    province_id = cookie_table[spider.CONFIG["site_id"]] 



def pager_filter(x):
    return {
            "url": x,
            "cookie": {
                "provinceId": province_id,
                },
            }

def list_filter(x):
    return {
            "url": x,
            "cookie": {
                "provinceId": province_id,
                }, 
            } 

stburl ="http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite=1&provinceId=%s&" % province_id


def stock_task_filter(items): 
    ret = []
    for i in split_list_iter(items, 40):
        prices = dict(i) 
        base = stburl + "&".join(["productIds=" + i for i in prices.keys()])
        ret.append({
                "url": base,
                "price":  prices,
                })
    return ret
