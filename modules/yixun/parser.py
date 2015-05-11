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

def cats(url, content, rule):
	content = content.decode("gbk", "replace")
	t = etree.HTML(content)
	return ['http://searchex.yixun.com/705798t706810-1-/']
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
	fret = format_price(ret)
	dps = {}
	for i in fret:
		dps[i[1]] = int(time.time())
	return {"result":fret, "dps":dps}