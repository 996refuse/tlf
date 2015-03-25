#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.m6go.com/baobaoshipin': "//section/div/div/div[1]/div/h3/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "m6go.cats_parser", 
                },
            "dst": {
                "name": "m6go_page",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='page']/div/a[last()]/@href",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "m6go_page",
                "batch": 30,
                "filter": "m6go.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "m6go_list", 
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
            "wait": 4,
            "src": {
                "type": "list",
                "name": "m6go_list",
                "batch": 30,
                "filter": "m6go.list_filter",
                },
            "rule": "//ul/li[@goodsid]",
            "dst": {
                "type": "list",
                "name": "spider_result",
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
)