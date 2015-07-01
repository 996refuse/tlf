
sites = { 
    "source": "cats",
    "order": True,
    "sites": [
        (25, "nanjing"),
        (1025, "beijing"), 
        (2025, "guangzhou"),
        (3025, "chengdu"),
        ], 
    } 


rule = (
        {
            "name": "cats", 
            "type": "fetch", 
            "repeat": 7200, 
            "boot": "suning.set_id",
            "from": {
                "http://www.suning.com/emall/pgv_10052_10051_1_.html": "//span/a[contains(@href, 'list.suning.com')]", 
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "suning.cats_parser" 
                },
            "dst": {
                "type": "list",
                "name": "suning_cats", 
                "subsite": True,
                },
            "test": ( 
                {
                    "url": "http://www.suning.com/emall/pgv_10052_10051_1_.html",
                    "check": "suning.test_cats_parser" 
                    },
                ), 
        }, 
        {
            "name": "pager",
            "type": "fetch", 
            "wait": 2,
            "src": {
                "type": "list",
                "name": "suning_cats",
                "filter": "suning.pager_filter",
                "batch": 30,
                "subsite": True,
                },
            "dst": {
                "type": "list", 
                "name": "suning_page",
                "subsite": True
                }, 
            "rule": {
                "normal": "//a[@id = 'pageLast']//text()",
                "book_a": "//span[@class = 'pageCount']/text()",
                "book_b": "//i[@id = 'pageTotal']/text()"
                },
            "get": {
                "method": "get", 
                "parser": "suning.pager",
                "not200": "retry",
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False 
                    },
                },
            "test": [
                {
                    "url": "http://list.suning.com/1-264317-0-0-0-9173.html",
                    "check": "suning.pager_test"
                }
                ] 
        },
        { 
            "name": "list", 
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "suning_page",
                "type": "list",
                "batch": 30,
                "filter": "suning.list_filter",
                "subsite": True
                },
            "multidst": {
                "price": {
                    "name": "suning_price",
                    "type": "list",
                    "subsite": True,
                },
                "book_price": {
                    "name": "suning_book_price",
                    "type": "list",
                    "subsite": True,
                },
                "spider": {
                    "name": "spider_result",
                    "type": "list"
                }, 
                "dp": { 
                    "name": "suning_dp",
                    "type": "list", 
                    "node": "dp_pairs",
                    "log": True
                    },
                "dps_log": {
                    "node": "dps_log",
                    "name": "suning_dps_log",
                    "type": "hash",
                    "subsite": True,
                    },
                "comment": {
                    "name": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "comment",
                    "pack": False
                    }
                },
            "rule": {
                "book_node": "//ul[@id = 'proList']/li", 
                "book_title": "div[@class = 'thirdInfo']/h3/a",
                "book_stock": "div[@class = 'thirdInfo']/span[@class = 'youhuo']/text()", 
                "normal_node": "//div[@id = 'proShow']/ul/li",
                "normal_title": "div[@class = 'inforBg']/h3/a/p/text()",
                "normal_stock": "div/div[contains(@class, 'comment')]/i/text()",
                "normal_price": "div/div[contains(@class, 'infor-top')]/p/img/@src2",
                "qid": "div[contains(@class , 'btn')]/div/img",
                "normal_comment": "div/div[contains(@class, 'comment')]/p/a/i/text()",
                "book_comment": "div[@class = 'thirdInfo']/form/p/span[@class='text-line']/em/a/text()",
                },
            "get": {
                "method": "get",
                "parser": "suning.list_parser",
                "not200": "retry", 
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False, 
                    } 
                },
            "test": ( 
                {
                    "url": "http://list.suning.com/0-258006-0-0-0-9173.html",
                    "check": "suning.list_test" ,
                    "ignore": True,
                },
                {
                    "url": "http://list.suning.com/0-431505-25-0-0-9017.html",
                    "check": "suning.list_test", 
                }
                )
        }, 
        { 
            "name": "price",
            "type": "fetch",
            "wait": 2,
            "src": { 
                "name": "suning_price",
                "type": "list",
                "filter": "suning.price_filter",
                "batch": 100,
                "subsite": True,
                },
            "dst": {
                "name": "spider_result",
                "subsite": False,
                "type": "list", 
                },
            "get": {
                "method": "get",
                "parser": "suning.price_parser",
                "not200": "log", 
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False, 
                }, 
                "keys": ("qid", "stock", "stock")
            },
        },
        { 
            "name": "book_price",
            "type": "fetch",
            "wait": 2,
            "src": { 
                "group": True,
                "name": "suning_book_price",
                "type": "list",
                "filter": "suning.bookprice_filter",
                "batch": 100,
                "subsite": True,
                },
            "dst": {
                "name": "spider_result",
                "subsite": False,
                "type": "list", 
                },
            "get": {
                "method": "get",
                "parser": "suning.book_price",
                "not200": "log", 
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False, 
                }, 
                "keys": ("qid", "stock")
            },
            "test": [
            {
                "url": "http://www.suning.com/emall/priceService_9173_107961923%7C%7C%7C_1.html",
                "qid": "107961923",
                "stock": 1,
                "check": "module_test",
            }
            ]
        },
        {
            "name": "dp",
            "type": "fetch", 
            "wait": 2,
            "src": { 
                "name": "suning_dp",
                "type": "list", 
                "qtype": "dp",
                },
            "dst": { 
                "name": "suning_dp",
                "type": "", 
                "qtype": "dp",
                }, 
            "get": {
                "method": "get", 
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False, 
                }, 
                "redirect": 10,
                "keys": ("qid", "stock"),
            },
        },
        {
            "type": "diff_dps",
            "name": "diff_dps",
            "wait": 20000,
            "src": {
                "type": "hash",
                "node": "dps_log",
                "name": "dps_log",
                "subsite": True,
                },
            "wait": 50000,
            "dst": {
                "type": "list",
                "name": "suning_diff_dps",
                "node": "diff_dps",
                "subsite": True,
                "log": False,
                }
        },
        {
            "name": "offshelf",
            "type": "fetch",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "suning_diff_dps",
                "batch": 600, 
                "node": "diff_dps",
                "subsite": True,
                "filter": "suning.off_filter",
                },
            "dst": {
                "name": "spider_result",
                "type": "list",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                }, 
                "parser": "suning.off_parser",
            },
            "test": [
                {
                    "url": "http://price2.suning.cn/webapp/wcs/stores/prdprice/249321_9173_10000_9-1.png",
                    "check": "suning.off_check",
                    "qid": 249321,
                }
                ]
        } 
        )
