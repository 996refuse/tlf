#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 2000,
            "from": {
                "http://list.mi.com/accessories/ajaxView/0-0-0-0-0-0": ""
            },
            "dst": {
                "name": "mi_page",
                "type": "list",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "mi.cats_parser"
            },
            "test": [
            {
                "url": "http://list.mi.com/accessories/ajaxView/0-0-0-0-0-0",
                "check": "module_test"
            }
            ]
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
            },
            "test": [
            {
                "url": "http://list.mi.com/accessories/ajaxView/0-0-0-0-20-0",
                "check": "module_test"
            },
            {
                "url": "http://list.mi.com/accessories/ajaxView/0-0-0-0-34-0",
                "check": "module_test"
            },
            {
                "url": "http://list.mi.com/accessories/ajaxView/0-0-0-0-52-0",
                "check": "module_test"
            },
            ]
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
            "multidst": {
                "spider": {
                    "type": "list",
                    "name": "spider_result",
                    },
                "dp": {
                    "type": "list",
                    "name": "mi_dp"
                    },
                },
            "get": {
                "method": "get",
                "parser": "mi.list_parser",
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                }
            },
            "test": [
            {
                "url": "http://list.mi.com/accessories/ajaxView/0-0-0-0-1-0",
                "check": "module_test_stock"
            }
            ]
)
