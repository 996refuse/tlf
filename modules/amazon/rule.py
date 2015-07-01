rule = (
        {
            "name": "guard",
            "type": "guard", 
            "src": {
                "name": "amazon_dp",
                "type": "set",
                },
            "dst": {
                "name": "amazon_dp_queue",
                "type": "list",
                }
        },
        {
            "name": "dp",
            "type": "dp",
            "wait": 2,
            "src": {
                "name": "amazon_dp_queue",
                "origin": "amazon_dp",
                "proxysrc": "amazon_ips",
                "type": "list", 
                "proxy": True,
                }, 
            "dst": {
                "name": "amazon_dp",
                "type": "list",
                }, 
            "get": {
                "method": "get", 
                "args": {
                    "limit": 400,
                    "interval": 1,
                    "debug": False, 
                }, 
            }
        }, 
        {
            "name": "ips",
            "type": "ips",
            "url": "http://www.amazon.cn",
            "src": {
                "name": "amazon_ips",
                "type": "set"
                }, 
            "dst": {
                "name": "amazon_ips",
                "type": "set"
                },
            "get": {
                "method": "get", 
                "args": {
                    "limit": 500,
                    "interval": 1, 
                    "keys": ("proxy", "check")
                }, 
                "randua": True,
                "parser": "amazon.test_ips"
            },
        }
       ) 
