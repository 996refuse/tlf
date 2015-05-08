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
                "db": 0,
                },
            "dps_log": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                },
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
        "111": {
            "site_id": 94,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price", "stock"),
            "ignore": False,
            },
        "bookuu": {
            "site_id": 110,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "360kxr": {
            "site_id": 50,
            "reload": 1,
            "workers": ("mcats", "scats", "pager", "list", "price"),
            "ignore": False,
            },
        "jiuxian": {
            "site_id": 103,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price"),
            "ignore": True,
            },
        "gjw": {
            "site_id": 108,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": True,
            },
        "d1": {
            "site_id": 115,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock1", "stock2"),
            "ignore": True,
            },
        "lenovo": {
            "site_id": 135,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": True,
            },
        "bookschina": {
            "site_id": 61,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "vancl": {
            "site_id": 62,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
}
