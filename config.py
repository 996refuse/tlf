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
            "site_id": 32,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "mi": {
            "site_id": 33,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "360kxr": {
            "site_id": 34,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "m6go": {
            "site_id": 35,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "bookschina": {
            "site_id": 36,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "zm7": {
            "site_id": 37,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "111": {
            "site_id": 38,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price", "stock"),
            "ignore": False,
            },
        "jiuxian": {
            "site_id": 39,
            "reload": 1,
            "workers": ("cats", "pager", "list", "price"),
            "ignore": False,
            },
        "gjw": {
            "site_id": 40,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock"),
            "ignore": False,
            },
        "zhiwo": {
            "site_id": 41,
            "reload": 1,
            "workers": ("cats", "pager", "list"),
            "ignore": False,
            },
        "d1": {
            "site_id": 42,
            "reload": 1,
            "workers": ("cats", "pager", "list", "stock1", "stock2"),
            "ignore": False,
            },
        "bookuu": {
            "site_id": 43,
            "reload": 1,
            "workers": ("cats", "list"),
            "ignore": False,
            },
}