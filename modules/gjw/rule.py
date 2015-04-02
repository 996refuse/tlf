#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.gjw.com/': "//div[@class='cateMenu']/ul/li/div[1]/strong/a/@href",
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
            }
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
            }
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
