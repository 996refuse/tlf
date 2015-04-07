#-*-encoding=utf-8-*-
rule = (
        {
            "name": "boot",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.gjw.com': "",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "gjw.boot_parser",
            },
            "dst": {
                "name": "gjw_cats",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.gjw.com",
                "check": "module_test"
            }
            ]
        },
        {
            "name": "cats",
            "type": "fetch",
            "wait": 4,
            "rule": "//div[@class='cateMenu']/ul/li/div[1]/strong/a/@href",
            "src": {
                "type": "list",
                "name": "gjw_cats",
                "batch": 30,
                "filter": "gjw.cats_filter"
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "gjw.cats_parser", 
                },
            "dst": {
                "name": "gjw_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='page_box']/span[last()]/a/@href",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "gjw_pager",
                "batch": 30,
                "filter": "gjw.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "gjw_list", 
                },
            "get": {
                "method": "get",
                "parser": "gjw.pager",
                "args": {
                    "limit": 5,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.gjw.com/baojianjiu/",
                "check": "module_test"
            },
            {
                "url": "http://www.gjw.com/putaojiu/",
                "check": "module_test"
            },
            {
                "url": "http://www.gjw.com/chaye/",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "gjw_list",
                "batch": 30,
                "filter": "gjw.list_filter",
                },
            "rule": "//div[@id='J_ItemList']/div/div",
            "dst": {
                "type": "list",
                "name": "gjw_stock",
                },
            "get": {
                "method": "get",
                "parser": "gjw.list_parser",
                "args": {
                    "limit": 5,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.gjw.com/putaojiu-search-page-1.htm",
                "check": "module_test"
            },
            {
                "url": "http://www.gjw.com/putaojiu-search-page-21.htm",
                "check": "module_test"
            },
            {
                "url": "http://www.gjw.com/yangjiu-search-page-9.htm",
                "check": "module_test"
            },
            ]
        },
        {
            "name": "stock",
            "type": "fetch",
            "wait": 4,
            "src": {
                "name": "gjw_stock",
                "type": "list",
                "batch": 40,
                "group": True,
                "filter": "gjw.stock_filter"
                },
            "get": {
                "method": "get",
                "parser": "gjw.stock_parser",
                "args": { 
                    "limit": 1,
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
                }
        }
)
