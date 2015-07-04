rule = (
        { 
            "name": "cats", 
            "type": "fetch",
            "repeat": 2400,
            "from": {
                "http://www.likeface.com/": ["//dd[contains(@class,'pngFix')]/a/@href"]
                }, 
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "likeface.cats_parser",
                },
            "dst": {
                "name": "likeface_list",
                "type": "list"
                }
        }, 
        { 
            "name": "pager",
            "type": "fetch",
            "wait": 2,
            "rule": [
                "//div[contains(@class, 'tPageTop')]/em/text()",
                "//div[contains(@class, 'tPageTop')]/a/@href"],
            "src": {
                "type": "list",
                "name": "likeface_list",
                "batch": 60, 
                "filter": "likeface.task_filter" 
                },
            "dst": {
                "type": "list",
                "name": "likeface_page", 
                },
            "get": { 
                "method": "get", 
                "parser": "likeface.page_parser",
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
                "node": "//ul[contains(@class, 'gPdtList')]/li",
                "link": "p[contains(@class, 'tIntro')]/a/@href",
                "price": "p[contains(@class, 'tPrc')]/strong/text()",
                "stock": "div[contains(@class, 'pro_span')]/div[contains(@is_has_goods, 'false')]/@style"
                },
            "src": {
                "type": "list",
                "name": "likeface_page",
                "batch": 60,
                },
            "dst": {
                    "type": "list",
                    "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "likeface.list_parser",
                "args": {
                        "limit": 20,
                        "interval": 1,
                        "debug": False,
                    }
                },
            "test": [{
                "url": "http://www.likeface.com/productlist.shtml?typeid=28&brandid=0&pricefrom=0&priceto=0&sort=&subtype=129&page=1",
                "check": "module_test"
            },{
                "url": "http://www.likeface.com/bst/chunmi",
                "check": "module_test"
            }]
        }
        )
