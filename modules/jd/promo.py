#-*-encoding=utf-8-*-

import pdb
from spider import jsonp_json
from spider import log_with_time
from spider import format_promo

from decimal import Decimal



def promo_filter(item):
    url = "http://pi.3.cn/promoinfo/get?id=%s&area=12_904_905_0&origin=1&callback=Promotions.set" 
    return {
            "url": url % item, 
            "crc": item
            } 



def coupon(couponlist):
    s = 0
    for m in couponlist:
        if m["type"] == 1:
            s += m["couponQouta"]
    return s



def promo_test(promos): 
    import json 
    dp_id, i = promos[0]
    for i in json.loads(i): 
        print i["type"], i["keywords"], i["desc"]



def promo_parser(task, rule):
    promos = [] 
    if len(task["text"]) < 200: 
        log_with_time("no promo info")
        ret = [(task["crc"], promos)] 
        return format_promo(ret) 
    try:
        j = jsonp_json(task["text"])
    except ValueError:
        log_with_time("json error: %s" % task["text"]) 
        ret = [(task["crc"], promos)] 
        return format_promo(ret) 
    if not j: 
        log_with_time("json null: %s" % task["text"])
        ret = [(task["crc"], promos)] 
        return format_promo(ret) 
    if j.get("mpt"):
        price = Decimal(j.get("mpt").split(",")[0])
        promos.append({ 
            "keywords": "手机专享价",
            "type": 9,
            "desc": "手机专享价: %s" % price,
            }) 
    for i in j["promotionInfoList"]: 
        ptype = i["promoType"] 
        if i.get("addMoney") and float(i.get("addMoney")):
            continue 
        if i.get("userLevel", 0) > 50:
            continue 
        if ptype == 1:
            if not i.get("needJBeanNum"):
                i["needJBeanNum"] = 0 
            if i["needJBeanNum"] > 0 and i.get("price", 0) > 0:
                #京豆优惠购 
                promos.append({
                    "desc": "京豆优惠购",
                    "type": 11,
                    "desc": "使用%s京豆可享受优惠价%s" % (Decimal(i["needJBeanNum"]), Decimal(i["price"])) 
                    }) 
            if i.get("adwordCouponList"): 
                s = coupon(i["adwordCouponList"])
                if s:
                    promos.append({
                        "desc": "赠%s京券" % s,
                        "keywords": "赠券",
                        "type": 3,
                        })
            if i.get("score"):
                #送京豆
                promos.append({
                    "keywords": "送京豆",
                    "type": 3,
                    "desc": "送京豆%s个" % i["score"]
                    })
            if i.get("extType") == 8:
                #团购 
                promos.append({
                    "keywords": "闪团",
                    "type": 8,
                    "desc": "闪团"
                    })
        elif ptype == 15: 
            if i["rebate"] > 0: 
                promos.append({
                    "desc": "封顶",
                    "type": 11,
                    "desc": "封顶%s折" % float(10 * i["rebate"])
                    }) 
        elif ptype == 4: 
            if i.get("adwordGiftSkuList"): 
                s = []
                for m in i["adwordGiftSkuList"]:
                    #1是附件
                    if m["giftType"] == 2:
                        s.append("%s x %s" % (m["name"].replace(" ", ""), m["number"])) 
                if s:
                    promos.append({
                        "keywords": "赠品",
                        "type": 3,
                        "desc": u"赠 " + ", ".join(s)
                        })
            #赠券
            if i.get("adwordCouponList"): 
                s = coupon(i["adwordCouponList"])
                if s:
                    promos.append({
                        "desc": "赠%s京券" % s,
                        "keywords": "赠券",
                        "type": 3,
                        }) 
            #赠京豆
            if i.get("score") and float(i["score"]):
                promos.append({
                    "keywords": "送京豆",
                    "type": 3,
                    "desc": "送京豆%s个" % i["score"]
                    }) 
        elif ptype == 10: 
            ftype = i["fullRefundType"] 
            if ftype == 1: 
                for m in i["fullLadderDiscountList"]: 
                    #加价购忽略
                    if m.get("addMoney") and Decimal(m["addMoney"]): 
                        continue
                    #非满减
                    if not m["needMoney"]:
                        continue
                    m["needMoney"] = Decimal(m["needMoney"])
                    m["rewardMoney"] = Decimal(m["rewardMoney"])
                    m["percent"]  = Decimal(m.get("percent", 0))
                    if m["needMoney"] and m["rewardMoney"]:
                        promos.append({
                            "keywords": "满减",
                            "type": 1,
                            "desc": "满%s减%s" % (m["needMoney"], m["rewardMoney"]),
                            }) 
                    if m["needMoney"] and not m["rewardMoney"] and not m["percent"]:
                        promos.append({
                            "keywords": "满赠",
                            "type": 3,
                            "desc": "满%s赠热销商品" % (m["needMoney"])
                            })
                    #满赠
                    if m.get("haveFullRefundGifts"): 
                        if m["needMoney"] and ["rewardMoney"]:
                            promos.append({
                                "keywords": "满送",
                                "type": 3,
                                "desc": "满%s减%s，得赠品" % (m["needMoney"], m["rewardMoney"]),
                                }) 
                        elif m["needMoney"]:
                            promos.append({
                                "keywords": "满送",
                                "type": 3,
                                "desc": "满%s即赠热销商品" % m["needMoney"]
                                })
                    #满赠券 
                    if m.get("adwordCouponList") and i["needMoney"]: 
                        s = coupon(m["adwordCouponList"])
                        if s:
                            promos.append({
                                "keywords": "满送券",
                                "type": 3,
                                "desc": "满%s送%s京券" % (m["needMoney"], s)
                                }) 
                    if m["needMoney"] and m["percent"]: 
                        promos.append({
                            "keywords": "满%s可享折扣" % m["needMoney"],
                            "type": 1,
                            "desc": "满%s减%s%%" % (m["needMoney"], m["percent"])
                            }) 
            elif ftype == 2: 
                if not i.get("needMondey"):
                    continue
                if float(i["needMondey"]) and i["reward"]:
                    if i.get("topMoney") and float(i["topMoney"]): 
                        promos.append({
                            "desc": "多次满减",
                            "type": 1,
                            "desc": "每满%s可减%s现金, 最多可减 %s" % (Decimal(i["needMondey"]), Decimal(i["reward"]), Decimal(i["topMoney"]))
                            })
                    else:
                        promos.append({
                            "keywords": "多次满减",
                            "type": 1,
                            "desc": "每满%s可减%s现金" % (Decimal(i["needMondey"]), Decimal(i["reward"]))
                            }) 
                    if i["needMondey"] and i["adwordCouponList"]: 
                        s = coupon(i["adwordCouponList"]) 
                        if s:
                            promos.append({
                                "keywords": "满送券",
                                "type": 3,
                                "desc": "每满%s即赠%s元京券" % (Decimal(i["needMondey"]), Decimal(s))
                                }) 
            elif ftype == 6: 
                s = []
                for m in i["fullLadderDiscountList"]:
                    if Decimal(m["needMoney"]) and Decimal(m["rewardMoney"]): 
                        s.append("满%s减%s" % (Decimal(m["needMoney"]), Decimal(m["rewardMoney"])))
                if s:
                    promos.append({
                        "keywords": "满减",
                        "type": 1,
                        "desc": ", ".join(s)
                        }) 
            elif ftype == 20: 
                log_with_time("ftype 20: %s" % task["url"])
            elif ftype == 11: 
                if i["needNum"] and i["deliverNum"]:
                    promos.append({
                        "keywords": "多买多惠",
                        "type": 11,
                        "desc": "买%s立减%s件商品价格" % (i["needNum"], i["deliverNum"])
                        }) 
            elif ftype == 13: 
                if i.get("needMondey") and i.get("deliverNum"):
                    promos.append({
                        "keywords": "多件优惠",
                        "type": 11,
                        "desc": "%s元可买%s件" % (Decimal(i["needMondey"]), i["deliverNum"]),
                        }) 
            elif ftype == 14: 
                #满needNum赠热销商品
                if i.get("needNum") and i.get("rebate"):
                    promos.append({
                        "keywords": "多件优惠",
                        "type": 11,
                        "desc": "满%s件总价打%s折" % (Decimal(i["needNum"]), float(10 * i["rebate"]))
                        })
                elif i.get("needNum"): 
                    promos.append({
                        "keywords": "满赠",
                        "type": 3,
                        "desc": "满%s件即赠热销商品" % i["needNum"]
                        })
            elif ftype == 15: 
                s = []
                for m in i["fullLadderDiscountList"]:
                    if m.get("addMoney") and float(m["addMoney"]):
                        continue 
                    if m["needNum"] and m["rebate"]:
                        s.append("满%s件总价打%s折" % (m["needNum"], float(10 * m["rebate"])))
                if s:
                    promos.append({
                        "keywords": "多买优惠",
                        "type": 11,
                        "desc": ", ".join(s)
                        }) 
            elif ftype == 16: 
                mtype = i["mfmzExtType"] 
                if mtype == 0:
                    s = []
                    for m in i["fullLadderDiscountList"]: 
                        if m.get("addMoney") and float(m["addMoney"]):
                            continue
                        if m.get("needNum") and m.get("rebate"):
                            s.append("满%s件总价打%s折" % (m["needNum"],  float(10 * m["rebate"])))
                    if s:  
                        promos.append({
                            "keywords": "满减",
                            "type": 3,
                            "desc": ", ".join(s)
                            }) 
                elif mtype == 1 or mtype == 3: 
                    #fullLadderDiscountList, 阶梯满减
                    s = []
                    for m in i["fullLadderDiscountList"]:
                        if m["needMoney"] and m["rewardMoney"]: 
                            s.append("满%s减%s" % (Decimal(m["needMoney"]), Decimal(m["rewardMoney"])))
                    if s:
                        promos.append({
                            "keywords": "满减",
                            "type": 1,
                            "desc": ", ".join(s)
                            }) 
                if mtype == 2: 
                    for m in i["fullLadderDiscountList"]:
                        if m["needMoney"]:
                            promos.append({
                                "keywords": "满赠",
                                "type": 3,
                                "desc": "满%s即赠热销商品" % Decimal(m["needMoney"])
                                }) 
                elif mtype == 4: 
                    s = []
                    for m in i["fullLadderDiscountList"]:
                        if m["needMoney"]:
                            s.append("满%s得赠品" % Decimal(m["needMoney"]))
                    if s:
                        promos.append({
                            "keywords": "满赠",
                            "type": 3,
                            "desc": ",".join(s)
                            }) 
                elif mtype == 5: 
                    s = []
                    for m in i["fullLadderDiscountList"]:
                        if m["needMoney"] and m["rewardMoney"] and m["mfmzTag"] == 1:
                            s.append("满%s立减%s" % (Decimal(m["needMoney"]), Decimal(m["rewardMoney"])))
                    if s:
                        promos.append({
                            "keywords": "满减",
                            "type": 1,
                            "desc": ", ".join(s)
                            })
            elif ftype == 17:
                log_with_time("ftype 17: %s" % task["url"]),
            elif ftype == 20:
                log_with_time("ftype 20: %s" % task["url"]), 
    ret = [(task["crc"], promos)] 
    return format_promo(ret)


