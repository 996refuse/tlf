#-*-encoding=utf-8-*-
rule = (
        {
            "name": "mcats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.360kxr.com': "//div[@class='nav-box']//ul/li[position()>1 and position()<last()-2]/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "360kxr.mcats_parser", 
            },
            "dst": {
                "name": "360kxr_scats",
                "type": "list",
            },
        },
        {
            "name": "scats",
            "type": "fetch",
            "wait": 4,
            "rule": {
                "subcats": "//div[contains(@class, 'left-nav-box')]//ul/li/h4/a/@href",
                "maincats": "//div[contains(@class,'left-nav-box')]//h4/a/@href",
            },
            "src": {
                "type": "list",
                "name": "360kxr_scats",
                "batch": 10,
                "filter": "360kxr.cats_filter"
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "360kxr.scats_parser", 
            },
            "dst": {
                "name": "360kxr_page",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.360kxr.com/instrument.html",
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
                "nodes1": "//dl/div[1][@style]",
                "nodes2": "//div[@id='search_table']//ul/li",
                "gid": "dd[@class='title']/a/@href",
                "priceimg": "dd[@class='price-box']/span[@class='price']/img/@src",
                "stock": "dd/div/p[@class='cart']",
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
                "batch": 40,
                "group": True,
                "filter": "360kxr.price_filter"
            },
            #"rule": {
            #    "kxrprice": "//span[@id='pro_mall_price']",
            #},
            "get": {
                "method": "get",
                "parser": "360kxr.price_parser",
                "args": { 
                    "limit": 20,
                    "interval": 2, 
                    "debug": False, 
                    "timeout": 10, 
                    }, 
                "not200": "log", 
                "randua": True
                },
            "multidst": {
                "result": {
                    "name": "spider_result",
                    "type": "list",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "360kxr_dps_log"
                },
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