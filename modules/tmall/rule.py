rule = (
        {
            "name": "cats",
            "type": "fetch",
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "tmall.chaoshi_cats", 
                },
            "from": {
                "http://chaoshi.tmall.com": "//li[@class = 'j_Li']/h3/a/@href"
                },
            "dst": {
                "name": "tmall_chaoshi_pager",
                "type": "list",
                }
            },
        {
            "name": "pager",
            "type": "fetch",
            "src": {
                "type": "list", 
                "name":  "tmall_chaoshi_pager",
                "filter": "tmall.chaoshi_pager_filter",
                },
            "get": {
                "method": "get",
                "parser": "tmall.chaoshi_pager",
                },
            "dst": {
                "type": "list",
                "name": "tmall_chaoshi_page",
            }
        },
        {
            "name": "pager",
            "type": "fetch",
            "src": {
                "type": "list",
                "name":  "tmall_chaoshi_page",
                },
            "get": {
                "method": "get",
                "parser": "tmall.chaoshi_list",
                },
            "dst": {
                "type": "list",
                "name": "tmall_chaoshi_list",
            }
        }, 
        )
