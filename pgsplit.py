#!/usr/bin/python3
#-*- coding:utf-8 -*-
import re
import os
import sys
import math
import aiohttp
import asyncio
import argparse
import functools

from lxml import etree

import pdb

def pagespliter(cls):
	class PageSpliter(cls):
		urltmpl = ""
		rules = ""
		def __init__(self, loop=None):
			cls.__init__(self)
			self.threshold = cls.threshold
			self.scale = cls.scale
			self.rules = cls.rules
			self.urltmpl = cls.urltmpl
			self.cids = {}
			self.session = aiohttp.ClientSession()

			self.sem = asyncio.Semaphore(128)
			self.eloop = loop if loop else asyncio.get_event_loop()

		def set(self, cids): self.cids = set(cids)

		@asyncio.coroutine
		def get(self, url, cb, *args, **kwargs):
			empty_html = '<html><body></body></html>'
			SpliterResponse = type('SpliterResponse', (), {})
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
				res = SpliterResponse()
				res.itemcount, res.pagecount = rr['itemcount'], rr['pagecount']
				if res.pagecount is None:
					res.status = None
					res.pagecount = 0
				elif res.pagecount < th:
					res.status = True
				else:
					res.status = False
				return res
			t = self.eloop.create_task(_get(url))
			return (yield from t)

		@asyncio.coroutine
		def read(self):
			if not self.cids: return None
			cid = self.cids.pop()
			ret = yield from self.split(cid)
			return cid, ret

		@asyncio.coroutine
		def split(self, cid, sprice=32, hmax = 10000):
			sc = lambda x: float(x * self.scale)
			@asyncio.coroutine
			def stepget(cid):
				sg = stepget
				lp,st = sg.lp, 2 ** (sg.th - 1 if sg.th else 0)
				#print("stepget:", sc(lp), sc(lp+st-1))
				l, h = sc(lp), sc(lp + st - 1)
				res = yield from self.get(self.url(cid, l, h), self.check)
				r = res.status
				if r is None: return res, 0, 0
				if not r and st == 1: r = True
				if r:
					sg.th += 1
					if sg.pa: sg.th += sg.pa
					sg.cm = 0
					sg.pa += 1
					print("stepget: ", lp, st)
					sg.lp += (st - 1 if st > 1 else st)
				else:
					sg.th -= 1
					if sg.cm: sg.th -= sg.cm
					if sg.th < 0: sg.th = 0
					sg.pa = 0
					sg.cm += 1
				return res, l, h

			stepget.th = int(math.log(sprice / self.scale, 2))
			stepget.pa = 0
			stepget.cm = 0
			stepget.lp = 0

			ret = []
			hmin = hmax // 4

			r, l, h = yield from stepget(cid)
			if r.status is None: return None
			while (not r.status or sc(h) < hmin) and sc(h) < hmax:
				print("--:", cid, l, h, r.pagecount, r.status)
				if r.status == True or l == h:
					print("result.append:",cid,l,h)
					ret.append([l, h, r.pagecount])
				r, l, h = yield from stepget(cid)
			else:
				print("result.append:",cid,l,h)
				ret.append([l, h, r.pagecount])

			r = yield from self.get(self.url(cid, h, -1), self.check)
			ret.append([h, -1, r.pagecount])
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
	return PageSpliter

@pagespliter
class DangDangPageSpliter:
	urltmpl = "http://category.dangdang.com/%s-lp%s-hp%s.html"
	rules = {
		"pagecount": "//div[@class='page' or @class='data']/span[3]/text()",
		"itemcount": "//div[@class='page' or @class='data']/span[1]/text()",
	}
	threshold = 100
	scale = 0.1

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
		lp = "" if lp == -1 else '%.1f' % lp
		hp = "" if hp == -1 else '%.1f' % hp
		url = self.urltmpl % (cid, lp, hp)
		#print(url, lp, hp)
		return url

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
	f.write('#' + s.url(c, -1, -1) + '\n')
	for i in r:
		f.write(s.url(c, i[0], i[1]) + ';' + str(i[2]*60) + '\n')
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
	#cids = {'cp01.58.01.00.00.00'}

	if args.type == 'dangdang':
		ps = DangDangPageSpliter()
	else:
		sys.exit("Invalid backend type.")

	reader = SpliterReader(ps)
	reader.loop(cids, ondata=functools.partial(dump, output))
