rule = (
        {
            "name": "dp",
            "type": "dp",
            "wait": 2,
            "src": {
                "name": "winxuan_dp",
                "type": "list",
                }, 
            "dst": {
                "name": "winxuan_dp",
                "type": "list",
                },

            "get": {
                "method": "get", 
                "args": {
                    "limit": 30,
                    "interval": 1,
                    "debug": False, 
                }, 
            }
        }, 
       ) 
