#-*-encoding=utf-8-*- 

rule = (
        {
            "name": "cats",
            "repeat": 7200,
            "type": "fetch",
            "from": { 
                "http://www.gome.com.cn/allcategory/":  ["//div[@class = 'item-bd']/div[@class = 'in']/a"], 
                }, 
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "gome.cats_parser"
                },
            "dst": {
                "name": "gome_list",
                "type": "list"
                },
            "period": "6-20"
            },
        {
            "name": "pager", 
            "type": "fetch", 
            "wait": 2,
            "src": {
                "type": "list",
                "name": "gome_list",
                "batch": 10,
                "filter": "gome.pager_filter",
                },
            "dst": {
                "type": "list",
                "name": "gome_page"
                }, 
            "get": { 
                "not200": "log",
                "method": "get", 
                "randua": True, 
                "args": {
                    "limit": 10, 
                    }, 
                "parser": "gome.pager", 
            },
        },
        {
            "name": "list",
            "type": "fetch",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "gome_page",
                "batch": 30, 
                }, 
            "get": { 
                "method": "get",
                "not200": "log",
                "randua": True,
                "args": {
                    "limit": 30, 
                    "copy_keys": ("old_url", ), 
                    },
                "parser": "gome.list_parser", 
                }, 
            "test": (
                {
                    "url": "http://www.gome.com.cn/category/cat21455614.html",
                    "check": "gome.test_list",
                    },
                ),
            "multidst": {
                "spider": {
                    "name": "spider_result",
                    "type": "list", 
                    }, 
                "dp": {
                    "name": "gome_dp",
                    "type": "list",
                    "node": "dp_pairs", 
                    },
                "dps_log": {
                    "node": "dps_log",
                    "type": "hash",
                    "name": "gome_dps_log",
                    },
                "shop": {
                    "node": "shop",
                    "type": "hash",
                    "with_siteid": True,
                    "name": "shop",
                    "pack": False
                    },
                "comment": {
                    "node": "comment",
                    "type": "hash",
                    "with_siteid": True,
                    "name": "comment",
                    "pack": False,
                    },
                "promo": { 
                    "type": "list",
                    "name": "gome_promo", 
                    "limit": 1000000
                    },
                }, 
            "test": [
                {
                    "url": "http://search.gome.com.cn/cloud/asynSearch?callback=callback_product&module=product&from=category&page=32&paramJson={+%22mobile%22+%3A+false+%2C+%22catId%22+%3A+%22cat15787588%22+%2C+%22catalog%22+%3A+%22coo8Store%22+%2C+%22siteId%22+%3A+%22coo8Site%22+%2C+%22shopId%22+%3A+%22%22+%2C+%22regionId%22+%3A+%2211010200%22+%2C+%22pageName%22+%3A+%22list%22+%2C+%22et%22+%3A+%22%22+%2C+%22XSearch%22+%3A+false+%2C+%22startDate%22+%3A+0+%2C+%22endDate%22+%3A+0+%2C+%22pageSize%22+%3A+48+%2C+%22state%22+%3A+4+%2C+%22weight%22+%3A+0+%2C+%22more%22+%3A+0+%2C+%22sale%22+%3A+0+%2C+%22instock%22+%3A+1+%2C+%22filterReqFacets%22+%3A++null++%2C+%22rewriteTag%22+%3A+false+%2C+%22userId%22+%3A+%22%22+%2C+%22priceTag%22+%3A+0+%2C+%22cacheTime%22+%3A+0+%2C+%22parseTime%22+%3A+7}&_=1432619492531",
                    "check": "gome.list_test",
                },
                {
                    "url": "http://search.gome.com.cn/cloud/asynSearch?callback=callback_productlist&module=product&from=category&page=1&paramJson=%7B+%22mobile%22+%3A+false+%2C+%22catId%22+%3A+%22cat15787588%22+%2C+%22catalog%22+%3A+%22coo8Store%22+%2C+%22siteId%22+%3A+%22coo8Site%22+%2C+%22shopId%22+%3A+%22%22+%2C+%22regionId%22+%3A+%2211010200%22+%2C+%22pageName%22+%3A+%22list%22+%2C+%22et%22+%3A+%22%22+%2C+%22XSearch%22+%3A+false+%2C+%22startDate%22+%3A+0+%2C+%22endDate%22+%3A+0+%2C+%22pageSize%22+%3A+48+%2C+%22state%22+%3A+4+%2C+%22weight%22+%3A+0+%2C+%22more%22+%3A+0+%2C+%22sale%22+%3A+0+%2C+%22instock%22+%3A+1+%2C+%22filterReqFacets%22+%3A++null++%2C+%22rewriteTag%22+%3A+false+%2C+%22userId%22+%3A+%22%22+%2C+%22priceTag%22+%3A+0+%2C+%22cacheTime%22+%3A+0+%2C+%22parseTime%22+%3A+7%7D&_=1432621008811",
                    "check": "gome.list_test",
                    }
                ]
        }, 
        {
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {
                "name": "gome_dp",
                "type": "list", 
                "batch": 30,
                "qtype": "dp",
                }, 
            "get": { 
                "method": "get", 
                "not200": "log",
                "randua": True,
                "args": {
                    "limit": 30, 
                }, 
            "not200": "log",
            }, 
            "dst": { 
                "node": "default",
                "qtype": "dp",
                "type": "",
                "name": "gome_dp"
                },
        }, 
        {
            "name": "promo",
            "type": "fetch",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "gome_promo",
                "batch": 100,
                "filter": "gome.promo_filter"
                },
            "dst": {
                "name": "promo_result",
                "type": "list",
                },
            "get": {
                "method": "get",
                "args": {
                    "limit": 20,
                    "interval": 1,
                    "debug": False, 
                    "key": ("old", )
                    },
                "not200": "pass",
                "parser": "gome.promo_parser"
                }, 
            "test": [
                {
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery17104623299303930253_1432705961310&goodsNo=8005947072&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PP01&zoneId=23010000&sid=pop8005947072&pid=A0005278399&programId=111111111&threeD=n&_=1432705961314",
                    "check": "gome.promo_test"
                    },
                {
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery17105603900919668376_1432712505544&goodsNo=8003502451&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PK01&zoneId=23010000&sid=pop8003502451&pid=A0004640266&programId=111111111&threeD=n&_=1432712505548",
                    "check": "gome.promo_test",
                    },
                {
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery1710016643482260406017_1432712943291&goodsNo=8005389422&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PK01&zoneId=23010000&sid=pop8005389422&pid=A0005152281&programId=111111111&threeD=n&_=1432712943296",
                    "check": "gome.promo_test",
                },
                {
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery17108558301122393459_1432712598416&goodsNo=8005473266&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PE01&zoneId=23010000&sid=pop8005473266&pid=A0005173188&programId=111111111&threeD=n&_=1432712598420",
                    "check": "gome.promo_test",
                    },
                {
                    #赠品
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery171028656046248371225_1432715378383&goodsNo=1000396505&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PK01&zoneId=23010000&sid=1120270131&pid=9131282446&programId=111111111&threeD=n&_=1432715378383",
                    "check": "gome.promo_test",
                    },
                {
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery171028656046248371225_1432715595277&goodsNo=1000403468&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PK01&zoneId=23010000&sid=1122170130&pid=9133251869&programId=111111111&threeD=n&_=1432715595277",
                    "check": "gome.promo_test",
                    },
                {
                    #满减2, 多个
                    "url": "http://g.gome.com.cn/ec/homeus/browse/store.jsp?callback=jQuery171028656046248371225_1432716282708&goodsNo=1000368738&city=23010100&areaId=230101001&siteId_p=&skuType_p=ZBBC&shelfCtgy3=PK01&zoneId=23010000&sid=1112810238&pid=9124060650&programId=111111111&threeD=n&_=1432716282708",
                    "check": "gome.promo_test",
                    }
                ]
        }
        )
