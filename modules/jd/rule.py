rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.jd.com/allSort.aspx": ["//div[@class = 'mc']/dl/dd/em/a"],
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "jd.cats_parser",
                },
            "dst": {
                "name": "jd_list",
                "type": "list",
                }
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": "//div[@class = 'f-pager']/span/i/text()",
            "src": {
                "type": "list",
                "name": "jd_list",
                "batch": 30,
                "filter": "jd.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "jd_page", 
                },
            "get": {
                "method": "get",
                "parser": "jd.pager",
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
                "name": "jd_page",
                "batch": 30,
                "filter": "jd.list_filter",
                }, 
            "rule": {
                "node": "//li[@class = 'gl-item']", 
                },
            "dst": { 
                "type": "list",
                "name": "jd_price", 
                }, 
            "get": {
                "method": "get",
                "parser": "jd.list_parser",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                } 
            }
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_price",
                "batch": 300,
                "group": True,
                "filter": "jd.price_filter",
                }, 
            "get": {
                "method": "get",
                "parser": "jd.price_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                    }
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
                "batch": 30, 
                "filter": "jd.stock_filter",
                },
            "get": { 
                "method": "get",
                "parser": "jd.stock_parser",
                "randua": True,
                "not200": "log",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False,
                    "keys": ("price",)
                    } 
                },
            "dst": {
                "type": "list",
                "name": "spider_result"
            } 
        } 
        )
        
