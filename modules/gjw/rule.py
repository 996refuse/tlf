#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
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