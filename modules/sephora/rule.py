#-*-encoding=utf-8-*- 

rule = ( 
        {
            "name": "cats", 
            "type": "fetch",
            "repeat": 1800,
            "from": {
                "http://www.sephora.cn/": ["//dl/dd/strong/a/@href"]
                }, 
            "get": {
                "type": "simple", 
                "method": "get", 
                "parser": "sephora.cats_parser",
                },
            "dst": {
                "name": "sephora_list", 
                "type": "list",
                }
            }, 
        {
            "name": "pager", 
            "type": "fetch",
            "wait": 2,
            "rule": {
                "count": "//b[@id = 'categorySum']/text()", 
                "url": "http://www.sephora.cn/webapp/wcs/stores/servlet/ajaxSearchResultsListView_sub", 
                },
            "src": {
                "type": "list",
                "name": "sephora_list",
                "batch": 1,
                "filter": "sephora.task_filter",
                },
            "dst": {
                "type": "list",
                "name": "sephora_page" 
                },
            "get": {
                "async": True,
                "method": "get", 
                "args": {
                    "limit": 1,
                    "interval": 1, 
                    "debug": False,
                    }, 
                "parser": "sephora.pager" 
                }
            },
        {
            "name": "list", 
            "type": "fetch",
            "wait": 2,
            "rule": {
                "node": "//body/li", 
                "link": "div/div[@class = 'proTit']/a/@href",
                "price": "div/div[@class = 'proPrice']/text()",
                },
            "src": {
                "name": "sephora_page",
                "type": "list",
                "batch": 1, 
                }, 
            "get": {
                "method": "post",
                "parser": "sephora.list_parser",
                "args": { 
                    "limit": 1,
                    "interval": 1, 
                    "debug": False,
                    }, 
                },
            "dst": {
                "name": "spider_result",
                "type": "list",
                }
            }, 
        )
