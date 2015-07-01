from spider import async_http
import pdb


def jump(task): 
    t = task.copy() 
    t["header"] = async_http.random_header()
    return t 


def get_cookie(task): 
    l1 = task["res_header"].get("Location")
    t = task.copy()
    t["url"] = l1
    return t 


def use_cookie(task): 
    t = task.copy()
    t["url"] = task["prev"]["url"]
    t["cookie"] = async_http.get_cookie(task["res_cookie"]) 
    return t 


chain = (jump, get_cookie, use_cookie)


def chaoshi_pager_filter(item):
    return {
            "url": item,
            "chain": chain,
            }

    
