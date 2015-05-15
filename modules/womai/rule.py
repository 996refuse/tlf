#-*-encoding=utf-8-*-
rule = (
        {
            "name": "pager",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.womai.com/ProductList.htm": "//div[@class='page_m']/span",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "womai.pager",
            },
            "dst": {
                "name": "womai_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "womai_list",
                "batch": 30,
                "filter": "womai.list_filter",
            },
            "rule": {
                "item": "//div[@class='product_list']/div[contains(@class, 'product_item')]/div[contains(@class, 'proitem_list')]",
                "gid": "div[@class='product_item_price']/@id"
            },
            "multidst": {
                "stock": {
                    "type": "list",
                    "name": "womai_stock",
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "womai_dps_log"
                },
            },
            "get": {
                "method": "get",
                "parser": "womai.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
        },
        {
            "type": "fetch",
            "name": "stock",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "womai_stock",
                "batch": 30,
                "filter": "womai.stock_filter",
            },
            "rule": {
                "item": "//div[@class='product_list']/div[contains(@class, 'product_item')]",
            },
            "dst": {
                "type": "list",
                "name": "spider_result",
            },
            "get": {
                "method": "get",
                "parser": "womai.stock_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://price.womai.com/PriceServer/open/productlist.do?prices=buyPrice&ids=554014,554013,553897,542301,542308,542300,539461,539141,538381,538423",
                "check": "module_test_stock",
            }
            ]
        },
)