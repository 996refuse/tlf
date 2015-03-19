#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.zm7.cn': "//div[@class='nav_list']/div/ul/li/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "zm7.cats_parser", 
            },
            "dst": {
                "name": "zm7_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@id='pager']",
            "src": {
                "type": "list",
                "name": "zm7_list",
                "batch": 30,
                "filter": "zm7.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "zm7_page", 
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
            "src": {
                "type": "list",
                "name": "zm7_page",
                "batch": 30,
                "filter": "zm7.list_filter",
                },
            "rule": "//div[@class='goods_table_list']/ul/li/div",
            "dst": {
                "type": "list",
                "name": "zm7_price",
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
            "src": {
                "name": "zm7_price",
                "type": "list",
                "batch": 16,
                "group": True,
                },
            "get": {
                "async": True,
                "method": "post",
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