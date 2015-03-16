rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 1200,
            "from": {
                "http://www.miyabaobei.com": ["//div[contains(@class, 'ccon')]/a/@href"]},
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "miyabaobei.cats_parser", 
                },
            "dst": {
                "name": "miyabaobei_list",
                "type": "list",
                }
            },
        {
            "name": "pager", 
            "type": "fetch",
            "wait": 2, 
            "rule": ("//div[@class = 'bmtitle']/div/em/text()", 40),
            "src": {
                "type": "list",
                "name": "miyabaobei_list",
                "batch": 2,
                "filter": "miyabaobei.task_filter",
                },
            "dst": {
                "type": "list",
                "name": "miyabaobei_page",
                },
            "get": {
                "async": True,
                "method": "get",
                "args": {
                    "limit": 1,
                    "interval": 1, 
                    "debug": False,
                    "timeout": 10,
                    }, 
                "parser": "miyabaobei.pager",
                "not200": "log",
                "randua": True,
                }, 
            },
        {
            "name": "list",
            "type": "fetch",
            "rule": {
                "node":"//div[contains(@class, 'content')]/div[contains(@id, 'item_')]",
                "link": "a/@href",
                "price":  "div[contains(@id, 'item_')]/div/div/span[contains(@id, 'sale_price')]/text()"
                },
            "wait": 2, 
            "src": {
                "name": "miyabaobei_page",
                "type": "list",
                "batch": 2, 
                },
            "get": {
                "method": "get",
                "parser": "miyabaobei.list_parser",
                "args": { 
                    "limit": 1,
                    "interval": 2, 
                    "timeout": 10,
                    "debug": False, 
                    }, 
                "not200": "log",
                "randua": True,
                },
            "dst": {
                "name": "miyabaobei_ids",
                "type": "list"
                }
            }, 
        {
            "name": "stock",
            "type": "fetch",
            "url": "http://www.miyabaobei.com/instant/item/getOutletsItemsInfo?ids=",
            "wait": 2, 
            "src": {
                "name": "miyabaobei_ids", 
                "type": "list",
                "batch": 80,
                "group": True,
                "filter": "miyabaobei.stock_task_filter"
                }, 
            "get": {
                "method": "get",
                "parser": "miyabaobei.stock_parser",
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
