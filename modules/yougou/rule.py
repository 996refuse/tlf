#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.yougou.com/allproducts.shtml": "//div[contains(@class, 'ygwrap') and @id]/div/div/div[@class='key']/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "yougou.cats",
            },
            "dst": {
                "name": "yougou_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yougou_pager",
                "batch": 10,
                "filter": "yougou.pager_filter",
            },
            "rule": "//span[@class='tpagesec']",
            "dst": {
                "type": "list",
                "name": "yougou_list",
            },
            "get": {
                "method": "get",
                "parser": "yougou.pager",
                "args": {
                    "limit": 5,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.yougou.com/f-0-6LJ_XWP-0-0.html",
                "check": "module_test",
            }
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yougou_list",
                "batch": 10,
                "filter": "yougou.list_filter",
            },
            "rule": {
                "nodes": "//ul[@id='proList']/li/div",
                "gid": "div/a/sup/@no",
                "gurl": "div/a/@href",
                "price": "div/p[@class='price_sc']/em/i/text()",
            },
            "dst": {
                "type": "list",
                "name": "yougou_stock",
            },
            "get": {
                "method": "get",
                "parser": "yougou.list_parser",
                "args": {
                    "limit": 5,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.yougou.com/f-0-Y0A_L9C-0-0-232.html",
                "check": "module_test",
            },
            {
                "url": "http://www.yougou.com/f-0-Y0A_L9C-0-0-242.html",
                "check": "module_test",
            },
            {
                "url": "http://www.yougou.com/f-0-Y0A_OX8-0-0-133.html",
                "check": "module_test",
            },
            ]
        },
        {
            "type": "fetch",
            "name": "stock",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "yougou_stock",
                "batch": 10,
                "filter": "yougou.stock_filter",
            },
            "dst": {
                "type": "list",
                "name": "spider_result",
            },
            "get": {
                "method": "get",
                "parser": "yougou.stock_parser",
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.yougou.com/commodity/getGoodsDetail.sc?cNo=99870871&rrdom=0.288716439336",
                "gurl": "233",
                "price": "233",
                "check": "module_test_stock"
            }
            ]
        },
)