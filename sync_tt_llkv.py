import llkv
import re
import ctypes
import struct
import pdb
import io
import os 


list_server = ("192.168.1.194", 8000)
dp_server = ("192.168.1.194", 8001)

dp_pattern = re.compile("[0-9]+\t([0-9]+)\t([\-0-9]+)\t") 
list_pattern = re.compile("([0-9\-]+)\t<p>([0-9\-]+)</p><s>([0-9\-]+)</s>") 


def dp_store(to, item): 
    site_id, crc = int(item[0]), int(item[1]) 
    if site_id > 0xffff or site_id < 0:
        print "overflow", item 
        return 
    key = (int(site_id) << 48) |ctypes.c_uint(int(crc)).value 
    to[key] = 0 


def list_store(to, item): 
    key, price, stock = item
    try:
        key = key_to_ulong(key) 
        value = price_stock_ulong(price, stock)
    except ValueError:
        print "garbage", repr(item) 
        return
    if not key or not value:
        return
    to[key] = value 


def key_to_ulong(key):
    u = key.rfind("-")
    site_id = int(key[u+1:])
    crc = int(key[:u]) 
    if crc > 0xffffffffffff or site_id > 0xffff:
        print "overflow: %s" % key
        return 
    return (site_id << 48) | ctypes.c_uint(crc).value 


def price_stock_ulong(price, stock): 
    try:
        price = int(price)
        stock = int(stock) 
    except ValueError:
        return
    if stock > 0:
        stock = 1
    if stock < 0:
        stock = 0
    if price < 0:
        price = 0
    if price > 0x7fffffffffffffff: 
        print "overflow", price , stock
        return
    value =  price | (int(stock) << 63)                
    return value 
    

def reset_file_ptr(fileobj): 
    if os.path.exists("llkv.dp.ptr"):
        fileobj.seek(int(open("llkv.dp.ptr").read())) 



def load(path, server, pat, store_fn): 
    m10 = 1024 * 1024 * 100
    cnt = 0
    fobj = open(path)
    #reset_file_ptr(fobj)
    con = llkv.Connection(*server)
    while True: 
        data = fobj.read(m10) 
        lastline = data.rfind("\n")
        if lastline <= 0: 
            break 
        fobj.seek(lastline - len(data), io.SEEK_CUR)
        result = pat.findall(data) 
        print "got items: ", len(result)
        to = {}
        pack = struct.pack
        for item in result:
            store_fn(to, item)
            if len(to) == 1000:
                cnt += 1000
                con.multi_set(to)
                to = {} 
        if to:
            cnt += len(to)
            con.multi_set(to) 
        print "current:", cnt
    ptr = open("llkv.dp.ptr", "w+")
    ptr.write(str(fobj.tell()))
    ptr.close()
    con.close() 
    fobj.close()




def get_key(server, key):
    key = key_to_ulong(key)
    con = llkv.Connection(*llkv_server)
    value = con.get(key)
    if not value:
        return key, None, None
    stock = value >> 63
    price = value & 0x7fffffffffffffff
    return key, price, stock



def sync_dp_idx():
    import MySQLdb
    db = {
            "host": "192.168.1.192",
            "port": 3306,
            "db": "dp_idx",
            "user": "minishop",
            "passwd": "MiniShop!@#"
            } 
    ll = llkv.Connection(*dp_server)
    con = MySQLdb.connect(**db)
    cur = con.cursor()
    print "loading from dp_idx"
    cur.execute("select url_crc, site_id from idx")
    from ctypes import c_uint 
    keys = []
    cnt = 0
    for crc, site_id in  cur.fetchall(): 
        key = (site_id << 48) | c_uint(crc).value 
        keys.append((key, 0))
        if len(keys) > 1000: 
            cnt += len(keys)
            print "current", cnt
            ll.multi_set(dict(keys)) 
            keys = []
    ll.close()
    con.close()




def main(): 
    import sys
    if sys.argv[1] == "dp":
        sync_dp_idx()
        load("/pub_file/last_url.txt", dp_server, dp_pattern, dp_store)
    elif sys.argv[1] == "list":
        load("/tmp/llkv.list", list_server, list_pattern, list_store) 
    elif sys.argv[1] == "get":
        print get_key(sys.argv[2])
    else:
        print """
        dp    load /tmp/llkv.dp
        list  load /tmp/llkv.list
        get key
        """ 


if __name__ == "__main__":
    main()

