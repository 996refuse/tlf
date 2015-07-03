rule = (
        { 
            "name": "cats", 
            "type": "fetch",
            "repeat": 4000,
            "from": {
                "http://www.lingshi.com/ditu.htm": ["//div[contains(@class,'brandye')]/div/div/a/@href"]
                }, 
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "lingshi.cats_parser",
                },
            "dst": {
                "name": "lingshiCats_list",
                "type": "list"
                }
        }, 
        { 
            "name": "pager",
            "type": "fetch",
            "wait": 2,
            "rule": "//li[contains(@class, 'page')]/span/text()",
            "src": {
                "type": "list",
                "name": "lingshiCats_list",
                "batch": 60, 
                "filter": "lingshi.task_filter" 
                },
            "dst": {
                "type": "list",
                "name": "lingshi_page", 
                },
            "get": { 
                "method": "get", 
                "parser": "lingshi.page_parser",
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
                "node": "//div[contains(@class, 'snack_wrap fixed')]/ul/li",
                "link": "a/@href",
                "price": "p[contains(@class, 'price')]/text()",
                #"stock": "div[contains(@class, 'pro_span')]/div[contains(@is_has_goods, 'false')]/@style"
                },
            "src": {
                "type": "list",
                "name": "lingshi_page",
                "batch": 60,
                },
            "dst": {
                    "type": "list",
                    "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "lingshi.list_parser",
                "args": {
                        "limit": 20,
                        "interval": 1,
                        "debug": False,
                    }
                },
            "test": [
            {
                "url": "http://www.lingshi.com/list/b42_y1.htm",
                "check": "module_test"
            }
            ]
        }
       )