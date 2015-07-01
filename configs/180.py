#-*-encoding=utf-8-*-

CLIENT = {
        "nodes": {
            "default": {
                "host": "127.0.0.1",
                "port": 9000,
                "db": 0
                }, 
            "diff_dps": {
                "host": "127.0.0.1",
                "port": 6380,
                "db": 0 
                },
            }, 
        "server_id": 170,
        } 

SITES = {
        "jd": {
            "site_id": 3,
            "workers": ("promo", ),
            "reload": 1,
            "ignore": False
            },
        "gome": {
            "site_id": 28,
            "workers": ("promo", ),
            "reload": 1,
            "ignore": False
            }, 
        "yixun.nanjing": {
            "site_id": 15,
            "reload": 1,
            "workers": ("promo",  ),
            "ignore": False,
            }, 
        "yixun.hubei": {
            "site_id": 3015,
            "reload": 1,
            "workers": ("promo", ),
            "ignore": False,
            }, 
        "yixun.beijing": {
            "site_id": 1015,
            "reload": 1,
            "workers": ("promo", ),
            "ignore": False,
            }, 
        "yixun.shenzhen": {
            "site_id": 2015,
            "reload": 1,
            "workers": ("promo", ),
            "ignore": False,
            }, 
        "yixun.chongqing": {
            "site_id": 4015,
            "reload": 1,
            "workers": ("promo", ),
            "ignore": False,
            }, 
        "yixun.shanxi": {
            "site_id": 5015,
            "reload": 1,
            "workers": ("promo", ),
            "ignore": False,
            }, 
        "suning.nanjing": {
            "site_id": 25,
            "workers": ("offshelf", ),
            "ignore": False,
            },
        "suning.beijing": {
            "site_id": 1025,
            "workers": ("offshelf", ),
            "ignore": False
            }, 
        "suning.guangzhou": {
            "site_id": 2025,
            "workers": ("offshelf", ),
            "ignore": False
            },
        "suning.chengdu": {
            "site_id": 3025,
            "workers": ("offshelf", ),
            "ignore": False,
            },
        }
