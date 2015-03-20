#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.jiuxian.com/': "//ul[@id='nav']/li[position() > 1]/h3/@url",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "jiuxian.cats_parser", 
                },
            "dst": {
                "name": "jiuxian_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='clearfix']/div/a[@class='number'][last()]",
            "src": {
                "type": "list",
                "name": "jiuxian_pager",
                "batch": 30,
                "filter": "jiuxian.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "jiuxian_list", 
                },
            "get": {
                "method": "get",
                "parser": "jiuxian.pager",
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
                "name": "jiuxian_list",
                "batch": 30,
                "filter": "jiuxian.list_filter",
                },
            "rule": "//div[@class='proListSearch']/ul/li",
            "dst": {
                "type": "list",
                "name": "jiuxian_price",
                },
            "get": {
                "method": "get",
                "parser": "jiuxian.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "name": "price",
            "type": "fetch",
            "src": {
                "name": "jiuxian_price",
                "type": "list",
                "batch": 40,
                "group": True,
                "filter": "jiuxian.price_filter"
                },
            "get": {
                "method": "get",
                "parser": "jiuxian.price_parser",
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