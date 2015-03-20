#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.360kxr.com/drugs.html': "//div[@class='left-nav-cont']/ul/li/h4/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "360kxr.cats_parser", 
                },
            "dst": {
                "name": "360kxr_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='pages-box']/div[@class='page-num']/span",
            "src": {
                "type": "list",
                "name": "360kxr_list",
                "batch": 30,
                "filter": "360kxr.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "360kxr_page", 
                },
            "get": {
                "method": "get",
                "parser": "360kxr.pager",
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
                "name": "360kxr_page",
                "batch": 30,
                "filter": "360kxr.list_filter",
                },
            "rule": "//div[@class='hunt-list-box']/ul[@class='ul-list0']/li/dl/div/dt/a/@href",
            "dst": {
                "type": "list",
                "name": "360kxr_price",
                },
            "get": {
                "method": "get",
                "parser": "360kxr.list_parser",
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
                "name": "360kxr_price",
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "360kxr.stock_task_filter"
                },
            "rule": {
                "kxrprice": "//div[@class='right-intro']/div/div/div/div/span",
            },
            "get": {
                "method": "get",
                "parser": "360kxr.stock_parser",
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