
import async_http
import pdb
import time
from spider import split_list_iter

def pager_filter(x):
    return {
            "url": x
            } 

def list_filter(x):
    return {
            "url": x
            } 


stock_base = "http://buy.api.muyingzhijia.com/json/reply/QueryPromPriceByProdId?a=0.30219353104828217&callback=jQuery17205880812340738396_1435391107448&ProductIdList={pids}&UserId=-1&Guid=201506231505da336e7b2898463db934ab1f5ed6836d&DisplayLabel=8&AreaSysNo=100&ChannelID=102&ExtensionSysNo=&_={time}&__=0.8835533487323052"


def stock_filter(items): 
    ret = []
    for i in split_list_iter(items, 60):
        keys = async_http.quote(",".join(i))
        url = stock_base.format(pids = keys, time = int(time.time() * 1000)) 
        ret.append({
                "url": url, 
                })
    return ret



