#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
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
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "rule": "//div[@class='sort_page']/div[@class='sort_page_num']/span",
            "src": {
                "type": "list",
                "name": "yixun_pager",
                "batch": 30,
                "filter": "yixun.pager_filter"
            },
            "dst": {
                "type": "list",
                "name": "yixun_list",
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
            "wait": 4,
            "src": {
                "type": "list",
                "name": "yixun_list",
                "batch": 30,
                "filter": "yixun.list_filter",
            },
            "rule": {
                "nodes": "//ul[@id='itemList']/li/div/div[@class='mod_goods_info']",
                "gid": "p[@class='mod_goods_tit']/a/@href",
                "price": "p[@class='mod_goods_price']/span[@class='mod_price']/span",
                "stock": "div[@class='goods_more']//a[@class='goods_buy']"
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
)