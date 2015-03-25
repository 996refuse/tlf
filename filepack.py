import MySQLdb
import datetime
import time 
import hashlib
import pdb
import os
from urlcrc import get_urlcrc


INSERT_IDX = "insert into idx (site_id, url_crc, offset, size, update_time, data_file, url, done, compress) values (%s, %s, %s, %s, '%s', '%s', '%s', 0, 0)"


class FilePack: 
    def __init__(self, db, limit=1000, datadir="/tmp/"):
        self.b = []
        self.meta = []
        self.limit = int(limit)
        self.cnt = 0
        self.idx = 0
        self.datadir = datadir 
        self.db = db 
        self.open_idx()


    def open_idx(self): 
        self.con = MySQLdb.connect(**self.db)
        self.cur = self.con.cursor() 
        self.cur.execute("set autocommit=0") 


    def close_idx(self):
        try:
            self.con.close()
        except Exception as e:
            print "close idx failed: %s" % e


    def add(self, site_id, name, content):
        if not name or not content:
            return
        self.meta.append({
            "title": name,
            "size": len(content),
            "offset": self.idx, 
            "crc": get_urlcrc(site_id, name),
            "site_id": site_id,
            }) 
        self.b.append(content)
        self.idx += len(content)
        self.cnt += 1
        if self.cnt >= self.limit:
            self.flush() 


    def clear(self):
        self.b = []
        self.meta = []
        self.limit = self.limit
        self.cnt = 0
        self.idx = 0 
        

    def _safe_insert(self, sql):
        while True:
            try:
                self.cur.execute(sql)
                break
            except Exception as e:
                print("%r %r"%(e, e.args))
                if len(e.args) <= 1:
                    print "_safe_insert bug: %s" % e
                    return
                msg = e.args[1]
                if ("gone away" in msg or "lost" in msg):
                    self.open_idx() 
            time.sleep(1)

    def _safe_commit(self): 
        while True:
            try:
                self.con.commit()
                break
            except Exception as e:
                if len(e.args) <= 1:
                    print "_safe_insert bug: %s" % e
                    return
                msg = e.args[1]
                if ("gone away" in msg or "lost" in msg):
                    self.open_idx()
            time.sleep(1) 


    def flush(self): 
        content = "".join(self.b) 
        h = hashlib.sha1(content).hexdigest() 
        f = open(os.path.join(self.datadir, h), "w+") 
        f.write(content)
        f.close()
        i = 0
        now = datetime.datetime.strftime(datetime.datetime.now(),
                '%Y-%m-%d %H:%M:%S') 
        for i in self.meta:
            sql = INSERT_IDX % (i["site_id"], 
                    i["crc"], i["offset"], i["size"], now,
                    h,  i["title"])
            self._safe_insert(sql) 
        self._safe_commit()
        self.clear() 


class FileUnpack:
    def __init__(self, db, datadir="/tmp"): 
        self.datadir = datadir 
        self.db = db

    def get(self, name): 
        self.cur.execute("select offset, size, data_file from idx where url = '%s'" % name)
        ret = self.cur.fetchone()
        if not ret:
            return
        offset, size, data_file = ret
        f = open(os.path.join(self.datadir, data_file))
        f.seek(offset)
        return f.read(size) 

    def open_idx(self): 
        self.con = MySQLdb.connect(**self.db)
        self.cur = self.con.cursor() 
        self.cur.execute("set autocommit=0") 


    def close_idx(self):
        try:
            self.con.close()
        except Exception as e:
            print "close idx failed: %s" % e


