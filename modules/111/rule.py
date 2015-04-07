#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.111.com.cn': "//div[@id='allCategoryHeader']/ul/li[(position()<last())]/div/h4/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "111.cats_parser", 
                },
            "dst": {
                "name": "111_pager",
                "type": "list",
            },
            "test": [
            {
                "url": 'http://www.111.com.cn',
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "rule": "//div[@class='turnPageBottom']/a[@id='page_']/@pageno",
            "src": {
                "type": "list",
                "name": "111_pager",
                "batch": 30,
                "filter": "111.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "111_list", 
                },
            "get": {
                "method": "get",
                "parser": "111.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/list/962285-0-0-0-0-0-0-1.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/964286-0-0-0-0-0-0-1.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/955306-0-0-0-0-0-0-1.html",
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
                "name": "111_list",
                "batch": 30,
                "filter": "111.list_filter",
                },
            "rule": "//ul[@id='itemSearchList']/li/div[not(contains(@class, 'none'))]",
            "dst": {
                "type": "list",
                "name": "111_price",
                },
            "get": {
                "method": "get",
                "parser": "111.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/list/953710-0-0-0-0-0-0-934.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/953710-0-0-0-0-0-0-913.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/964106-0-0-0-0-0-0-55.html",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "111_price",
                "batch": 30,
                "filter": "111.price_filter",
                },
            "rule": "",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "111.price_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
        },
)