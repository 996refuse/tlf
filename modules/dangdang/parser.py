#-*-encoding=utf-8-*-
import lxml
from lxml import etree
import async_http
from spider import log_with_time
from spider import jsonp_json
from spider import format_price
import pdb
import re
import json
import time

import cProfile as profile

pr = profile.Profile()

bookurl = 'e.dangdang.com'
normurl = 'category.dangdang.com'
itemurl = 'http://product.dangdang.com/%s.html'

def cats_parser(url, content, rule):
    content = content.decode("gbk")
    t = etree.HTML(content)
    ret = []
    for i in t.xpath(rule):
        if not 'http' in i:
            continue
        if 'category_path' in i:
            cat = re.search("(?<=category_path=).+", i).group()
            i = 'http://' + normurl + '/cp' + cat + '.html'
        ret.append(i)
    return list(set(ret))

def test_cats(res):
    assert(len(res) > 1500)

#f = open("/home/cc/log", "a")
def pager(task, rule):
    try:
        content = task['text'].decode("gbk", 'replace')
        t = etree.HTML(content)
    except:
        #pdb.set_trace()
        log_with_time("bad response %s"%task['url'].decode('utf-8', 'replace'))
        return
    ret = []
    #pdb.set_trace()

    url = task['url']
    url = url[:url.find(".htm")]
    if bookurl in task['url']:
        urule1,urule2 = rule['book'], rule['norm']
        padmethod = url + "_%s_saleWeek_1.htm"
    else:
        urule1,urule2 = rule['norm'], rule['book']
        padmethod = url + '-pg%s.html'

    pagecount = t.xpath(urule1)

    if not pagecount:
        pagecount = t.xpath(urule2)
        if not pagecount:
            log_with_time("bad rule %s"%task['url'].decode('utf-8', 'replace'))
            return
    pagecount = pagecount[0]
    if type(pagecount) == lxml.etree._Element:
        pagecount = pagecount.text
    #pdb.set_trace()
    pagecount = re.search("\d+", pagecount)
    if not pagecount:
        log_with_time("bad rule %s"%task['url'].decode('utf-8', 'replace'))
        return
    pagecount = int(pagecount.group())
    for i in range(1, pagecount+1):
        ret.append(padmethod % str(i))
    return ret

# for ebooks (stock==1)
_re_b1_gid = re.compile("(?<=product_id=)\d+")
_re_b1_price = re.compile("\d+\.\d+")
def __book_list_parser1(t, task, rule):
    nodes = t.xpath(rule['ebook'])
    ret = []
    #pdb.set_trace()
    for node in nodes:
        gid = node.xpath(rule['gid']['ebook'])
        price = node.xpath(rule['price']['ebook'])
        if not gid or not price:
            log_with_time("bad rule %s"%task['url'])
            continue
        gid = _re_b1_gid.search(gid[0]).group()
        price = _re_b1_price.search(price[0].text).group()
        ret.append((gid, price, 1))
    return ret

_re_b2_price = re.compile("\d+\.\d+|\d+")
def __book_list_parser2(t, task, rule):
    nodes = t.xpath(rule['book'])
    ret = []
    for node in nodes:
        gid = node.attrib['id']
        price = node.xpath(rule['price']['book'])
        if not price:
            log_with_time("bad response %s"%task['url'])
            continue
        try:
            price = _re_b2_price.search(price[0].text).group()
        except:
            log_with_time("bad regex %s"%task['url'])
            continue
        stock = node.xpath(rule['stock']['book'])
        if not stock:
            log_with_time("bad rules %s"%task['url'])
            continue
        stock = stock[0]
        st = 1 if 'AddToShoppingCart' in stock else 0
        ret.append((gid, price, st))
    return ret

_re_n1_gid = re.compile("\d+(?=.htm)")
def __norm_list_parser1(t, task, rule):
    for r in (rule['norm1'], rule['norm2']):
        nodes = t.xpath(r)
        if nodes: break
    if not nodes: return []
    ret = []
    for node in nodes:
        price = node.xpath(rule['price']['norm'])
        if not price:
            continue
        price = _re_b2_price.search(price[0].text).group()
        gid = node.xpath(rule['gid']['norm'])
        gid = _re_n1_gid.search(gid[0]).group()
        ret.append((gid, price, 1))
    return ret

def list_parser(task, rule):
    #pr.enable()
    try:
        t = etree.HTML(task['text'].decode('gbk', 'replace'))
    except:
        log_with_time("bad response %s"%task['url'])
        return
    ret = []
    if bookurl in task['url']:
        ret = __book_list_parser1(t, task, rule)
    elif 'cp' in task['url']:
        ret = __book_list_parser2(t, task, rule)
    else:
        ret = __norm_list_parser1(t, task, rule)
    #pr.disable()
    #pr.print_stats()
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = int(time.time())
    return {"result": fret, "stock": [], "dps": dps}

def stock_parser(task, rule):
    try:
        j = json.loads(task['text'])
        stock = 1 if j['havestock'] in ("true", "realstock") else 0
    except:
        log_with_time("bad response %s"%task['url'])
        return

    ret = [(itemurl % task['info'][0], task['info'][1], stock)]
    fret = format_price(ret)
    return fret
