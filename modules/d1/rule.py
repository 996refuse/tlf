#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://www.d1.com.cn/': "//div[@class='hmenu_txt']/ul/li[position()>2]/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "d1.cats_parser", 
                },
            "dst": {
                "name": "d1_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='GPager']/a[last()]/@href",
            "src": {
                "type": "list",
                "name": "d1_pager",
                "batch": 30,
                "filter": "d1.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "d1_list", 
                },
            "get": {
                "method": "get",
                "parser": "d1.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
        },
        {
            "type": "fetch",
            "name": "list",
            "src": {
                "type": "list",
                "name": "d1_list",
                "batch": 30,
                "filter": "d1.list_filter",
                },
            "rule": "//ul[@class='m_t10']/li/div",
            "dst": {
                "type": "list",
                "name": "d1_stock1",
                },
            "get": {
                "method": "get",
                "parser": "d1.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "stock1",
            "src": {
                "type": "list",
                "name": "d1_stock1",
                "batch": 30,
                },
            "dst": {
                "type": "list",
                "name": "d1_stock2",
                },
            "get": {
                "async": True,
                "method": "post",
                "parser": "d1.stock_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "stock2",
            "src": {
                "group": True,
                "type": "list",
                "name": "d1_stock2",
                "batch": 30,
                "filter": "d1.stock_filter",
                },
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "d1.stock_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)