#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.feiniu.com/sitemap': "//div[@class='sitemap-col']/dl/dd/dl/dt/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "feiniu.cats", 
                },
            "dst": {
                "name": "feiniu_pager",
                "type": "list",
            },
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "feiniu_pager",
                "batch": 50,
                "filter": "feiniu.pager_filter",
            },
            "rule": "//span[contains(@class, 'page_count')]/text()",
            "dst": {
                "type": "list",
                "name": "feiniu_list",
            },
            "get": {
                "method": "get",
                "parser": "feiniu.pager",
                "args": {
                    "limit":10,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "feiniu_list",
                "batch": 50,
                "filter": "feiniu.list_filter",
                },
            "rule": {
                "nodes": "//ul[@id='cata_choose_product']/li/div",
                "gid": "div[@class='listPic']/a/@href",
            },
            "multidst": {
                "price": {
                    "type": "list",
                    "name": "feiniu_price",
                    },
                "dp": {
                    "type": "list",
                    "name": "feiniu_dp",
                    }
            },
            "get": {
                "method": "get",
                "parser": "feiniu.list_parser",
                "args": {
                    "limit": 10,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://www.feiniu.com/category/C18992/?page=11",
                "check": "module_test"
            }
            ]
        },
        {
            "type": "fetch",
            "name": "price",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "feiniu_price",
                "batch": 50,
                },
            "multidst": {
                "result": {
                    "type": "list",
                    "name": "spider_result",
                },
               "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "feiniu_dps_log"
                },
            },
            "get": {
                "method": "post",
                "parser": "feiniu.price_parser",
                "args": {
                    "limit": 10,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "feiniu_dp",
                "type": "list",
                "qtype": "dp",
                },
            "dst": {
                "name": "feiniu_dp",
                "type": "",
                "qtype": "dp",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False,
                },
                "redirect": 2,
            }, 
        }
)
