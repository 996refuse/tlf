#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "",
            },
            "dst": {
                "name": "",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "",
            "src": {
                "type": "list",
                "name": "",
                "batch": 30,
                "filter": ""
            },
            "dst": {
                "type": "list",
                "name": "",
            },
            "get": {
                "method": "get",
                "parser": "",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            },
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "",
                "batch": 30,
                "filter": "",
            },
            "rule": "",
            "dst": {
                "type": "list",
                "name": "",
            },
            "get": {
                "method": "get",
                "parser": "",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "stock",
            "src": {
                "group": True,
                "type": "list",
                "name": "",
                "batch": 30,
                "filter": "",
                },
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)