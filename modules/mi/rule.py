#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "food",
            "food": ['http://list.mi.com/accessories/ajaxView/0-0-0-0-0-0'],
            "dst": {
                "name": "mi_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "",
            "src": {
                "type": "list",
                "name": "mi_list",
                "batch": 30,
                "filter": "mi.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "mi_page", 
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
            "src": {
                "type": "list",
                "name": "mi_page",
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