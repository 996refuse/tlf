#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.360kxr.com/drugs.html': "//div[@class='left-nav-cont']/ul/li/h4/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "360kxr.cats_parser", 
            },
            "dst": {
                "name": "360kxr_page",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.360kxr.com/drugs.html",
                "check": "module_test",
            },
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "rule": "//div[@class='pages-box']/div[@class='page-num']/span",
            "src": {
                "type": "list",
                "name": "360kxr_page",
                "batch": 10,
                "filter": "360kxr.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "360kxr_list", 
                },
            "get": {
                "method": "get",
                "parser": "360kxr.pager",
                "args": {
                    "limit": 4,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.360kxr.com/category/394-0-2-1-15-1.html",
                "check": "module_test",
            },
            {
                "url": "http://www.360kxr.com/category/977-0-2-1-15-1.html",
                "check": "module_test",
            },
            {
                "url": "http://www.360kxr.com/category/992-0-2-1-15-1.html",
                "check": "module_test",
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "360kxr_list",
                "batch": 10,
                "filter": "360kxr.list_filter"
            },
            "rule": {
                "nodes": "//div[@id='search_table']//ul/li",
                "gid": "dl/div/dt/a/@href",
                "stock": "dl/div/dd/div/p[@class='cart']",
            },
            "dst": {
                "type": "list",
                "name": "360kxr_price",
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "360kxr.list_parser",
                "args": {
                    "limit": 4,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.360kxr.com/category/483-1-4-2-2-0,999999-all-9-all-all-all-2.html",
                "check": "module_test"
            },
            {
                "url": "http://www.360kxr.com/category/201-0-2-1-15-1.html",
                "check": "module_test"
            },
            {
                "url": "http://www.360kxr.com/category/328-1-4-2-2-0,999999-all-9-all-all-all-9.html",
                "check": "360kxr.test_list"
            },
            ]
        },
        {
            "name": "price",
            "type": "fetch",
            "wait": 4,
            "src": {
                "name": "360kxr_price",
                "type": "list",
                "batch": 10,
                "group": True,
                "filter": "360kxr.price_filter"
                },
            "rule": {
                "kxrprice": "//span[@id='pro_mall_price']",
            },
            "get": {
                "method": "get",
                "parser": "360kxr.price_parser",
                "args": { 
                    "limit": 4,
                    "interval": 2, 
                    "debug": False, 
                    "timeout": 10, 
                    }, 
                "not200": "log", 
                "randua": True
                },
            "dst": {
                "name": "spider_result",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.360kxr.com/product/8726.html",
                "stock": 1,
                "check": "module_test"
            }
            ]
        }
)