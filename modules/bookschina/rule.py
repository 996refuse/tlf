#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.bookschina.com/books/kind/sort.asp': "//section/div/div/div[1]/div/h3/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "bookschina.cats_parser", 
                },
            "dst": {
                "name": "bookschina_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='page']/div/a[last()]/@href",
            "src": {
                "type": "list",
                "name": "bookschina_list",
                "batch": 30,
                "filter": "bookschina.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "bookschina_page", 
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
            "src": {
                "type": "list",
                "name": "bookschina_page",
                "batch": 30,
                "filter": "bookschina.list_filter",
                },
            "rule": "//ul/li[@goodsid]",
            "dst": {
                "type": "list",
                "name": "bookschina_price",
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
        {
            "name": "stock",
            "type": "fetch",
            "src": {
                "name": "bookschina_price",
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "bookschina.stock_task_filter"
                },
            "rule": {
                "stock": "//span[@id='stockCountSpan']",
            },
            "get": {
                "method": "get",
                "parser": "bookschina.stock_parser",
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