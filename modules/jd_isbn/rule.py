rule = ( 
        {
            "type": "fetch",
            "name": "desc", 
            "wait": 2,
            "src": {
                "type": "list",
                "name": "jd_isbn_dp",
                "batch": 100,
                "filter": "jd.list_filter",
                }, 
            "dst": {
                "name": "jd_isbn_desc",
                "type": "list", 
                },
            "get": {
                "method": "get",
                "parser": "jd_isbn.dp_parser",
                "not200": "log", 
                "args": {
                    "limit": 50,    
                    "interval": 1,
                    "debug": False, 
                }, 
            },
            "test": (
                {
                    "url": "http://item.jd.com/1360789194.html",
                    "check": "jd_isbn.test_dp",
                }, 
                )
        }, 
        {
            "name": "dp",
            "type": "dp", 
            "wait": 2,
            "src": { 
                "name": "jd_isbn_desc",
                "type": "list", 
                },
            "dst": { 
                "name": "jd_isbn_desc",
                "type": "none", 
                }, 
            "get": {
                "method": "get", 
                "args": {
                    "limit": 50,
                    "interval": 1,
                    "debug": False, 
                }, 
            },
        } 
    )
        
