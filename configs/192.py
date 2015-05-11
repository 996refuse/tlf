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
            "dps_log": {
                "host": "192.168.1.192",
                "port": 6379,
                "db": 0
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
            "workers": ("pager", "list", "price", "dp"),
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
        "mi": {
            "site_id": 167,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "111": {
            "site_id": 94,
            "reload": 1,
            "workers": ("cats", "pager", "list", "item", "price"),
            "ignore": False,
        },
        "360kxr": {
            "site_id": 50,
            "reload": 1,
            "workers": ("mcats", "scats", "pager", "list", "price"),
            "ignore": False,
            },
        "bookschina": {
            "site_id": 61,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "bookuu": {
            "site_id": 110,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "m6go": {
            "site_id": 51,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "yixun": {
            "site_id": 15,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "womai": {
            "site_id": 32,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False,
            },
}
