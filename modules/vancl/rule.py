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
            },
            "test": [
            {
                "url": "http://s.vancl.com/search",
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
                "name": "vancl_list",
                "batch": 30,
                "filter": "vancl.list_filter"
            },
            "rule": {
                "nodes": "//div[@id='vanclproducts']/ul/li",
                "gid": "p/a/@href",
                "price1": "div/span[@class='Sprice']",
                "price2": "div/div[1]",
            },
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
            },
            "test": [
            {
                "url": "http://s.vancl.com/p6.html",
                "check": "module_test"
            },
            {
                "url": "http://s.vancl.com/p9.html",
                "check": "module_test"
            },
            {
                "url": "http://s.vancl.com/p3.html",
                "check": "module_test"
            }
            ]
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
            "rule": "//div[@id='goods-viewer']",
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
            "multidst": {
                "result": {
                    "name": "spider_result",
                    "type": "list",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "vancl_dps_log"
                },
            },
            "test": [
            {
                "url": "http://www.s.cn/puma-82561904.html",
                "price": "233",
                "check": "module_test_stock"
            }
            ]
        }
)