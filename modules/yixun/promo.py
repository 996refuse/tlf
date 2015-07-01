#-*-encoding=utf-8-*-
import pdb
import json
from spider import log_with_time
from spider import format_promo


def promo_filter(item):
    url = "http://item.yixun.com/p/CGINewPromotion?pid=%s&whid=1&product_sale_model=0"
    return {
            "url": url % item,
            "crc": item
            }


def promo_test(items):
    print items


def promo_parser(task, rule): 
    promos = [] 
    try:
        item = json.loads(task["text"])
    except ValueError as e:
        log_with_time(e)
        return format_promo([(task["crc"], promos)])
    if int(item.get("errno", "1")) != 0: 
        log_with_time("errno not zero")
        return format_promo([(task["crc"], promos)])

    for i in item["data"]:
        for j in i["info_list"]:
            tp = int(j["discount_type"])
            if tp == 5:
                #满减
                promos.append({
                    "keywords": "满减",
                    "type": 1,
                    "desc": j["name"]
                    }) 
            #7, 8, 加价换购, 10推荐活动忽略 
            elif tp == 9:
                promo_id = j["promotion_ruleid"] 
                more = []
                for m in item["data"]:
                    if m["item_ruleid"] == promo_id:
                        more.append(m["title"])
                promos.append({
                    "keywords": "满赠",
                    "type": 3,
                    "desc": u"%s: %s" %  (j["name"], ", ".join(more))
                    })
            elif tp == 11:
                #可领券 
                promos.append({
                    "keywords": "赠券",
                    "type": 3,
                    "desc": j["desc"].encode("utf8").replace("点击领券！", "")
                    }) 

    ret = [(task["crc"], promos)]
    return format_promo(ret)

        

