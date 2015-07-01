import pdb

def pager_filter(x):
    return {
            "url": x,
            "redirect": 10,
            }

def list_filter(x):
    return {
            "url": x,
            "redirect": 10,
            }

def price_filter(x): 
    link, qid, pimg, s = x
    return {
            "url": pimg, 
            "link": link,
            "qid": qid,
            "stock": s 
            }

priceurl = 'http://www.suning.com/emall/priceService_%s_%s%%7C%%7C%%7C_1.html'
def bookprice_filter(items):
    ret = []

    for link, qid, lid, s in items:
        ret.append({
                "url": priceurl % (lid, qid), 
                "link": link,
                "qid": qid,
                "stock": s 
                })
    return ret


price_base = "http://price2.suning.cn/webapp/wcs/stores/prdprice/%s_9173_10000_9-1.png"

def off_filter(item): 
    return {
            "url": price_base % item[0],
            "qid": item[0],
            "link": item[1],
            }
