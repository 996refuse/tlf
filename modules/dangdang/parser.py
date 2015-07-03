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

ebookurl = 'e.dangdang.com'
normurl = 'category.dangdang.com'
itemurl = 'http://product.dangdang.com/%s.html'

def cats_parser(url, res, rule):
    content = res['text']
    content = content.decode("gbk")
    t = etree.HTML(res['text'])
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

# f0 = open("log.0", "a")
# f1 = open("log.1", "a")
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
    if ebookurl in task['url']:
        padmethod = url + "_%s_saleWeek_1.htm"
    else:
        padmethod = url + '-pg%s.html'

    pagecount = t.xpath(rule['norm'])

    if not pagecount:
        pagecount = t.xpath(rule['ebook'])
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
    # if pagecount >= 100:
    #     cat = re.search("(?<=com/).+(?=\.htm)", task['url']).group()
    #     itc = t.xpath("//div[@class='page' or @class='data']/span[1]/text()")
    #     itc = int(re.search("\d+", itc[0]).group()) if itc else 0
    #     f0.write(cat + '\n')
    #     f0.flush()
    #     f1.write(cat + ';' + str(itc) + '\n')
    #     f1.flush()
    for i in range(1, pagecount+1):
        ret.append(padmethod % str(i))
    return ret

dp_base = "http://product.dangdang.com/%s.html"

# for ebooks (stock==1)
_re_b1_gid = re.compile("(?<=product_id=)\d+")
_re_b1_price = re.compile("\d+\.\d+")
def __book_list_parser1(t, task, rule):
    nodes = t.xpath(rule['ebook'])
    ret = []
    comments = {}
    dp = []
    for node in nodes:
        gid = node.xpath(rule['gid']['ebook'])
        price = node.xpath(rule['price']['ebook'])
        if not gid or not price:
            log_with_time("bad rule %s"%task['url'])
            continue
        gid = _re_b1_gid.search(gid[0]).group()
        price = _re_b1_price.search(price[0].text).group()
        ret.append((str(gid), str(price), 1)) 
        comment = node.xpath(rule['comment']) 
        if not comment:
            comment = ["0"]
        else:
            comment = re.findall("([0-9]+)", comment[0])
        comments[gid] = comment[0] 
        dp.append((dp_base % gid, ""))
    return ret, comments, None, dp

_re_b2_gid = re.compile("(?<=com/).+(?=.htm)")
_re_b2_price = re.compile("\d+\.\d+|\d+")
def __book_list_parser2(t, task, rule):
    nodes = t.xpath(rule['book'])
    ret = []
    comments = {}
    shop = {}
    dp = []
    for node in nodes:
        gid = node.xpath(rule['gid']['norm'])
        price = node.xpath(rule['price']['book'])
        if not price or not gid:
            log_with_time("bad response %s"%task['url'])
            continue
        try:
            gid = _re_b2_gid.search(gid[0]).group()
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
        ret.append((str(gid), str(price), st)) 
        comment = node.xpath(rule['comment']) 
        if not comment:
            comment = ["0"]
        else:
            comment = re.findall("([0-9]+)", comment[0])
        comments[gid] = comment[0] 
        dp.append((dp_base % gid, ""))
        store_link = node.xpath(rule["store_normal"]) 
        if store_link: 
            title = store_link[0].attrib["title"]
            store_id = re.findall("com/([0-9]+)", store_link[0].attrib["href"])[0]
            shop[gid] = "%s,%s" % (store_id, title) 
    return ret, comments, shop, dp

_re_n1_gid = re.compile("\d+(?=.htm)")
def __norm_list_parser1(t, task, rule):
    for r in (rule['norm1'], rule['norm2']):
        nodes = t.xpath(r)
        if nodes: break
    if not nodes: return []
    ret = []
    comments = {}
    shop = {}
    dp = []
    for node in nodes:
        price = node.xpath(rule['price']['norm'])
        if not price:
            continue
        price = _re_b2_price.search(price[0].text).group()
        gid = node.xpath(rule['gid']['norm'])
        gid = _re_n1_gid.search(gid[0]).group()
        ret.append((str(gid), str(price), 1))
        comment = node.xpath(rule['comment']) 
        if not comment:
            comment = ["0"]
        else:
            comment = re.findall("([0-9]+)", comment[0])
        comments[gid] = comment[0] 
        dp.append((dp_base % gid, ""))
        store_link = node.xpath(rule["store_normal"]) 
        if store_link: 
            title = store_link[0].attrib["title"]
            store_id = re.findall("com/([0-9]+)", store_link[0].attrib["href"])[0]
            shop[gid] = "%s,%s" % (store_id, title)
    return ret, comments, shop, dp

def list_parser(task, rule):
    #pr.enable()
    try:
        t = etree.HTML(task['text'].decode('gbk', 'replace'))
    except:
        log_with_time("bad response %s"%task['url'])
        return
    ret = [] 
    if ebookurl in task['url']:
        r = __book_list_parser1(t, task, rule)
    elif 'cp' in task['url']:
        r = __book_list_parser2(t, task, rule)
    else:
        r = __norm_list_parser1(t, task, rule)
    ret, comments, shop, dp = r 
    #pr.disable()
    #pr.print_stats()
    fret = format_price(ret)
    dps = {}
    for i in fret:
        dps[i[1]] = int(time.time())
    return {
            "result": fret, 
            "dps": dps,
            "shop": shop,
            "comment": comments,
            "dp": dp,
            }

def stock_parser(task, rule):
    try:
        j = json.loads(task['text'])
        stock = 1 if j['havestock'] in ("true", "realstock") else 0
    except:
        log_with_time("bad response %s"%task['url'])
        return

    ret = [(itemurl % task['info'][0], str(task['info'][1]), stock)]
    fret = format_price(ret)
    return fret

def offcheck_test(items):
    pdb.set_trace()


def checkoffline(task, rule): 
    try:
        j = json.loads(task['text'])
        j = j['items']
    except:
        log_with_time("bad response %s"%task['url'])
        return
    ret = []
    for k,v in j.items():
        if not v['is_found']:
            ret.append((str(k), str(-1), -1))
    fret = format_price(ret)
    return fret
