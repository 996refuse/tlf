#-*-encoding=utf-8-*- 

CLIENT = {
        "nodes": { 
            "default": {
                "host": "192.168.1.191",
                "port": 6379,
                "db": 0
                }, 
            "dp_pairs": {
                "host": "192.168.1.191",
                "port": 6379,
                "db": 0,
                }
            }, 
        "mysql": {
            "host": "192.168.1.168",
            "port": 3308,
            "db": "PriceStock",
            "user": "minishop",
            "passwd": "MiniShop!@#"
            }, 
        "dp_idx": {
            "host": "192.168.1.192",
            "port": 3306,
            "db": "dp_idx",
            "user": "minishop",
            "passwd": "MiniShop!@#"
            }, 
        "data_file": {
            "host": "192.168.1.192", 
            "port": 3306,
            "db": "dp_idx",
            "user": "minishop",
            "passwd": "MiniShop!@#"
            },
        "llkv_list": {
            "host": "192.168.1.191",
            "port": 8000,
            },
        "llkv_dp": {
            "host": "192.168.1.191",
            "port": 8001 
            },
        "server_id": 170,
        } 


SITES = { 
        "suning.nanjing": {
            "site_id": 25,
            "workers": ("pager", "list", "price"),
            "ignore": False,
            },
        "suning.beijing": {
            "site_id": 1025,
            "workers": ("pager", "list", "price"),
            "ignore": False
            },
        "suning.guangzhou": {
            "site_id": 2025,
            "workers": ("pager", "list", "price"),
            "ignore": False
            }, 
        "suning.chengdu": {
            "site_id": 3025,
            "workers": ("pager", "list", "price"),
            "ignore": False,
            }, 
        }
