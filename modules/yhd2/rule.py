
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
                "http://www.yhd.com/marketing/allproduct.html": "//dd/em/span/a/@href",
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
            "rule": "//div[@class='search_select_page']/div",
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
                "nodes1": "//div[@id='itemSearchList']/div",
                "nodes2": "//li/div[contains(@class, 'search_item_box') and not(contains(@class, 'none'))]",
                "price1": "div/p[contains(@class, 'proPrice')]/em",
                "price2": "div[contains(@class, 'pricebox')]/span[1]",
                "comment1": "div/p[contains(@class, 'proPrice')]/span[@class='comment']/a/text()",
                "comment2": "p[@class='comment']/a/text()",
                "store1": "div[contains(@class, 'owner')]/a",
                "store2": "div/p[@class = 'storeName']/a",
                "link": ".//a/@pmid",
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
                "url": "http://list.yhd.com/searchPage/c32307-0-84337/b/a-s1-v0-p13-price-d0-f0-m1-rt0-pid-mid0-k",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/searchPage/c23597-0-91235/b/a-s1-v0-p45-price-d0-f0-m1-rt0-pid-mid0-k",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/searchPage/c5073-0-84464/b/a-s1-v0-p7-price-d0-f0-m1-rt0-pid-mid0-k",
                "check": "module_test"
            },
            {
                "url": "http://list.yhd.com/searchPage/c35574-0-0/b/a-s1-v0-p12-price-d0-f0-m1-rt0-pid-mid0-k",
                "check": "module_test"
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
