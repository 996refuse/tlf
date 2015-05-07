#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://search.bookuu.com/': "//div[@class='allcats']/div[contains(@class, 'cats-item')]/div/ul/li/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "bookuu.cats_parser", 
                },
            "dst": {
                "name": "bookuu_pager",
                "type": "list",
            },
            "test": [
            {
                "url": "http://search.bookuu.com/",
                "check": "bookuu.test_cats"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "bookuu_pager",
                "batch": 30,
                "filter": "bookuu.pager_filter",
            },
            "rule": "//div[@id='page']/ul/li[3]/text()",
            "dst": {
                "type": "list",
                "name": "bookuu_list",
            },
            "get": {
                "method": "get",
                "parser": "bookuu.pager",
                "args": {
                    "limit":15,  
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
                "name": "bookuu_list",
                "batch": 30,
                "filter": "bookuu.list_filter",
                },
            "rule": "//div[@class='main-wrap']/div[contains(@class, 'books-list')]",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "bookuu.list_parser",
                "args": {
                    "limit":15,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)