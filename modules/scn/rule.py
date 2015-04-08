#-*-encoding=utf-8-*-
rule = (
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='clearfix']/table/tr/td[@class='pagernum']/a[last()]",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.s.cn/list": ""
            },
            "src": {
                "type": "list",
                "name": "scn_pager",
                "batch": 30,
                "filter": "scn.pager_filter"
            },
            "dst": {
                "type": "list",
                "name": "scn_list", 
                },
            "get": {
                "method": "get",
                "parser": "scn.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.s.cn/list",
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
                "name": "scn_list",
                "batch": 30,
                "filter": "scn.list_filter",
                },
            "rule": {
                "node": "//div[@class='product_list']/dl",
                },
            "dst": {
                "type": "list",
                "name": "scn_stock", 
                },
            "get": {
                "method": "get",
                "parser": "scn.list_parser",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.s.cn/list/pg66",
                "check": "module_test"
            },
            {
                "url": "http://www.s.cn/list/pg23",
                "check": "module_test"
            },
            {
                "url": "http://www.s.cn/list/pg79",
                "check": "module_test"
            },
            ]
        },
        {
            "name": "stock",
            "type": "fetch",
            "wait": 4,
            "src": {
                "name": "scn_stock",
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "scn.stock_task_filter"
                },
            "rule": "//div[@class='buyinfo_bot']//span[@class='store']",
            "get": {
                "method": "get",
                "parser": "scn.stock_parser",
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