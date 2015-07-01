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
                }, 
            "diff_dps": {
                "host": "192.168.1.193",
                "port": 6380,
                "db": 0
                },
            "dps_log": {
                "host": "192.168.1.192",
                "port": 6379,
                "db": 0
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
        }


GENERAL = {
        "server_id": 170,
        "log_size": 256 * 1024 * 1024,
        }



SITES = {
        "jd": {
            "site_id": 3,
            "workers": ("list", "styles", "dp", "price", "stock"),
            "ignore": False
            },
        "jd_book": {
            "site_id": 3,
            "workers": ("list", ),
            "ignore": False
            },
        "gome": {
            "site_id": 28,
            "workers": ("dp", ),
            "ignore": False
            },
        "suning.nanjing": {
            "site_id": 25,
            "workers": ("pager", "list", "price", "book_price", "dp"),
            "ignore": False,
            },
        "suning.beijing": {
            "site_id": 1025,
            "workers": ("pager", "list", "price", "book_price"),
            "ignore": False
            },
        "suning.guangzhou": {
            "site_id": 2025,
            "workers": ("pager", "list", "price", "book_price"),
            "ignore": False
            },
        "suning.chengdu": {
            "site_id": 3025,
            "workers": ("pager", "list", "price", "book_price"),
            "ignore": False,
            },
        "yixun.chongqing": {
            "site_id": 4015,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            }, 
        "yixun.shanxi": {
            "site_id": 5015,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "dangdang": {
            "site_id": 2,
            "reload": 1,
            "workers": ("list", "dp", "offcheck"),
            "ignore": False,
            },
        "yhd.nanjing": {
            "site_id": 31,
            "reload": 1,
            "workers": ("dp", ),
            "ignore": False,
            }, 
        "yhd.hubei": {
            "site_id": 3031,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False
            }, 
        "feiniu": {
            "site_id": 180,
            "reload": 1,
            "workers": ("dp", ),
            "ignore": False,
            }, 
        "womai.huanan": {
            "site_id": 2032,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False,
            }, 
        }
