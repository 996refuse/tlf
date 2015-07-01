
rule = {
        
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 10000,
            "from": {
                
                },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "ocx.cats_parser",
                },
            "dst": {
                "name": "ocx_list",
                "type": "list",
                },

        },
    
        {
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": {
                },
            "src": {
                "type": "list",
                "name": "ocx_list",
                "batch": 30,
                "filter": "ocx.pager_filter", 
                },
            "dst": {
                "type": "list",
                "name": "ocx_page",
                },
            "get": {
                "method": "get",
                "parser": "ocx.pager", 
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                },
            },
            "test": (
                {
                    "url": ""
                    "check": "ocx.test_list",
                },
                )
        }, 
        
        {
            "type": "fetch",
            "name": "list",
            "wait": 2,
            "src": {
                "type": "list",
                "name": "ocx_page",
                "batch": 2000,
                "filter": "ocx.list_filter",
                },
            "rule": {

                },
            "multidst": {

                },
            "test": (
                {
                    "url": "",
                    "check": "ocx.test_list", 
                }, 
                ),
            "get": {
                "method": "get",
                "parser": "ocx.list_parser", 
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                },
            }
        }, 

        }
