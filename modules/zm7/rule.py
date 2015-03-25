#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.zm7.cn': "//div[@class='nav_list']/div/ul/li/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "zm7.cats_parser", 
            },
            "dst": {
                "name": "zm7_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@id='pager']",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "zm7_pager",
                "batch": 30,
                "filter": "zm7.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "zm7_list", 
                },
            "get": {
                "method": "get",
                "parser": "zm7.pager",
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
                "name": "zm7_list",
                "batch": 30,
                "filter": "zm7.list_filter",
                },
            "rule": "//div[@class='goods_table_list']/ul/li/div",
            "dst": {
                "type": "list",
                "name": "zm7_stock",
                },
            "get": {
                "method": "get",
                "parser": "zm7.list_parser",
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
            "wait": 4,
            "src": {
                "name": "zm7_stock",
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "zm7.stock_filter"
                },
            "get": {
                "async": True,
                "method": "get",
                "parser": "zm7.stock_parser",
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