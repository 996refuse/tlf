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
                }, 
            "diff_dps": {
                "host": "192.168.1.193",
                "port": 6380,
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
            "workers": ("list", "styles", "offshelf", "dp", "price", "stock"),
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
        "d1": {
            "site_id": 115,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock1", "stock2"),
            "ignore": False,
            },
        "vancl": {
            "site_id": 19,
            "reload": 1,
            "workers": ("pager", "list", "stock"),
            "ignore": False,
            },

        "yougou": {
            "site_id": 93,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "zm7": {
            "site_id": 138,
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
        "dangdang": {
            "site_id": 2,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
}
