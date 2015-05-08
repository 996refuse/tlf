#-*-encoding=utf-8-*-
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json
import _tess
import time

_tess.set_config({"datadir": "/usr/share/tessdata", "lang": "eng"})

url = 'http://www.360kxr.com'
def mcats_parser(url, content, rule):
    t = etree.HTML(content)
    return [url + i for i in t.xpath(rule)]

def scats_parser(task, rule):
    if 'category' in task['url']:
        return [task['url']]
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['maincats'])
    if not nodes:
        nodes = t.xpath(rule['subcats'])
    return [url + i for i in nodes]

pagerburl = 'http://www.360kxr.com/category/'
re_cat = re.compile("(?<=category/)[0-9]+(?=-)")
def pager(task, rule):
    bpath = '-1-4-2-2-0,999999-all-9-all-all-all-'
    cat = re_cat.search(task['url'])

    t = etree.HTML(task['text'])
    pagenum = t.xpath(rule)

    ret = []

    if not cat:
        log_with_time("bad response %r" % task['url'])
        return ret

    cat = cat.group()

    if not pagenum:
        pagenum = 1
    else:
        pagenum = int(re.search("\d+", pagenum[0].text).group())
    ret.append(task['url'])
    for i in range(2, pagenum+1):
        ret.append(pagerburl + cat + bpath + str(i) + '.html')
    return ret

listburl = "http://www.360kxr.com"
def list_parser(task, rule):
    t = etree.HTML(task['text'])
    nodes = t.xpath(rule['nodes1'])
    if not nodes:
        #pdb.set_trace()
        nodes = t.xpath(rule['nodes2'])
    ret = []
    for node in nodes:
        gid = node.xpath(rule['gid'])
        priceimg = node.xpath(rule['priceimg'])
        stock = node.xpath(rule['stock'])
        if not gid or not priceimg:
            log_with_time("bad response %r"%task['url'])
            continue
        gid = gid[0]
        priceimg = priceimg[0]
        if stock:
            stock = 1
        else:
            stock = 0
        ret.append((listburl+gid, priceimg, stock))
    return ret

def test_list(res):
    assert(res[0][1])

def price_parser(task, rule):
    price = _tess.recognize(task['text'], _tess.IMAGE_PNG, 32)
    try:
        price = re.search("\d+\.\d+|\d+", price).group()
    except:
        log_with_time("bad price: %s" % task['url'])
        return
    ret = [(task['gid'], price, task['stock'])]
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = time.time()
    return {"result":fret, "dps": dps}