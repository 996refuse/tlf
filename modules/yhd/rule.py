rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.yhd.com/marketing/allproduct.html": ["//dd/em/span/a/@href"]},
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "yhd.cats_parser", 
                },
            "dst": {
                "name": "yhd_pager",
                "type": "list",
            },
            "test": [
            {
                "url": "http://www.yhd.com/marketing/allproduct.html",
                "check": "module_test"
            }
            ],
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": '//input[@id="pageCountPage"]/@value',
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yhd_pager",
                "batch": 30,
                "filter": "yhd.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "yhd_list", 
                },
            "get": {
                "method": "get",
                "parser": "yhd.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://list.yhd.com/c34641-0-0/",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/c31329-0-0/",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/c21770-0-85959/",
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
                "name": "yhd_list",
                "batch": 30,
                "filter": "yhd.list_filter",
                }, 
            "rule": "//div[@id='itemSearchList']/div", 
            "dst": { 
                "type": "list",
                "name": "yhd_stock",
                }, 
            "get": {
                "method": "get",
                "parser": "yhd.list_parser",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                } 
            },
            "test": [
            {
                "url": "http://list.yhd.com/c34641-0-0/",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/c31329-0-0/",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/c21770-0-85959/",
                "check": "module_test"
            },
            ]
        },
        {
            "name": "stock",
            "type": "fetch",
            "url": "http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite=1&provinceId=1&",
            "wait": 4,
            "src": {
                "name": "yhd_stock", 
                "type": "list",
                "batch": 16,
                "group": True,
                "filter": "yhd.stock_task_filter"
                }, 
            "get": {
                "method": "get",
                "parser": "yhd.stock_parser",
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