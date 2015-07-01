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
            "rule": "//div[contains(@class, 'ui-paging')]/span[@class='total']/text()",
            "src": {
                "type": "list",
                "name": "vip_list",
                "batch": 60, 
                "filter": "vip.task_filter" 
                },
            "dst": {
                "type": "list",
                "name": "vip_page", 
                },
            "get": { 
                "method": "get", 
                "parser": "vip.page_parser",
                "args": {
                        "limit": 20,  
                        "interval": 1,
                        "debug": False, 
                    } 
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
                "batch": 60, 
                },
            "multidst": {
                "spider": {
                    "type": "list",
                    "name": "spider_result", 
                    },
                "dp": {
                    "type": "list",
                    "name": "vip_dp"
                    },
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "vip_dps_log", 
                    }
                },
            "get": { 
                "method": "get",
                "parser": "vip.list_parser",
                "args": {
                        "limit": 20,  
                        "interval": 1,
                        "debug": False, 
                    } 
                },
            "test": [
            {
                "url": "http://category.vip.com/search-1-0-26.html?q=2|7849&wz=1",
                "check": "module_test"
            }
            ]
        },
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                    "name": "vip_dp",
                    "type": "list",
                    "qtype": "dp", 
                },
            "dst": {
                "name": "vip_dp",
                "type": "list",
                "qtype": "dp",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                    }
                },
            }
        )
