#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.bookschina.com/books/kind/sort.asp': "//div[@class='categories']/h3/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "bookschina.cats_parser", 
                },
            "dst": {
                "name": "bookschina_page",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.bookschina.com/books/kind/sort.asp",
                "check": "bookschina.test_cats"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='bottompage']/a[last()]/@href",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "bookschina_page",
                "batch": 10,
                "filter": "bookschina.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "bookschina_list", 
                },
            "get": {
                "method": "get",
                "parser": "bookschina.pager",
                "args": {
                    "limit": 2,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.bookschina.com/kinder/49000000/",
                "check": "module_test"
            },
            {
                "url": "http://www.bookschina.com/kinder/35000000/",
                "check": "module_test"
            },
            {
                "url": "http://www.bookschina.com/kinder/17000000/",
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
                "name": "bookschina_list",
                "batch": 10,
                "filter": "bookschina.list_filter",
                },
            "rule": {
                "nodes": "//div[@class='inright']/div[@class='bookContent']",
                "gid": "div[@class='wordContent']/a[@class='titlein']/@href",
                "price": "div[@class='wordContent']/span",
            },
            "multidst": {
                "result": {
                    "type": "list",
                    "name": "spider_result",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "bookschina_dps_log"
                },
            },
            "get": {
                "method": "get",
                "parser": "bookschina.list_parser",
                "args": {
                    "limit": 2,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.bookschina.com/kinder/63000000_5_1_92/",
                "check": "module_test",
            },
            {
                "url": "http://www.bookschina.com/kinder/63000000_5_1_523/",
                "check": "module_test",
            },
            {
                "url": "http://www.bookschina.com/kinder/63000000_5_1_317/",
                "check": "module_test",
            },
            ]
        },
)