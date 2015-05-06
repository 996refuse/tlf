#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
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
            },
            "test": [
            {
                "url": "http://www.d1.com.cn/",
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@class='GPager']/a[last()]/@href",
            "wait": 4,
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
            "test": [
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=014",
                "check": "module_test"
            },
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=030",
                "check": "module_test"
            },
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=020",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "d1_list",
                "batch": 30,
                "filter": "d1.list_filter",
                },
            "rule": {
                "nodes": "//ul[@class='m_t10']/li/div",
                "gid": "div[@class='g_title']/span/a/@href",
                "price": "div[@class='g_price']/span/font",
            },
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
            },
            "test": [
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=014&pageno=59",
                "check": "module_test"
            },
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=014&pageno=27",
                "check": "module_test"
            },
            {
                "url": "http://www.d1.com.cn/result.jsp?productsort=020&pageno=5",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "stock1",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "d1_stock1",
                "batch": 30,
            },
            "multidst": {
                "next": {
                    "type": "list",
                    "name": "d1_stock2",
                },
                "result": {
                    "type": "list",
                    "name": "spider_result"
                },
            },
            "get": {
                "async": True,
                "method": "post",
                "parser": "d1.stock1_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
        },
        {
            "type": "fetch",
            "name": "stock2",
            "wait": 4,
            "src": {
                "group": True,
                "type": "list",
                "name": "d1_stock2",
                "batch": 30,
                "filter": "d1.stock2_filter",
                },
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "d1.stock2_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)