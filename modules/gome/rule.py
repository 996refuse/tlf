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
                    "interval": 1, 
                    "debug": False,
                    "timeout": 10,
                    "copy_keys": ("old_url", ),
                    }, 
                "parser": "gome.pager"
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
                "async": True,
                "method": "post", 
                "not200": "log",
                "randua": True,
                "args": {
                    "limit": 30,
                    "interval": 1, 
                    "debug": False,
                    "timeout": 10, 
                    "copy_keys": ("old_url", ),
                    },
                "parser": "gome.list_parser", 
                }, 
            "multidst": {
                "spider": {
                    "name": "spider_result",
                    "type": "list", 
                    "log": False,
                    }, 
                "group": {
                    "name": "group_28",
                    "type": "hash",
                    "node": "group",
                    "pack": False,
                    "log": False,
                    }
                }, 
            } 
        )
