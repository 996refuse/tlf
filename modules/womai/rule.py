#-*-encoding=utf-8-*-

sites = {
        "source": "cats",
        "sites": [
            (32, "huabei"),
            (1032, "huadong"),
            (2032, "huanan"), 
            ]
        }

rule = ( 
        {
            "name": "pager",
            "type": "fetch",
            "repeat": 7200, 
            "from": { 
                "http://www.womai.com/ProductList.htm": "//div[@class='page_m']/span",
            },
            "from_filter": "womai.from_filter",
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "womai.pager",
            },
            "dst": {
                "name": "womai_list",
                "type": "list",
                "subsite": True,
            },
            "period": "8-20",
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
                "subsite": True,
            },
            "rule": {
                "item": "//div[@class='product_list']/div[contains(@class, 'product_item')]/div[contains(@class, 'proitem_list')]",
                "gid": "div[@class='product_item_price']/@id", 
            },
            "multidst": {
                "stock": {
                    "type": "list",
                    "name": "womai_stock",
                    "subsite": True,
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "womai_dps_log"
                },
                "dp": {
                    "type": "list",
                    "name": "womai_dp",
                    }
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
            "test": [{
                "url": "http://www.womai.com/ProductList.htm?zhId=605&&rypId=608&&isKeyCommendClick=1&&Cid=606&&brand=-1&&mid=100&page=4",
                "check": "womai.list_test", 
                }]
        },
        {
            "type": "fetch",
            "name": "stock",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "womai_stock",
                "batch": 300,
                "filter": "womai.stock_filter",
                "subsite": True,
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
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "womai_dp",
                "type": "list",
                "qtype": "dp",
                },
            "dst": {
                "name": "womai_dp",
                "type": "",
                "qtype": "dp",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 10,
                    "interval": 1,
                    "debug": False,
                }, 
                "allow_redirect": 3,
            }, 
        },

)
