
sites = {
    "source": "cats",
    "order": True,
    "sites": [
        (31, "nanjing"),
        (1031, "beijing"),
        (2031, "guangzhou"),
        (3031, "hubei"),
        (4031, "sichuan")
        ],
    }


rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                "http://www.yhd.com/marketing/allproduct.html": "//dl/dd/em/span/a/@href"
            },
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
            "boot": "yhd.set_province_id",
            "rule": "//div[ @class = 'select_page_num']/text()",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yhd_pager",
                "batch": 30,
                "filter": "yhd.pager_filter",
                "subsite": True,
                },
            "dst": {
                "type": "list",
                "name": "yhd_list",
                "subsite": True
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "yhd.pager",
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://list.yhd.com/c21359-0-0",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/c34905-0-0",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/vc2594-0-0",
                "check": "module_test"
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "boot": "yhd.set_province_id",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yhd_list",
                "batch": 100,
                "filter": "yhd.list_filter",
                "subsite": True
                },
            "rule": { 
                "node": "(//*[@id='itemSearchList']/*[@id]) | (//body/li)", 
                "price": ".//*[@yhdprice]/@yhdprice",
                "link": ".//a/@pmid",
                "comment": ".//a[contains(@id, 'pdlinkcomment_')]/text()",
                "shop": "(.//a[contains(@id, 'merchant_')]) | (.//a[contains(@onclick, 'store')])" 
            },
            "multidst": {
                "stock": {
                    "type": "list",
                    "name": "yhd_stock",
                    "subsite": True,
                },
                "dp": {
                    "type": "list",
                    "name": "yhd_dp",
                    },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "yhd_dps_log"
                },
                "comment": {
                    "name": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "comment",
                    "pack": False
                    },
                "shop": {
                    "name": "shop",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "shop",
                    "pack": False
                    } 
            },
            "get": {
                "method": "get",
                "parser": "yhd.list_parser",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                    "key": ("title", )
                }
            },
            "test": [ 
            {
                "url": "http://list.yhd.com/searchVirCateAjax/vc1599/c0/b/a-s1-v0-p4-price-d0-mid0-f0-k?callback=jsonp1435313370351&isGetMoreProducts=1&moreProductsDefaultTemplate=0&isLargeImg=0",
                "check": "yhd.list_test"
            }, 

            {
                "url": "http://list.yhd.com/searchPage/c33044-0-0/b/a-s1-v4-p13-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp1435310878717&?isGetMoreProducts=1&isLargeImg=1",
                "check": "yhd.list_test"
            }, 
            {
                "url": "http://list.yhd.com/searchPage/c33797-0-81144/b/a-s1-v0-p2-price-d0-f0-m1-rt0-pid-mid0-k/?callback=jsonp1435308845639&&isLargeImg=0",
                "check": "yhd.list_test"
            }, 


            ]
        },
        {
            "name": "stock",
            "type": "fetch",
            "wait": 4,
            "src": {
                "name": "yhd_stock",
                "type": "list",
                "batch": 800,
                "group": True,
                "filter": "yhd.stock_task_filter",
                "subsite": True,
                },
            "get": {
                "method": "get",
                "parser": "yhd.stock_parser",
                "args": {
                    "limit": 30,
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
            },
            "test": [
            {
                "url": " http://busystock.i.yihaodian.com/busystock/restful/truestock?mcsite=1&provinceId=1&productIds=37187310",
                "price": {"37187310": "233"},
                "check": "module_test_stock"
            }
            ]
        },
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "yhd_dp",
                "type": "list",
                "qtype": "dp",
                },
            "dst": {
                "name": "yhd_dp",
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
)
