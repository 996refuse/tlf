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

itemurl = 'http://sh.womai.com/Product-100-%s.htm'

def pager(url, content, rule):
	try:
		t = etree.HTML(content)
	except:
		log_with_time("bad response %s"%url.decode('utf-8', 'replace'))
		return
	page = t.xpath(rule)
	if not page:
		log_with_time("bad rule %s"%url.decode("utf-8", "replace"))
		return
	ret = []
	page = page[0].text
	pagecount = re.search("\d+", page)
	if not pagecount:
		log_with_time("bad regex %s"%content)
		return
	pagecount = int(pagecount.group())
	for i in range(1, pagecount+1):
		ret.append(url + "?page=" + str(i))
	return ret

re_gid = re.compile("\d+")
def list_parser(task, rule):
	try:
		t = etree.HTML(task['text'])
		nodes = t.xpath(rule['item'])
	except:
		log_with_time("bad response %s"%task['url'])
		return
	if not nodes:
		log_with_time("bad rule %s"%task['url'])
		return
	ret = []
	dps = {}
	for node in nodes:
		gid = re_gid.search(node.attrib.get('id', ""))
		if not gid:
			log_with_time("bad regex %s"%task['url'])
			continue
		gid = gid.group()
		ret.append(gid)
		dps[gid] = int(time.time())
	return {"stock": ret, "dps": dps}

def stock_parser(task, rule):
	try:
		txt = task['text']
		txt = txt[txt.find("(")+1:txt.rfind(")")]
		nodes = json.loads(txt.decode('gbk'))['result']
	except:
		log_with_time("bad response %s"%task['url'])
	ret = []
	for i in nodes:
		gid = i['id']
		try:
			price = i['price']['buyPrice']['priceValue']
		except:
			price = -1
		stock = 1 if i['sellable'] else 0
		ret.append((itemurl%gid, price, stock))
	fret = format_price(ret)
	return fret
