#-*-encoding=utf-8-*-
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
                "book": "//div[@class='page']/input[@name='totalPage']/@value"
            },
            "src": {
                "type": "list",
                "name": "dangdang_pager",
                "batch": 50,
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
                "batch": 30,
                "filter": "dangdang.list_filter",
            },
            "rule": {
                "norm1": "//div[@id='content']/div/div/div",
                "norm2": "//div[contains(@class, 'shoplist')]/ul/li/div",
                "ebook": "//div[@id='category_ebookLst']//div[@class='ebookLst_s']",    # ebooks
                "book": "//div[@name='Product']/div/ul/li",
                "gid": {
                    "ebook": "div[@class='ebookCon']/div/h2/a/@href",
                    "norm": "a/@href",
                },
                "price": {
                    "ebook": "div[@class='ebookCon']/div/div/span[@class='price']/span[1]/em",
                    "book": "div/p/span[@class='price_n']",
                    "norm": "p[@class='price']/span[@class='price_n']",
                },
                "stock": {
                    "book": "div/p[contains(@class, 'buy_button')]/a[1]/@href",
                }
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
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "dangdang_dps_log"
                }
            },
            "get": {
                "method": "get",
                "parser": "dangdang.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://e.dangdang.com/list_98.01.62.00_3_saleWeek_1.htm",
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
                "batch": 30,
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
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
        },
)