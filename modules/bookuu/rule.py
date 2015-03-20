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
                "name": "bookuu_list",
                "type": "list",
            }
        },
        {
            "type": "fetch",
            "name": "list",
            "src": {
                "type": "list",
                "name": "bookuu_list",
                "batch": 10,
                "filter": "bookuu.list_filter",
                },
            "rule": "//div[@class='main-wrap']/div[contains(@class, 'books-list')]",
            "dst": {
                "type": "list",
                "name": "spider_result",
                },
            "get": {
                "method": "get",
                "parser": "bookuu.list_parser",
                "args": {
                    "limit": 1,  
                    "interval": 1,
                    "debug": False
                }
            }
        },
)