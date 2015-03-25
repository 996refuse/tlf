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
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='bottompage']/a[last()]/@href",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "bookschina_page",
                "batch": 30,
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
                "name": "bookschina_list",
                "batch": 30,
                "filter": "bookschina.list_filter",
                },
            "rule": "//div[@class='inright']/div[@class='bookContent']",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "bookschina.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)