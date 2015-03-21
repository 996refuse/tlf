rule = (
{
            "name": "cats",
            "type": "fetch",

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
                }
            },
        {
            "type": "fetch",
            "name": "pager",
            "rule": '//input[@id="pageCountPage"]/@value',
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
            }
        },
        {
            "type": "fetch",
            "name": "list", 
            "src": {
                "type": "list",
                "name": "yhd_list",
                "batch": 30,
                "filter": "yhd.list_filter",
                }, 
            "rule": {
                "node": "//ul[@id='itemSearchList']/li", 
                "pid": "div/div/span[@productid]/@productid",
                "price": 'div/div/span[@productid]/@yhdprice',
                },
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
            }
        },
        {
            "name": "stock",
            "type": "fetch",
            "url": "http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite=1&provinceId=1&",
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