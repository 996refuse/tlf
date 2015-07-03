rule = (
        { 
            "name": "cats", 
            "type": "fetch",
            "repeat": 4000,
            "from": {
                "http://www.tootoo.cn/category.html": ['<a href="/category-(\d{5})?.html">[^<>]*</a>']
                }, 
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "tootoo.cats_parser",
                },
            "dst": {
                "name": "tootooCatsInt_list",
                "type": "list"
                }
        }, 
        { 
            "name": "pager",
            "type": "fetch",
            "wait": 2,
            "rule": "//div[contains(@class, 'tlist_pxnum')]/span/text()",
            "src": {
                "type": "list",
                "name": "tootooCatsInt_list",
                #"batch": 60, 
                "filter": "tootoo.task_filter" 
                },
            "dst": {
                "type": "list",
                "name": "tootoo_page", 
                },
            "get": { 
                "method": "get", 
                "parser": "tootoo.page_parser",
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
                "node": "//ul[contains(@id, 'list_goodslist')]/li",
                "link": "div[contains(@class, 'pro_box')]/div[contains(@class, 'pro_img')]/a/@href",
                "price": "div[contains(@class, 'pro_price')]/b/text()",
                "stock": "div[contains(@class, 'pro_span')]/div[contains(@is_has_goods, 'false')]/@style"
                },
            "src": {
                "type": "list",
                "name": "tootoo_page",
                "batch": 60,
                },
            "dst": {
                    "type": "list",
                    "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "tootoo.list_parser",
                "args": {
                        "limit": 20,
                        "interval": 1,
                        "debug": False,
                    }
                },
            "test": [
            {
                "url": "http://www.tootoo.cn/list-s1-13093-0-0-0-0-0-1-0-0-0-1,2,3,0-zh_cn.html",
                "check": "module_test"
            }
            ]
        }
    )