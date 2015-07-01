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
            "diff_dps": {
                "host": "192.168.1.193",
                "port": 6380,
                "db": 0
                },
            "dps_log": {
                "host": "192.168.1.192",
                "port": 6379,
                "db": 0,
                },
            "comment": {
                "host": "192.168.1.176",
                "port": 6379,
                "db": 1,
                },
            "shop": {
                "host": "192.168.1.176",
                "port": 6379,
                "db": 1,
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
        "llkv_promo": {
            "host": "192.168.1.194",
            "port": 8002 
            },
        "promo_tt": {
            "host": "192.168.1.168",
            "port": 6500
            }, 
        }


GENERAL = {
        "server_id": 170,
        "log_size": 256 * 1024 * 1024,
        }


SITES = {
        "commit": {
            "site_id": 0,
            "reload": 1,
            "workers": ("b2c", "promo"),
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
        "yhd.sichuan": {
            "site_id": 4031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            },
        "vip": {
            "site_id": 129,
            "reload": 1,
            "workers": ("cats", "pager", "list", "dp"),
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
            "workers": ("cats", "pager", "list", "price", "book_price"),
            "ignore": False,
            },
        "suning.beijing": {
            "site_id": 1025,
            "workers": ("pager", "list", "price", "book_price"),
            "ignore": False
            }, 
        "dangdang": {
            "site_id": 2,
            "reload": 1,
            "workers": ("list", "dp"),
            "ignore": False,
            },
        "feiniu": {
            "site_id": 180,
            "reload": 1,
            "workers": ("list", ),
            "ignore": False,
            }, 
        }
