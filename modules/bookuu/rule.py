#-*-encoding=utf-8-*-
rule = (
        {
            "name": "cats",
            "type": "fetch",
            "from": {
                'http://search.bookuu.com/': "//div[@class='allcats']/div[contains(@class, 'cats-item')]/div/ul/li/a/@href",
            },
            "get": {
                "type": "simple",
                "method": "get",
                "parser": "bookuu.cats_parser", 
                },
            "dst": {
                "name": "bookuu_pager",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "pager",
            "rule": "//div[@id='paging']/li[last()-1]/a",
            "src": {
                "type": "list",
                "name": "bookuu_pager",
                "batch": 30,
                "filter": "bookuu.pager_filter"
                },
            "dst": {
                "type": "list",
                "name": "bookuu_list", 
                },
            "get": {
                "method": "get",
                "parser": "bookuu.pager",
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
            "src": {
                "type": "list",
                "name": "bookuu_list",
                "batch": 30,
                "filter": "bookuu.list_filter",
                },
            "rule": "//ul[@id='bfd_show_fu']/li",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "bookuu.list_parser",
                "args": {
                    "limit": 30,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)