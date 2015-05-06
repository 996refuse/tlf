
def pager_filter(x):
    return {
            "url": x
            }

def list_filter(x):
    return {
            "url": x
            }

def price_filter(x): 
    link, qid, pimg, s = x
    return {
            "url": pimg, 
            "link": link,
            "qid": qid,
            "stock": s 
            }

