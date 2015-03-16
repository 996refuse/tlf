rule = (
        { 
            "name": "cats", 
            "type": "fetch",
            "repeat": 2400,
            "from": {
                "http://category.vip.com/": ["(q=[0-9]+\|[0-9]+&wz=[0-9]+)","(q=[0-9]+\|[0-9]+&ff=[0-9]+)"]
                }, 
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "vip.cats_parser",
                },
            "dst": {
                "name": "vip_list",
                "type": "list"
                }
        }, 
        { 
            "name": "pager",
            "type": "fetch",
            "wait": 2,
            "rule": "//span[@class = 'cat-paging-txt']/text()",
            "src": {
                "type": "list",
                "name": "vip_list",
                "batch": 1, 
                "filter": "vip.task_filter" 
                },
            "dst": {
                "type": "list",
                "name": "vip_page", 
                },
            "get": {
                "async": True,
                "method": "get", 
                "parser": "vip.page_parser"
                }
            },
        {
            "name": "list",
            "type": "fetch",
            "wait": 2,
            "rule": {
                "node": "//figure[contains(@id, 'J_pro_')]",
                "link": "div[@class = 'cat-item-pic']/a/@href",
                "price": "figcaption[@class = 'cat-item-inf']/p/span[@class = 'cat-pire-nub']/text()"
                },
            "src": {
                "type": "list",
                "name": "vip_page",
                "batch": 1, 
                },
            "dst": {
                "type": "list",
                "name": "spider_result", 
                },
            "get": { 
                "method": "get",
                "parser": "vip.list_parser",
                "args": {
                        "limit": 20,  
                        "interval": 1,
                        "debug": False, 
                    } 
                }
            }
        )
