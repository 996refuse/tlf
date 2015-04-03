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
            "workers": ("cats", "pager", "price", "list", "stock"),
            "ignore": False,
            }, 
        "jd_book": {
            "site_id": 3,
            "workers": ("cats", "pager", "price", "list", "stock"),
            "ignore": False,
            }, 
        "suning.nanjing": {
            "site_id": 25,
            "workers": ("cats", "pager", "list", "dp"),
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

