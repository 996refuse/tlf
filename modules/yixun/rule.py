#-*-encoding=utf-8-*-

sites = { 
    "source": "cats", 
    "sites":[ 
        (15, "nanjing"),
        (1015, "beijing"), 
        (2015, "shenzhen"),
        (3015, "hubei"),
        (4015, "chongqing"),
        (5015, "shanxi"),
        ], 
    } 


rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 3600,
            "from": {
                "http://searchex.yixun.com/": "//div/div[@class='m_classbox']/div/dl/dt/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "yixun.cats",
            },
            "dst": {
                "name": "yixun_pager",
                "type": "list", 
                "subsite": True,
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "boot": "yixun.set_siteid",
            "wait": 4,
            "rule": "//div[@class='sort_page']/div[@class='sort_page_num']/span",
            "src": {
                "type": "list",
                "name": "yixun_pager",
                "batch": 30,
                "subsite": True,
                "filter": "yixun.pager_filter"
            },
            "dst": {
                "type": "list",
                "name": "yixun_list",
                "subsite": True
            },
            "get": {
                "method": "get",
                "parser": "yixun.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://searchex.yixun.com/706028-1-/",
                "check": "module_test_not",
            },
            ]
        },
        {
            "type": "fetch",
            "name": "list",
            "boot": "yixun.set_siteid",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yixun_list",
                "batch": 30,
                "subsite": True,
                "filter": "yixun.list_filter",
            },
            "rule": {
                "nodes": "//ul[@id='itemList']/li/div/div[@class='mod_goods_info']",
                "gid": "p[@class='mod_goods_tit']/a/@href",
                "price": "p[@class='mod_goods_price']/span[@class='mod_price']/span",
                "stock": "div[@class='goods_more']//a[@class='goods_buy']",
                "comment": "p/span[@class='goods_comments']/a/b/text()",
            },
            "multidst": {
                "result": {
                    "type": "list",
                    "name": "spider_result", 
                },
                "dps": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "yixun_dps_log"
                },
                "dp": {
                    "type": "list",
                    "name": "yixun_dp", 
                    },
                "comment": {
                    "name": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "node": "comment",
                    "pack": False
                    },
                "promos": {
                    "name": "yixun_promo",
                    "type": "list", 
                    "subsite": True,
                    }
            },
            "get": {
                "method": "get",
                "parser": "yixun.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://searchex.yixun.com/705798t706810-1-/55e5707?YTAG=3.2144315120020",
                "check": "module_test",
            },
            ]
        },
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "yixun_dp",
                "type": "list",
                "qtype": "dp",
                },
            "dst": {
                "name": "yixun_dp",
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
            "name": "promo",
            "type": "fetch",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "yixun_promo",
                "batch": 100,
                "subsite": True,
                "filter": "yixun.promo_filter"
                },
            "dst": {
                "name": "promo_result",
                "type": "list",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                    "client_type": "json",
                    },
                "randua": True,
                "parser": "yixun.promo_parser"
                }, 
            "test": [ 
                {
                    "url": "http://item.yixun.com/p/CGINewPromotion?pid=2203461&whid=1&product_sale_model=0",
                    "check": "yixun.promo_test",
                    "crc": 2203461
                    }, 
                { 
                    "url": "http://item.yixun.com/p/CGINewPromotion?pid=1958877&whid=1&product_sale_model=0",
                    "check": "yixun.promo_test",
                    "crc": 1958877
                    },
                {
                    "url": "http://item.yixun.com/p/CGINewPromotion?cids1=1007&cids2=45&cids3=129&pid=2199178&whid=1&product_sale_model=0",
                    "check": "yixun.promo_test",
                    "crc": 2199178
                    }
                ] 
        }
)
