#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.m6go.com/baobaoshipin': "//section/div/div/div[1]/div/h3/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "m6go.cats_parser", 
                },
            "dst": {
                "name": "m6go_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='page']/div/a[last()]/@href",
            "src": {
                "type": "list",
                "name": "m6go_list",
                "batch": 30,
                "filter": "m6go.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "m6go_page", 
                },
            "get": {
                "method": "get",
                "parser": "m6go.pager",
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
                "name": "m6go_page",
                "batch": 30,
                "filter": "m6go.list_filter",
                },
            "rule": "//ul/li[@goodsid]",
            "dst": {
                "type": "list",
                "name": "m6go_price",
                },
            "get": {
                "method": "get",
                "parser": "m6go.list_parser",
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
                "name": "m6go_price",
                "type": "list",
                "batch": 30,
                "group": True,
                "filter": "m6go.stock_task_filter"
                },
            "rule": {
                "stock": "//span[@id='stockCountSpan']",
            },
            "get": {
                "method": "get",
                "parser": "m6go.stock_parser",
                "args": { 
                    "limit": 10,
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