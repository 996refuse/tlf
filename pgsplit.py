#!/usr/bin/python3
#-*- coding:utf-8 -*-
import re
import os
import sys
import aiohttp
import asyncio
import argparse
import functools

from lxml import etree

import pdb

class pagespliter(object):
	urltmpl = ""
	rules = ""
	def __init__(self, thr, loop=None):
		self.threshold = thr
		self.cids = {}
		self.session = aiohttp.ClientSession()

		self.sem = asyncio.Semaphore(128)
		self.eloop = loop if loop else asyncio.get_event_loop()

	def check(self, txt):
		raise Exception("should be implemented in subclass.")

	def url(self, cid, lp, hp, *args, **kwargs):
		raise Exception("should be implemented in subclass.")

	def set(self, cids): self.cids = set(cids)

	@asyncio.coroutine
	def get(self, url, cb, *args, **kwargs):
		empty_html = '<html><body></body></html>'
		@asyncio.coroutine
		def _get(url):
			retry = 8
			while retry:
				try:
					with (yield from self.sem):
						r = yield from asyncio.wait_for(self.session.request('get', url), 10)
						t = yield from asyncio.wait_for(r.text(), 10)
					break
				except Exception as e:
						print('Exception:', e, url)
						t = empty_html
						retry -= 1
				yield from asyncio.sleep(2)
				print("retry: %s"%(8-retry), url)
			th= self.threshold
			rr= cb(t, *args, **kwargs)
			itemcount, pagecount = rr['itemcount'], rr['pagecount']
			if pagecount is None: return None, 0
			return (True if pagecount < th else False), pagecount
		t = self.eloop.create_task(_get(url))
		return (yield from t)

	@asyncio.coroutine
	def read(self):
		if not self.cids: return None
		cid = self.cids.pop()
		ret = yield from self.split(cid)
		return cid, ret

	@asyncio.coroutine
	def split(self, cid, hmax = 5000):
		@asyncio.coroutine
		def stepget(cid):
			sg = stepget
			lp,st = sg.lp, 2 ** (sg.th - 1 if sg.th else 0)
			r,t = yield from self.get(self.url(cid, lp, lp+st-1), self.check)
			if r is None: return None, 0
			if not r and st == 1: r = True
			if r:
				sg.th += 1
				if sg.pa: sg.th += sg.pa
				sg.cm = 0
				sg.pa += 1
				sg.lp += (st - 1 if st > 1 else st)
			else:
				sg.th -= 1
				if sg.cm: sg.th -= sg.cm
				if sg.th < 0: sg.th = 0
				sg.pa = 0
				sg.cm += 1
			return r, t, lp, lp + st - 1

		stepget.th = 6
		stepget.pa = 0
		stepget.cm = 0
		stepget.lp = 0

		ret = []
		hmin = hmax // 4

		r, t, l, h = yield from stepget(cid)
		if r is None: return None
		while (not r or h < hmin) and h < hmax:
			print("--:", l, h, t, r)
			if r == True:
				print("result.append:",cid,l,h)
				ret.append([l, h, t])
			r, t, l, h = yield from stepget(cid)
		else:
			print("result.append:",cid,l,h)
			ret.append([l, h, t])

		r,t = yield from self.get(self.url(cid, h, -1), self.check)
		ret.append([h, -1, t])
		print(cid, ret)
		return self._format(ret, self.threshold)

	def _format(self, lst, th):
		ret = []
		p = lst.pop(0)
		for i,v in enumerate(lst):
			if p[2] + v[2] > th:
				ret.append(p)
				p = v
			else:
				p[1] = v[1]
				p[2] += v[2]
		ret.append(p)
		print(ret)
		return ret

class DangDangPageSpliter(pagespliter):
	urltmpl = "http://category.dangdang.com/%s-lp%s-hp%s.html"
	rules = {
		"pagecount": "//div[@class='page' or @class='data']/span[3]/text()",
		"itemcount": "//div[@class='page' or @class='data']/span[1]/text()",
	}

	def __init__(self, thr, loop=None):
		pagespliter.__init__(self, thr, loop)
		self.urltmpl = DangDangPageSpliter.urltmpl
		self.rules = DangDangPageSpliter.rules
		self.threshold = thr

	def check(self, txt):
		rules = self.rules
		t = etree.HTML(txt)
		pagecount = t.xpath(rules['pagecount'])
		itemcount = t.xpath(rules['itemcount'])
		pagecount = int(re.search("\d+", pagecount[0]).group()) if pagecount else None
		itemcount = int(re.search("\d+", itemcount[0]).group()) if itemcount else None
		if not itemcount: pagecount = 0
		return {"pagecount": pagecount, "itemcount": itemcount}

	def url(self, cid, lp, hp):
		if hp == -1: hp = ""
		return self.urltmpl % (cid, lp, hp)

class SpliterReader(object):
	def __init__(self, spliter, cids=set(), maxconn=64):
		self.spliter = spliter
		self.cids = cids
		self.maxconn = maxconn
		self.eloop = spliter.eloop
		self.readers = set()

	def add_reader(self, cid, cb):
		@asyncio.coroutine
		def reader(cid):
			return (yield from self.spliter.split(cid))
		t = self.eloop.create_task(reader(cid))
		t.add_done_callback(functools.partial(self.ondata, cb, cid))
		self.readers.add(t)
	
	def ondata(self, cb, cid, future):
		print("====== tol readers: %s , %s ======" % (len(self.readers), cid))
		self.readers.remove(future)
		r = future.result()
		if cb and r: cb(self.spliter, cid, r)
		if self.cids:
			print("=== tol cids %s ===" % len(self.cids))
			self.add_reader(self.cids.pop(), cb)
		if not self.readers:
			self.eloop.stop()

	def loop(self, cids, ondata=None):
		self.cids |= set(cids)
		for i in range(self.maxconn):
			print("=== tol cids %s ===" % len(self.cids))
			if not self.cids: break
			self.add_reader(self.cids.pop(), ondata)
		self.eloop.run_forever()

parser = argparse.ArgumentParser(prog="pagespliter")
parser.add_argument("infile", nargs=1, help="select input file")
parser.add_argument("-o", "--output", nargs="?", help="output file")
parser.add_argument("-t", "--type", nargs=1, help="backend type(dangdang, jd)")

def dump(f, s, c, r):
	f.write('#' + s.url(c, "", "") + '\n')
	for i in r:
		f.write(s.url(c, i[0], i[1]) + '\n')
	f.flush()

if __name__ == "__main__":
	args = parser.parse_args(sys.argv[1:])

	if not args.type:
		sys.exit("Invalid backend type.")

	args.type = args.type[0]
	output = open(args.output, 'w+') if args.output else sys.stdout
	
	infile = open(args.infile[0], 'r+')
	cids = set(infile.read(-1).split("\n"))
	cids.remove('')

	#cids = {'cp01.31.01.00.00.00'}

	if args.type == 'dangdang':
		ps = DangDangPageSpliter(100)
	else:
		sys.exit("Invalid backend type.")

	reader = SpliterReader(ps)
	reader.loop(cids, ondata=functools.partial(dump, output))
