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
                },
            "dps_log": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0
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
        "jd": {
            "site_id": 3,
            "reload": 1, 
            "workers": ("cats", "pager", "list", "dp"),
            "ignore": False,
            }, 
        "jd_book": {
            "site_id": 3,
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
        "gome": {
            "site_id": 28,
            "reload": 1, 
            "workers": ("cats", "pager", "list"),
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
            }, 
        "dangdang": {
            "site_id": 2,
            "workers": ("dp", ),
            "ignore": False,
            }, 
        "bookuu": {
            "site_id": 110,
            "workers": ("dp", "ips", "guard"),
            "ignore": False
            },
        "winxuan": {
            "site_id": 62,
            "workers": ("dp", ),
            "ignore": False
            }, 
        "amazon": {
            "site_id": 1,
            "workers": ("dp", "guard", "ips"),
            "ignore": False
            },
        "jd_isbn": {
            "site_id": 3,
            "workers": ("desc", "dp"),
            "ignore": False 
            }
        } 

