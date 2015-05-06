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
                }
            },
        {
            "name": "pager", 
            "type": "fetch", 
            "wait": 2,
            "src": {
                "type": "list",
                "name": "gome_list",
                "batch": 10,
                "filter": "gome.task_filter",
                },
            "dst": {
                "type": "list",
                "name": "gome_page"
                }, 
            "not200": "log",
            "get": {
                "async": True,
                "method": "post", 
                "randua": True, 
                "args": {
                    "limit": 10, 
                    "copy_keys": ("old_url", ), 
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
                "method": "post", 
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
                    }
                }, 
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
        }
        )
