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

yougou = 'http://www.yougou.com'

def cats(url, content, rule):
	try:
		t = etree.HTML(content)
	except:
		log_with_time("bad response %s"%content.decode('utf-8', 'replace'))
		return
	ret = []
	for i in t.xpath(rule):
		ret.append(yougou + i)
	return ret

def pager(task, rule):
	try:
		t = etree.HTML(task['text'])
	except:
		log_with_time("bad response %s"%task['url'])
		return
	page = t.xpath(rule)
	if not page:
		log_with_time("bad rule %s"%task['url'])
		return
	ret = []
	page = page[0].text
	pagecount = page.split("/")[-1]
	if not pagecount:
		log_with_time("bad response %s"%content)
		return
	pagecount = int(pagecount)
	url = task['url'].replace(".html", "")
	for i in range(1, pagecount+1):
		ret.append(url + '-' + str(i) +".html")
	return ret

def list_parser(task, rule):
	try:
		t = etree.HTML(task['text'])
		nodes = t.xpath(rule['nodes'])
	except:
		log_with_time("bad response %s"%task['url'])
		return
	if not nodes:
		log_with_time("bad rule %s"%task['url'])
		return
	ret = []
	for node in nodes:
		gid = node.xpath(rule['gid'])
		gurl = node.xpath(rule['gurl'])
		price = node.xpath(rule['price'])
		if not gid or not gurl or not price:
			log_with_time("bad rule %s"%task['url'])
			continue
		ret.append((gid[0], gurl[0], price[0]))
	return ret

def stock_parser(task, rule):
	try:
		j = json.loads(task['text'])
	except:
		log_with_time("bad response %s"%task['url'])
		return
	ret = []
	inv = j.get('inventory')
	stock = sum(v for k,v in inv.items()) if inv else 0
	if stock: stock = 1
	ret.append((task['gurl'], task['price'], stock))
	fret = format_price(ret)
	dps = {}
	for i in fret:
		dps[i[1]] = int(time.time())
	return {"result":fret, "dps":dps}
