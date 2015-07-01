rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 10000,
            "from": {
                "http://book.jd.com/booksort.html": "//div[@class = 'mc']/dl/dd/em/a",
                "http://mvd.jd.com/mvdsort/4051.html": "//div[@class = 'mc']/dl/dd/em/a",
                "http://mvd.jd.com/mvdsort/4052.html": "//div[@class = 'mc']/dl/dd/em/a",
                "http://mvd.jd.com/mvdsort/4053.html": "//div[@class = 'mc']/dl/dd/em/a",
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "jd_book.cats_parser",
                },
            "dst": {
                "name": "jd_book_list",
                "type": "list",
                },
            "price_range": "price_range",
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": {
                "book": "//div[@class =  'f-pager']/span/i/text()"
                },
            "src": {
                "type": "list",
                "name": "jd_book_list",
                "batch": 30,
                "filter": "jd_book.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "jd_book_page",
                },
            "get": {
                "method": "get",
                "parser": "jd_book.pager",
                "not200": "log",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_book_page",
                "batch": 2000,
                "filter": "jd_book.list_filter",
                },
            "rule": {
                "book": "//ul/li[@class = 'gl-item']/div",
                "title": "div[@class = 'p-name']/a/em/text()",
                "comment": "div[@class = 'p-commit']/strong/a/text()",
                },
            "multidst": {
                "dp": {
                    "type": "list",
                    "name": "jd_dp",
                    "log": False,
                    },
                "price": {
                    "type": "list",
                    "name": "jd_book_price" 
                    },
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "jd_dps_log",
                    "log": False,
                    },
                "comment": {
                    "name": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "comment",
                    "pack": False,
                    "log": False
                    },
                "promo": {
                    "name": "jd_promo",
                    "type": "list",
                    "log": False,
                    "limit": 20000000
                    }
                },
            "test": (
                {
                    "url": "http://list.jd.com/list.html?cat=1713,3258&area=1,72,4137&page=284&delivery=0&stock=0&sort=sort_winsdate_desc&JL=4_6_0",
                    "check": "jd_book.test_list",
                    },
                ),
            "get": {
                "method": "get",
                "parser": "jd_book.list_parser",
                "not200": "log",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                }
            },
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_book_price",
                "batch": 6000,
                "group": True,
                "filter": "jd_book.price_filter",
                },
            "get": {
                "method": "get",
                "parser": "jd_book.price_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                    }
                },
            "dst": {
                "type": "list",
                "name": "jd_book_stock",
                },
        },
        {

            "type": "fetch",
            "name": "stock",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_book_stock",
                "batch": 300,
                "filter": "jd_book.stock_filter",
                },
            "get": {
                "method": "get",
                "parser": "jd_book.stock_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                    "keys": ("price",),
                    }
                },
            "dst": {
                "type": "list",
                "name": "spider_result"
            }
        }, 
        {
            "name": "promo",
            "type": "fetch",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_promo",
                "batch": 100,
                "filter": "jd.promo_filter"
                },
            "dst": {
                "name": "promo_result",
                "type": "list",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                    },
                "randua": True,
                "parser": "jd.promo_parser"
                }, 
            "test": [
                {
                    "url": "http://pi.3.cn/promoinfo/get?id=1089942922&area=12_904_905_0&origin=1&callback=Promotions.set",
                    "check": "jd.promo_test"
                    }
                ]
        } 
        )
