#-*-encoding=utf-8-*- 

CLIENT = {
        "nodes": { 
            "default": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0
                }, 
            "group": {
                "host": "192.168.1.165",
                "port": 6978,
                "db": 5,
                },
            }, 
        "tt": {
            "host": "192.168.1.168",
            "port": 11261
            }, 
        "mysql": {
            "host": "192.168.1.168",
            "port": 3308,
            "db": "PriceStock",
            "user": "minishop",
            "passwd": "MiniShop!@#"
            }, 
        "server_id": 170,
        } 


SITES = { 
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
            "workers": ("cats", "pager", "list", "stock"),
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
            "workers": ("pager", "list"),
            "ignore": False,
            },
        "lenovo": {
            "site_id": 135,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
}