#-*-encoding=utf-8-*-

CLIENT = {
        "nodes": {
            "default": {
                "host": "127.0.0.1",
                "port": 9000,
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
            } 
        }

GENERAL = {
    "log_size": 256 * 1024 * 1024 
}
