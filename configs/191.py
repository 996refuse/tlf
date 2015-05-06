#-*-encoding=utf-8-*- 

CLIENT = {
        "nodes": { 
            "default": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0
                }, 
            "dp_pairs": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                },
            "dps_log": {
                "host": "192.168.1.192",
                "port": 6379,
                "db": 0, 
                }, 
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
            "host": "192.168.1.194",
            "port": 8000,
            },
        "llkv_dp": {
            "host": "192.168.1.194",
            "port": 8001 
            },
        "server_id": 170,
        } 


SITES = { 
        "commit": {
            "site_id": 0,
            "reload": 1,
            "workers": ("commit",),
            "ignore": False
            },
        "idx": {
            "site_id": 0,
            "reload": 1,
            "workers": ("idx", ),
            "ignore": False
            },
        "sephora": {
            "site_id": 12,
            "reload": 1, 
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            }, 
        "yhd.nanjing": {
            "site_id": 31,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False
            },
        "yhd.beijing": {
            "site_id": 1031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            }, 
        "yhd.guangzhou": {
            "site_id": 2031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            }, 
        "yhd.hubei": {
            "site_id": 3031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            }, 
        "yhd.sichuan": {
            "site_id": 4031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            }, 
        "vip": {
            "site_id": 129,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "miyabaobei": {
            "site_id": 195,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False
            },
        "gome": {
            "site_id": 28,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False, 
            },
        "jd": {
            "site_id": 3,
            "workers": ("cats", "pager", "hotzone"),
            "ignore": False,
            }, 
        "jd_book": {
            "site_id": 3,
            "workers": ("cats", "pager", "price", "list", "stock"),
            "ignore": False,
            }, 
        "suning.nanjing": {
            "site_id": 25,
            "workers": ("cats", "pager", "list", "price"),
            "ignore": False,
            },
        "suning.beijing": {
            "site_id": 1025,
            "workers": ("pager", "list", "price"),
            "ignore": False
            } 
        } 

