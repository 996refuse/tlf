#-*-encoding=utf-8-*-
rule = (
        {
            "name": "pager",
            "type": "fetch",
            "repeat": 1000,
            "from": {
                'http://s.vancl.com/search': "//div[@id='pager']/em",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "vancl.pager_parser", 
                },
            "dst": {
                "name": "vancl_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "vancl_list",
                "batch": 30,
                "filter": "vancl.list_filter"
            },
            "rule": "//div[@id='vanclproducts']/ul/li",
            "dst": {
                "type": "list",
                "name": "vancl_stock",
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "vancl.list_parser",
                "args": {
                    "limit": 10,
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "name": "stock",
            "type": "fetch",
            "src": {
                "name": "vancl_stock",
                "type": "list",
                "batch": 10,
                "group": True,
                "filter": "vancl.stock_filter"
                },
            "rule": "//p[@class='NowHasGoods']",
            "get": {
                "method": "get",
                "parser": "vancl.stock_parser",
                "args": { 
                    "limit": 5,
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