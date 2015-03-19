#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
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
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='turnPageBottom']/a[@id='page_']/@pageno",
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
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "src": {
                "type": "list",
                "name": "111_list",
                "batch": 30,
                "filter": "111.list_filter",
                },
            "rule": "//ul[@id='itemSearchList']/li/div[not(contains(@class, 'none'))]",
            "dst": {
                "type": "list",
                "name": "111_price",
                },
            "get": {
                "method": "get",
                "parser": "111.list_parser",
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
            "src": {
                "group": True,
                "type": "list",
                "name": "111_price",
                "batch": 30,
                "filter": "111.price_filter",
                },
            "rule": "",
            "dst": {
                "type": "list",
                "name": "111_stock",
                },
            "get": {
                "method": "get",
                "parser": "111.price_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "name": "stock",
            "type": "fetch",
            "src": {
                "name": "111_stock",
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "111.stock_task_filter"
                },
            "rule": "//div[@class='o2o_box']/span[@class='o2o_note']",
            "get": {
                "method": "get",
                "parser": "111.stock_parser",
                "args": { 
                    "limit": 1,
                    "interval": 2, 
                    "debug": False, 
                    "timeout": 10, 
                    }, 
                "not200": "log", 
                "randua": True
                },
            "dst": {
                "name": "spider_result",
                "type": "list",
                }
        }
)