import filepack
import requests
import pdb

import MySQLdb as mysqldb

db = {"host":"127.0.0.1", "port":3306, "user":"root", "passwd":"20061992", "db":"dp_idx"}

p = filepack.FilePack(db)

p.open_idx()

for i in ("http://product.dangdang.com/22742927.html",
        "http://product.dangdang.com/20934047.html"): 
    resp = requests.get(i) 
    p.add(2, i, resp.text.encode("utf-8"))

p.flush()

p.close_idx()

p1 = filepack.FileUnpack(db)

p1.open_idx() 

x = p1.get("http://product.dangdang.com/20934047.html") 

x1 = p1.get("http://product.dangdang.com/22742927.html")

p1.close_idx()





