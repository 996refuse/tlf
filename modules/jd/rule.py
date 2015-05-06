rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000, 
            "from": { 
                "http://www.jd.com/allSort.aspx":  ["//div[@class = 'mc']/dl/dd/em/a"],
                "http://d.jd.com/category/get?callback=getCategoryCallback":"", 
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "jd.cats_parser",
                },
            "dst": {
                "name": "jd_list",
                "type": "list",
                }, 
            "price_range": "price_range",
        }, 
        {
            "name": "hotzone",
            "type": "fetch",
            "repeat": 1200, 
            "hotlimit": 10,
            "from": { 
                "http://www.jd.com/allSort.aspx":  ["//div[@class = 'mc']/dl/dd/em/a"],
                "http://d.jd.com/category/get?callback=getCategoryCallback":"", 
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "jd.cats_parser",
                },
            "dst": {
                "name": "jd_list",
                "type": "list",
                }, 
            "price_range": "price_range",
        }, 
        {
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": {
                "normal": "//div[@class = 'f-pager']/span/i/text()", 
                "test1": "//div[contains(@class, 'pagin')]/span/i/text()"
                },
            "src": {
                "type": "list",
                "name": "jd_list",
                "batch": 30,
                "filter": "jd.pager_filter",
                "qtype": "redis",
                },
            "dst": {
                "type": "list",
                "name": "jd_page", 
                },
            "get": {
                "method": "get",
                "parser": "jd.pager",
                "not200": "log", 
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }, 
            },
            "test": (
                {
                    "url": "http://list.jd.com/list.html?cat=6728,6745,11953&ev=exprice_M180L200%40",
                    "check": "jd.test_list",
                },
                ) 
        },
        {
            "type": "fetch",
            "name": "styles",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_styles",
                "batch": 100,
                "filter": "jd.styles_filter", 
                },
            "rule": "colorSize\s*:(.*]),",
            "multidst": {
                "price": {
                        "name": "jd_price",
                        "type": "list",
                        },
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "jd_dps_log", 
                    }
                },
            "get": {
                "method": "get",
                "parser": "jd.styles_parser",
                "not200": "log", 
                "args": {
                    "limit": 100,    
                    "interval": 1,
                    "debug": False, 
                }, 
            },
            "test": (
                {
                    "url": "http://item.jd.com/1075935341.html",
                    "check": "jd.test_list", 
                }, 
                { 
                    "url": "http://item.jd.com/1117108069.html",
                    "check": "jd.test_list"
                }
                ) 
        },
        {
            "type": "fetch",
            "name": "list", 
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_page",
                "batch": 100,
                "filter": "jd.list_filter",
                }, 
            "rule": {
                "node": "//li[@class = 'gl-item']", 
                "title": "div/div[@class = 'p-name']/a/em/text()",
                "group": "div/div[contains(@class, 'p-scroll')]/span/div/ul/li[@class = 'ps-item']/a/img",
                "comment": "div/div[@class = 'p-commit']/strong/a/text()",
                },
            "multidst": {
                "dp": {
                    "type": "list",
                    "name": "jd_dp", 
                    },
                "price": {
                    "type": "list",
                    "name": "jd_price"
                    },
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "jd_dps_log",
                    },
                "styles": {
                    "type": "list",
                    "name": "jd_styles",
                    },
                #"comment": { 
                #    "name": "comment",
                #    "type": "str",
                #    "node": "comment", 
                #    "key_pat": ("%s-%s", "site_id"),
                #    "pack": False
                #    }
                }, 
            "test": (
                {
                    "url": "http://list.jd.com/list.html?cat=1315,1343,9719",
                    "check": "jd.test_list",
                    "ignore": True
                },
                {
                    "url": "http://list.jd.com/list.html?cat=1315,1342,1350",
                    "check": "jd.test_list",
                    "ignore": True
                },
                {
                    "url": "http://list.jd.com/list.html?cat=1315,1343,9719",
                    "check": "jd.test_list", 
                    }
                ),
            "get": {
                "method": "get",
                "parser": "jd.list_parser",
                "not200": "log", 
                "args": {
                    "limit": 100,    
                    "interval": 1,
                    "debug": False, 
                }, 
            }
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_price",
                "batch": 6000,
                "group": True,
                "filter": "jd.price_filter",
                }, 
            "get": {
                "method": "get",
                "parser": "jd.price_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                    }, 
                },
            "dst": {
                "type": "list", 
                "name": "jd_stock",
                },
        },
        {

            "type": "fetch",
            "name": "stock",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_stock",
                "batch": 300, 
                "filter": "jd.stock_filter",
                },
            "get": { 
                "method": "get",
                "parser": "jd.stock_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                    "keys": ("price",), 
                    }, 
                },
            "dst": {
                "type": "list",
                "name": "spider_result"
            },
            "test": (
                {
                    "url": "http://st.3.cn/gsis.html?type=getstocks&skuids=1471467083&provinceid=1&cityid=72&areaid=2799&callback=jsonp121212&_=125121",
                    "price": {
                        "1471467083": "100",
                        },
                    "check": "jd.test_list",
                    },
                )
        } ,
        {
            "name": "dp",
            "type": "fetch", 
            "wait": 2,
            "src": { 
                "name": "jd_dp",
                "type": "list", 
                "qtype": "dp",
                },
            "dst": { 
                "name": "jd_dp",
                "type": "",
                "qtype": "dp",
                }, 
            "get": {
                "method": "get", 
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                }, 
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
                },
            "wait": 50000, 
            "dst": {
                "type": "list",
                "name": "jd_diff_dps",
                "node": "diff_dps",
                "log": False
                }
        }, 
        {
            "name": "offshelf",
            "type": "fetch", 
            "wait": 2,
            "src": { 
                "type": "list",
                "name": "jd_diff_dps",
                "batch": 600, 
                "group": True,
                "node": "diff_dps",
                "filter": "jd.off_filter",
                },
            "dst": { 
                "name": "jd_stock",
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
                "parser": "jd.price_parser",
            }, 
        }, 
        )
        
