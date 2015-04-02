#-*-encoding=utf-8-*- 

CLIENT = {
        "nodes": { 
            "default": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0
                }, 
            "group": { 
                "host": "127.0.0.1",
                "port": 6379,
                "db": 5,
                },
            "dp_pairs": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                }
            }, 
        "stat_redis": {
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0
            },
        "tt": {
            "host": "192.168.1.168",
            "port": 11261
            }, 
        "mysql": {
            "host": "127.0.0.1",
            "port": 3306,
            "db": "PriceStock",
            "user": "root",
            "passwd": "root_for_test_!@#",
            }, 
        "dp_idx": {
            "host": "127.0.0.1",
            "port": 3306,
            "db": "dp_idx",
            "user": "root",
            "passwd": "root_for_test_!@#"
            }, 
        "data_file": {
            "host": "127.0.0.1", 
            "port": 3306,
            "db": "dp_idx",
            "user": "root",
            "passwd": "root_for_test_!@#"
            },
        "llkv_list": {
            "host": "127.0.0.1",
            "port": 8000,
            },
        "llkv_dp": {
            "host": "127.0.0.1",
            "port": 8001 
            },
        "server_id": 170,
        } 

SITES = { 
        "suning": {
            "site_id": 25,
            "workers": ("cats", "pager"),
            "ignore": False
            }

        } 

