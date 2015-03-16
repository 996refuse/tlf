#-*-encoding=utf-8-*-


rule = (
        {
            "name": "cats",
            "from": ["http://www.gome.com.cn/allcategory/"],
            "rule": "//div[@class = 'item-bd']/div[@class = 'in']/a",
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
            "src": {
                "type": "list",
                "name": "gome_list",
                "batch": 2,
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
                    "limit": 2,
                    "interval": 1, 
                    "debug": False,
                    "timeout": 10,
                    }, 
                "parser": "gome.pager"
                },
            },
        {
            "name": "list",
            "type": "fetch",
            "src": {
                "type": "list",
                "name": "gome_page",
                "batch": 2,
                "filter": "gome.list_task_filter",
                },
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "async": True,
                "method": "post",
                "args": {
                    "limit": 2,
                    "interval": 1, 
                    "debug": False,
                    "timeout": 10, 
                    },
                "parser": "gome.list_parser",
                "not200": "log",
                "randua": True
                },
            } 
        )
