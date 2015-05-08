#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.111.com.cn': "//div[@id='allCategoryHeader']/ul/li[(position()<last())]/div/h4/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "111.cats_parser",
                },
            "dst": {
                "name": "111_pager",
                "type": "list",
            },
            "test": [
            {
                "url": 'http://www.111.com.cn',
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            #"rule": "//div[@class='turnPageBottom']/a[@id='page_']/@pageno",
            "rule": "//li[@class='pageNum']/text()",
            "src": {
                "type": "list",
                "name": "111_pager",
                "batch": 30,
                "filter": "111.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "111_list",
                },
            "get": {
                "method": "get",
                "parser": "111.pager",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/list/962285-0-0-0-0-0-0-1.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/964286-0-0-0-0-0-0-1.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/955306-0-0-0-0-0-0-1.html",
                "check": "111.test_list"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "111_list",
                "batch": 30,
                "filter": "111.list_filter",
                },
            "rule": {
                "nodes": "//ul[@id='itemSearchList']/li/div[contains(@class, 'itemSearchResultCon')]",
                "buyinfo": "div[@class='buyInfo']",
                "sellout": "button[contains(@class, 'sellout')]",
                "buycart": "button[@class='buy']",
                "comment": "div[@class='comment']/a",
            },
            "multidst": {
                "prices": {
                    "type": "list",
                    "name": "111_price",
                },
                "items": {
                    "type": "list",
                    "name": "111_item",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "111_dps_log"
                },
            },
            "get": {
                "method": "get",
                "parser": "111.list_parser",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/list/953710-0-0-0-0-0-0-59.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/953710-0-0-0-0-0-0-23.html",
                "check": "module_test"
            },
            {
                "url": "http://www.111.com.cn/list/964106-0-0-0-0-0-0-23.html",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "item",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "111_item",
                "batch": 10,
                "filter": "111.item_filter",
                },
            "rule": "//input[@id='seriesCartButton']",
            "dst": {
                "type": "list",
                "name": "111_price",
                },
            "get": {
                "not200": "trace",
                "method": "get",
                "parser": "111.item_parser",
                "args": {
                    "limit": 5,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/interfaces/item/itemPrice.action?itemids=50066756",
                "gid": "http://www.111.com.cn/product/50066756.html",
                "stock": 1,
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "111_price",
                "batch": 15,
                "filter": "111.price_filter",
                },
            "rule": "",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "not200": "trace",
                "method": "get",
                "parser": "111.price_parser",
                "args": {
                    "limit": 6,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.111.com.cn/interfaces/item/itemPrice.action?itemids=50066756",
                "gid": "http://www.111.com.cn/product/50066756.html",
                "stock": 1,
                "check": "module_test"
            }
            ]
        },
)
