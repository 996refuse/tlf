#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",

            "from": {
                "http://www.s.cn/list": ""
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "scn.cats_parser", 
                },
            "dst": {
                "name": "scn_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='clearfix']/table/tr/td[@class='pagernum']/a[last()]",
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
            }
        },
        {
            "type": "fetch",
            "name": "list", 
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
            }
        },
        {
            "name": "stock",
            "type": "fetch",
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