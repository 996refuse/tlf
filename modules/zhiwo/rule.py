#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "repeat": 20000,
            "from": {
                'http://www.zhiwo.com/mall': "//div[@class='col-sub']/div[@class='content-box']/ul/li/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "zhiwo.cats_parser", 
                },
            "dst": {
                "name": "zhiwo_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@id='paging']/li[last()-1]/a",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "zhiwo_pager",
                "batch": 30,
                "filter": "zhiwo.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "zhiwo_list", 
                },
            "get": {
                "method": "get",
                "parser": "zhiwo.pager",
                "args": {
                    "limit": 30,    
                    "interval": 1,
                    "debug": False
                }
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "wait": 4,
            "src": {
                "type": "list",
                "name": "zhiwo_list",
                "batch": 30,
                "filter": "zhiwo.list_filter",
                },
            "rule": "//ul[@id='bfd_show_fu']/li",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "zhiwo.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)