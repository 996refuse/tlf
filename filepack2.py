import redis
import datetime
import time 
import hashlib
import pdb
import os
import msgpack
from urlcrc import get_urlcrc 
from struct import pack, unpack
import io

INSERT_IDX = "insert into idx (site_id, url_crc, offset, size, update_time, data_file, url) values (%s, %s, %s, %s, '%s', '%s', '%s')"

INSERT_DATA_FILE = "insert into data_file (site_id, data_file,  status, compress, update_time) values(%s, '%s', %s, %s, '%s')" 

class FilePack: 
    def __init__(self, db, site_id, limit=1000, datadir="/tmp/"):
        self.b = []
        self.meta = []
        self.limit = int(limit)
        self.cnt = 0
        self.idx = 0
        self.datadir = datadir 
        self.db = db 
        self.site_id = int(site_id)
        self.rdb = redis.StrictRedis(**db) 


    def add(self, name, content, crc=None):
        if not name or not content:
            return 
        assert len(name) < 103
        m = {
            "title": name,
            "size": len(content),
            "offset": self.idx, 
            "date_time": int(time.time())
            } 
        if crc:
            m["crc"] = int(crc) 
        else:
            m["crc"] = get_urlcrc(self.site_id, name), 
        self.meta.append(m)
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
        

    def _gen_idx(self):
        n_entry = len(self.meta)
        entry_size = 128 
        magic = "gwd\x00"
        version = 1 
        data_offset = n_entry * entry_size + 16 
        self.data_offset = data_offset
        h = [magic, pack("I", version),
            pack("I", n_entry),
            pack("I", entry_size)] 
        for i in self.meta:
            h.extend((
                pack("I", self.site_id),
                pack("I", i["date_time"]),
                pack("q", i["crc"]), 
                pack("I", i["offset"] + data_offset),
                pack("I", i["size"]))) 
            short = i["title"][:103] 
            h.append(short + (104 - len(short)) * "\x00") 
        h.extend(self.b) 
        self.b = h 


    def flush(self): 
        if not self.b:
            return
        self._gen_idx()
        content = "".join(self.b) 
        h = hashlib.sha1(content).hexdigest() 
        f = open(os.path.join(self.datadir, h), "w+") 
        f.write(content)
        f.close()
        i = 0
        now = datetime.datetime.strftime(datetime.datetime.now(),
                '%Y-%m-%d %H:%M:%S') 
        sqls = []
        for i in self.meta:
            sql = INSERT_IDX % (self.site_id, 
                    i["crc"], i["offset"] + self.data_offset,
                    i["size"], now,
                    h,  i["title"])
            sqls.append(sql) 
        sqls.append(INSERT_DATA_FILE % (self.site_id, h, 0, 0, now))
        self.rdb.rpush("dp_idx", msgpack.packb(sqls)) 
        self.clear() 



class FileUnpack:
    def __init__(self, data_file, datadir="/tmp"): 
        self.data_file = os.path.join(datadir, data_file)
        self.fobj = open(self.data_file) 
        self.magic = self.fobj.read(4)
        assert self.magic == "gwd\x00"
        self.version = unpack("I", self.fobj.read(4))[0]
        self.n_entry = unpack("I", self.fobj.read(4))[0]
        self.entry_size = unpack("I", self.fobj.read(4))[0] 
        self.data_offset = self.fobj.tell()


    def get_file(self, meta):
        d = meta.copy()
        self.fobj.seek(meta["offset"], io.SEEK_SET)
        d["data"] = self.fobj.read(meta["size"])
        return d


    def _parse_meta(self, meta_str): 
        site_id = unpack("I", meta_str[0:4])[0]
        date_time = unpack("I", meta_str[4:8])[0]
        crc = unpack("q", meta_str[8:16])[0] 
        offset = unpack("I", meta_str[16:20])[0]
        size = unpack("I", meta_str[20:24])[0]
        url = meta_str[24:].strip("\x00")
        return {
            "site_id": site_id,
            "date_time": date_time,
            "crc": crc,
            "offset": offset,
            "size": size,
            "url": url
            } 


    def get_idx(self):
        self.fobj.seek(self.data_offset, io.SEEK_SET)
        files = []
        for i in range(self.n_entry):
            meta_str = self.fobj.read(self.entry_size)
            assert len(meta_str) == self.entry_size
            files.append(self._parse_meta(meta_str))
        return files 
