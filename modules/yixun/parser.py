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

def cats(url, res, rule):
	content = res['text']
	content = content.decode("gbk", "replace")
	t = etree.HTML(content)
	return t.xpath(rule)

padurl = "all/------%s---------.html#list"
def pager(task, rule):
	try:
		t = etree.HTML(task['text'])
		page = t.xpath(rule)
	except:
		log_with_time("bad response %s"%task['url'].decode('utf-8', 'replace'))
		return
	if not page:
		log_with_time("bad rule %s"%task['url'])
		return
	ret = []
	page = etree.tostring(page[0])
	pagecount = re.search("(?<=/)\d+", page)
	if not pagecount:
		log_with_time("bad regex %s"%task['url'])
		return
	pagecount = int(pagecount.group())
	for i in range(1, pagecount+1):
		ret.append(task['url'] + padurl % str(i))
	return ret

re_gid = re.compile("(?<=item-).+(?=.htm)")
def list_parser(task, rule):
	try:
		t = etree.HTML(task['text'])
		nodes = t.xpath(rule["nodes"])
	except:
		log_with_time("bad response %s"%task['url'])
		return
	if not nodes:
		log_with_time("bad rule %s"%task['url'])
		return
	ret = []
	comments = {}
        promos = []
	for node in nodes:
		gid = node.xpath(rule["gid"])
		price = node.xpath(rule["price"])
		stock = 1 if node.xpath(rule["stock"]) else 0
		if not gid or not price:
			log_with_time("bad rule %s"%task['url'])
			continue
		gid = gid[0]
		price = price[0].text
		ret.append((gid, price, stock)) 
		comment = node.xpath(rule['comment'])
		if not comment:
			log_with_time("bad rule for comments: %s"%task['url'])
			comment = ['0']
		_gid = re_gid.search(gid).group() 
		comments[_gid] = re.search("\d+", ','.join(comment)).group()
                promos.append(_gid)
	fret = format_price(ret)
        dp = []
        for i in ret:
            dp.append((i[0], "")) 
	dps = {}
	for i in fret:
		dps[i[1]] = int(time.time())
        return {"result":fret, "dps":dps, "comment": comments, "dp": dp, "promos": promos}
