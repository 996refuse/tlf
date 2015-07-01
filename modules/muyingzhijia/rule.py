
rule = (
        
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                    "http://www.muyingzhijia.com/Shopping/alllist.aspx": "//li/dl[contains(@id, 'cateId')]/dd/a/@href"
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "muyingzhijia.cats_parser",
                },
            "dst": {
                "name": "muyingzhijia_list",
                "type": "list",
                }, 
            "period": "7-20",
        }, 
        {
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": "//div[@class = 'pagin']/span/text()", 
            "src": {
                "type": "list",
                "name": "muyingzhijia_list",
                "batch": 30,
                "filter": "muyingzhijia.pager_filter", 
                },
            "dst": {
                "type": "list",
                "name": "muyingzhijia_page",
                },
            "get": {
                "method": "get",
                "parser": "muyingzhijia.pager", 
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False
                },
            },
            "test": (
                {
                    "url": "http://www.muyingzhijia.com/Shopping/subcategory.aspx?cateID=468",
                    "check": "muyingzhijia.pager_test",
                },
                )
        }, 
        
        {
            "type": "fetch",
            "name": "list",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "muyingzhijia_page",
                "batch": 100,
                "filter": "muyingzhijia.list_filter",
                },
            "rule": {
                "node": "//ul[@class = 'goods_list']/li", 
                "gid": ".//*[@data-gid]/@data-gid",
                "link": "@data-url",
                },
            "multidst": {
                "price": {
                    "name": "muyingzhijia_stock",
                    "type": "list",
                    }, 
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "muyingzhijia_dps_log", 
                    },
                "dp": {
                    "type": "list",
                    "name": "muyingzhijia_dp", 
                    }, 
                },
            "test": (
                {
                    "url": "http://www.muyingzhijia.com/Shopping/subcategory.aspx?cateID=468&page=3",
                    "check": "muyingzhijia.list_test", 
                }, 
                ),
            "get": {
                "method": "get",
                "parser": "muyingzhijia.list_parser", 
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False,
                },
            }, 
        }, 
        {

            "type": "fetch",
            "name": "stock",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "muyingzhijia_stock",
                "batch": 300,
                "group": True,
                "filter": "muyingzhijia.stock_filter",
                },
            "get": {
                "method": "get",
                "parser": "muyingzhijia.stock_parser", 
                "args": {
                    "limit": 5,
                    "interval": 1,
                    "debug": False, 
                    },
                },
            "dst": {
                "type": "list",
                "name": "spider_result"
            },
            "test": (
                {
                    "url": "http://buy.api.muyingzhijia.com/json/reply/QueryPromPriceByProdId?a=0.30219353104828217&callback=jQuery17205880812340738396_1435391107448&ProductIdList=105805%2C105807%2C105815%2C108882%2C117093%2C117094%2C117095%2C117150%2C117152%2C117153%2C117156%2C117157%2C117163%2C117165%2C117166%2C117169%2C117170%2C117172%2C117173%2C117178%2C117218%2C117223%2C117231%2C117381%2C121467%2C121468%2C116396%2C117083%2C116454%2C117179%2C117380%2C108886%2C116397%2C105806%2C117180%2C103758%2C105813%2C108884%2C108885%2C117079&UserId=-1&Guid=201506231505da336e7b2898463db934ab1f5ed6836d&DisplayLabel=8&AreaSysNo=100&ChannelID=102&ExtensionSysNo=&_=1435391108640&__=0.8835533487323052",
                    "check": "muyingzhijia.stock_test",
                    }, 
                {
                    "url": "http://buy.api.muyingzhijia.com/json/reply/QueryPromPriceByProdId?a=0.30219353104828217&callback=jQuery17205880812340738396_1435391107448&ProductIdList=151442&UserId=-1&Guid=201506231505da336e7b2898463db934ab1f5ed6836d&DisplayLabel=8&AreaSysNo=100&ChannelID=102&ExtensionSysNo=&_=1435391108640&__=0.8835533487323052",
                    "check": "muyingzhijia.stock_test",

                    }
                )
        } , 
        )
