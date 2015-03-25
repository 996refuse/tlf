#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "food",
            "repeat": 20000,
            "food": ['http://list.mi.com/accessories/ajaxView/0-0-0-0-0-0'],
            "dst": {
                "name": "mi_page",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "mi_page",
                "batch": 30,
                "filter": "mi.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "mi_list", 
                },
            "get": {
                "method": "get",
                "parser": "mi.pager",
                "args": {
                    "limit": 30,    
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
                "name": "mi_list",
                "batch": 30,
                "filter": "mi.list_filter",
                },
            "rule": "",
            "dst": {
                "type": "list",
                "name": "spider_result", 
                },
            "get": {
                "method": "get",
                "parser": "mi.list_parser",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            }
        }
)