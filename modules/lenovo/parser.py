#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json

gurl = lambda x,y:'http://shop.lenovo.com.cn/search/getproduct.do?plat=4&categorycode=%s&keyword=&sorder=0&spage=%d&sarry=1'%(x,y)

def cats_parser(url, content, rule):
    t = etree.HTML(content)
    codes = [re.search("(?<=code=)\d+", i).group() for i in t.xpath(rule)]
    return [gurl(i,1) for i in codes]

def pager(task, rule):
    j = json.loads(task['text'])
    if not 'gpagecount' in j:
        log_with_time("bad response %r"%task['url'])
        return []
    code = re.search("(?<=code=)\d+(?=&)", task['url']).group()
    ret = []
    for i in range(1, j['gpagecount']+1):
        ret.append(gurl(code,i))
    return ret

surl = lambda x: 'http://shop.lenovo.com.cn/srv/getginfo.do?plat=4&gcodes=%s&salestype=0'%x
def list_parser(task, rule):
    j = json.loads(task['text'])
    if not 'glist' in j:
        log_with_time("bad response %r"%task['url'])
        return []
    ret = []
    for g in j['glist']:
        ret.append((surl(g['gcode']), g['gprice']))
    return ret

def stock_parser(task, rule):
    burl = lambda x: 'http://shop.lenovo.com.cn/product/%s.html'%x
    try:
        j = json.loads(task['text'])
        stockstatus = j['glist'][0]['stockstatus']
    except:
        log_with_time("bad response %r"%task['url'])
        return []

    if not stockstatus or '无' in stockstatus.encode("utf8"):
        stock = 0
    else:
        stock = 1

    code = re.search("(?<=gcodes=)\d+", task['url']).group()
    ret = [(burl(code), task['price'], stock)]
    fret = format_price(ret)
    return fret