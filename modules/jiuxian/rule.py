#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
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
            },
            "test": [
            {
                "url": "http://www.jiuxian.com/",
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='clearfix']/div/a[@class='number'][last()]",
            "wait": 4,
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
            },
            "test": [
            {
                "url": "http://list.jiuxian.com/95-0-0-0-0-0-0-0-0-0-0-0.htm#v2",
                "check": "module_test"
            },
            {
                "url": "http://list.jiuxian.com/68-0-0-0-0-0-0-0-0-0-0-0.htm#v2",
                "check": "module_test"
            },
            {
                "url": "http://list.jiuxian.com/179-0-0-0-0-0-0-0-0-0-0-0.htm",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "jiuxian_list",
                "batch": 30,
                "filter": "jiuxian.list_filter",
                },
            "rule": {
                "nodes": "//div[@class='proListSearch']/ul/li",
                "gid": "div/a[@class='proName']/@href",
                "ostock": "div/a[contains(@class, 'lack')]",
            },
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
            },
            "test": [
            {
                "url": "http://list.jiuxian.com/2-0-0-0-0-0-0-0-0-0-0-0.htm?pageNum=23&",
                "check": "jiuxian.test_list"
            },
            {
                "url": "http://list.jiuxian.com/2-0-0-0-0-0-0-0-0-0-0-0.htm?pageNum=11&",
                "check": "module_test"
            },
            {
                "url": "http://list.jiuxian.com/1-0-0-0-0-0-0-0-0-0-0-0.htm?pageNum=100&",
                "check": "module_test"
            },
            ]
        },
        {
            "name": "price",
            "type": "fetch",
            "wait": 4,
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