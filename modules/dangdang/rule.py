#-*-encoding=utf-8-*-

import simple_http

test_offcheck_hdr = simple_http.json_header.copy()
test_offcheck_hdr["Referer"] = "http://category.dangdang.com" 

rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://category.dangdang.com/": "//div[contains(@class, 'con')]/div[contains(@class,'col')]//div[@class='cfied-list']/div[@class='list']/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "dangdang.cats_parser",
            },
            "dst": {
                "name": "dangdang_pager",
                "type": "list",
            },
            "price_range": "price_range",
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "rule": {
                "norm": "//ul[@class='paging']/li[@class='page_input']/span[1]",
                "ebook": "//div[@class='page']/input[@name='totalPage']/@value",
            },
            "src": {
                "type": "list",
                "name": "dangdang_pager",
                "batch": 500,
                "filter": "dangdang.pager_filter"
            },
            "dst": {
                "type": "list",
                "name": "dangdang_list",
            },
            "get": {
                "method": "get",
                "parser": "dangdang.pager",
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://category.dangdang.com/cid\xe8\xb7\x91\xe6\xad\xa5\xe6\x9c\xba .html",
                "check": "module_test",
            },
            {
                "url": "http://category.dangdang.com/cid4005296-pg1.html",
                "check": "module_test"
            },
            {
                "url": "http://category.dangdang.com/cp10.24.00.00.00.00.html",
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "dangdang_list",
                "batch": 500,
                "filter": "dangdang.list_filter",
            },
            "rule": {
                "norm1": "//div[@id='content']/div/div/div",
                "norm2": "//div[contains(@class, 'shoplist')]/ul/li/div",
                "ebook": "//div[@id='category_ebookLst']//div[@class='ebookLst_s']",    # ebooks
                "book": "//div[@name='Product']/div/ul/li/div",
                "comment": "p[@class='star']/a/text()",
                "gid": {
                    "ebook": "div[@class='ebookCon']/div/h2/a/@href",
                    "norm": "a/@href",
                },
                "price": {
                    "ebook": "div[@class='ebookCon']/div/div/span[@class='price']/span[1]/em",
                    "book": "p/span[@class='price_n']",
                    "norm": "p[@class='price']/span[@class='price_n']",
                },
                "stock": {
                    "book": "p[contains(@class, 'buy_button')]/a[1]/@href",
                },
                "store_normal": "p[@class = 'link']/a", 
            },
            "multidst": {
                "stock": {
                    "type": "list",
                    "name": "dangdang_stock",
                },
                "result": {
                    "type": "list",
                    "name": "spider_result",
                },
                "dp": {
                    "type": "list",
                    "name": "dangdang_dp",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "dangdang_dps_log"
                },
                "comment": {
                    "name": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "comment",
                    "pack": False
                    },
                "shop": {
                    "name": "shop",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "shop",
                    "pack": False
                    }

            },
            "get": {
                "method": "get",
                "parser": "dangdang.list_parser",
                "args": {
                    "limit": 50,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://category.dangdang.com/cp01.63.18.00.00.00-lp20-hp23-pg2.html",
                "check": "module_test",
            },
            {
                "url": "http://category.dangdang.com/cp01.58.11.00.00.00-pg47.html",
                "check": "module_test"
            },
            {
                "url": "http://category.dangdang.com/cid4001022-pg21.html",
                "check": "module_test_stock"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "stock",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "dangdang_stock",
                "batch": 500,
                "filter": "dangdang.stock_filter",
                },
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "dangdang.stock_parser",
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False
                }
            },
        },
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "dangdang_dp",
                "type": "list",
                "qtype": "dp",
                },
            "dst": {
                "name": "dangdang_dp",
                "type": "",
                "qtype": "dp",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                },
            },
        }, 
        {
            "type": "diff_dps", 
            "name": "diff_dps", 
            "src": { 
                "type": "hash",
                "node": "dps_log",
                "name": "dps_log",
                },
            "wait": 86400, 
            "dst": {
                "type": "list",
                "name": "dangdang_diff_dps",
                "node": "diff_dps",
                "log": False
                }
        }, 
        {
            "name": "offcheck",
            "type": "fetch", 
            "wait": 2,
            "src": { 
                "type": "list",
                "name": "dangdang_diff_dps",
                "batch": 3000, 
                "group": True,
                "node": "diff_dps",
                "filter": "dangdang.off_filter",
                },
            "dst": { 
                "name": "spider_result",
                "type": "list", 
                },
            "get": {
                "method": "post", 
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False, 
                }, 
                "parser": "dangdang.checkoffline",
            }, 
            "test": [
                {
                    "payload": {
                        "pids": "1098685806, 1111111", 
                        "time": "1433917547",
                        "type": "get_price",
                        },
                    "header": test_offcheck_hdr,
                    "url": "http://category.dangdang.com/Standard/Search/Extend/hosts/api/get_price.php",
                    "method": "post", 
                    "check": "dangdang.offcheck_test"
                    }
                ]
        },
)
