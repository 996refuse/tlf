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
            },

        "sephora": {
            "site_id": 12,
            "reload": 1, 
            "workers": ("cats", "pager", "list"),
            "ignore": True,
            }, 
        "vip": {
            "site_id": 129,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": True,
            },
        "miyabaobei": {
            "site_id": 195,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": True,
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
            "ignore": True,
            }, 
        "yhd": {
            "site_id": 31,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "scn": {
            "site_id": 14,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "mi": {
            "site_id": 167,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "360kxr": {
            "site_id": 50,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price"),
            "ignore": False,
            },
        "m6go": {
            "site_id": 51,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "bookschina": {
            "site_id": 61,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "zm7": {
            "site_id": 138,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "111": {
            "site_id": 94,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price", "stock"),
            "ignore": False,
            },
        "jiuxian": {
            "site_id": 103,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price"),
            "ignore": False,
            },
        "gjw": {
            "site_id": 108,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "zhiwo": {
            "site_id": 140,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "d1": {
            "site_id": 115,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock1", "stock2"),
            "ignore": False,
            },
        "bookuu": {
            "site_id": 110,
            "reload": 1,
            "workers": ("cats", "list"),
            "ignore": False,
            },
        "vancl": {
            "site_id": 19,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False,
            },
        "lenovo": {
            "site_id": 135,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
}

