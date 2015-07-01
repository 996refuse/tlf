rule = (
        {
            "name": "dp",
            "type": "dp",
            "wait": 2,
            "src": {
                "name": "yihaodian_dp",
                "type": "list",
                }, 
            "dst": {
                "name": "yihaodian_dp",
                "type": "list",
                },

            "get": {
                "method": "get", 
                "args": {
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                }, 
            }
        }, 
       ) 
