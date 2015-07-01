import os 
import pdb

cats_rule = """
        {{
            "name": "cats",
            "type": "fetch",
            "repeat": 10000,
            "from": {{
                
                }},
            "get": {{
                "type": "simple",
                "method": "get",
                "parser": "{site}.cats_parser",
                }},
            "dst": {{
                "name": "{site}_list",
                "type": "list",
                }},

        }},
    """


cats_parser = """ 
def cats_parser(url, res, rule):
    t = etree.HTML(res["text"])
    return t.xpath(rule)
"""


pager_rule = """
        {{
            "type": "fetch",
            "name": "pager",
            "wait": 2,
            "rule": {{
                }},
            "src": {{
                "type": "list",
                "name": "{site}_list",
                "batch": 30,
                "filter": "{site}.pager_filter", 
                }},
            "dst": {{
                "type": "list",
                "name": "{site}_page",
                }},
            "get": {{
                "method": "get",
                "parser": "{site}.pager", 
                "args": {{
                    "limit": 30,
                    "interval": 1,
                    "debug": False
                }},
            }},
            "test": (
                {{
                    "url": "",
                    "check": "{site}.pager_test",
                }},
                )
        }}, 
        """


pager_filter = """
def pager_filter(x):
    return {{
            "url": x
            }} 
"""

pager_parser = """
def pager(task, rule):
    t = etree.HTML(task["text"]) 
"""


list_rule = """
        {{
            "type": "fetch",
            "name": "list",
            "wait": 2,
            "src": {{
                "type": "list",
                "name": "{site}_page",
                "batch": 2000,
                "filter": "{site}.list_filter",
                }},
            "rule": {{
                "node": "", 
                }},
            "multidst": {{ 
                "dps_log": {{
                    "node": "dps_log",
                    "type": "hash",
                    "name": "{site}_dps_log", 
                    }},
                "dp": {{
                    "type": "list",
                    "name": "{site}_dp", 
                    }}, 
                }},
            "test": (
                {{
                    "url": "",
                    "check": "{site}.list_test", 
                }}, 
                ),
            "get": {{
                "method": "get",
                "parser": "{site}.list_parser", 
                "args": {{
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                }},
            }}
        }}, 
"""


list_filter = """
def list_filter(x):
    return {{
            "url": x
            }} 
"""


list_parser = """
def list_parser(task, rule):
    t = etree.HTML(task["text"]) 
    nodes = t.xpath(rule["node"]) 
    if not nodes:
        log_with_time("node rule error: %s" % task["url"])
        return 
    dp = []
    dps = {}
    ret = [] 
    now = int(time.time())
    for node in nodes:
        pass 
"""


dp_rule = """
        {{
            "name": "dp",
            "type": "fetch",
            "wait": 2,
            "src": {{
                "name": "{site}_dp",
                "type": "list",
                "qtype": "dp",
                }},
            "dst": {{
                "name": "{site}_dp",
                "type": "",
                "qtype": "dp",
                }},
            "get": {{
                "method": "get",
                "args": {{
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                }},
                "redirect": 2,
            }},
        }}, 
"""

diff_dps_rule = """
        {{
            "type": "diff_dps",
            "name": "diff_dps",
            "wait": 86400,
            "src": {{
                "type": "hash",
                "node": "dps_log",
                "name": "dps_log",
                }}, 
            "dst": {{
                "type": "list",
                "name": "{site}_diff_dps",
                "node": "diff_dps",
                "log": False
                }}
        }}, 
"""


offshelf_rule = """
        {{
            "name": "offshelf",
            "type": "fetch",
            "wait": 2,
            "src": {{
                "type": "list",
                "name": "{site}_diff_dps",
                "batch": 600,
                "group": True,
                "node": "diff_dps",
                "filter": "{site}.off_filter",
                }},
            "dst": {{
                "name": "{site}_stock",
                "type": "list",
                }},
            "get": {{
                "method": "get",
                "args": {{
                    "limit": 100,
                    "interval": 1,
                    "debug": False,
                }},
                "randua": True,
                "parser": "{site}.offshelf_parser",
            }},
        }}, 
        """


offshelf_parser = """
def offshelf_parser(task, rule):
    t = etree.HTML(task["text"]) 
"""



offshelf_filter = """
def offshelf_filter(x):
    return {{
            "url": x
            }} 
""" 

stock_filter = """
def stock_parser(task, rule): 
    try:
        j = jsonp_json(task["text"].decode("utf-8"))
    except Exception as e:
        log_with_time("response error: %s %s" % (task["url"], e)) 
        return 
"""

stock_parser = """
        {{

            "type": "fetch",
            "name": "stock",
            "wait": 2,
            "src": {{
                "type": "list",
                "name": "{site}_stock",
                "batch": 300,
                "filter": "{site}.stock_filter",
                }},
            "get": {{
                "method": "get",
                "parser": "muyingzhijia.stock_parser",
                "randua": True,
                "not200": "log",
                "args": {{
                    "limit": 100,
                    "interval": 1,
                    "debug": False, 
                    }},
                }},
            "dst": {{
                "type": "list",
                "name": "spider_result"
            }},
            "test": (
                {{
                    "url": "",
                    "check": "{site}.stock_test",
                    }},
                )
        }}, 
"""

roles = {
        "cats": (cats_rule, cats_parser, None),
        "pager": (pager_rule, pager_parser, pager_filter),
        "list": (list_rule, list_parser, list_filter),
        }


init_base = "from filter import *\nfrom parser import *\nfrom rule import *\n" 


rule_base = """
rule = ( 
        {rule}
       ) 
""" 


filter_base = """
from spider import split_list_iter
import pdb
import time 
{rule}
"""



parser_base = """ 
import re
import time
import pdb
from lxml import etree
from spider import log_with_time
from spider import jsonp_json
from spider import format_price 
{rule}
""" 

test_base = """
def {name}_test(items):
    assert items 
"""

def write_file(fn, content): 
    f = open(fn, "w+") 
    f.write(content)
    f.close()      


def create_module(fn, *role_names): 
    _ = os.path.join
    spider_path = os.path.dirname(__file__)
    path =_(spider_path, "modules/%s" % fn)
    os.makedirs(path) 
    rules = []
    filters = []
    parsers = []
    for name in role_names: 
        if name not in roles:
	  continue
	rule, parser, filter = roles[name] 
        if rule: rules.append(rule)
        if filter: filters.append(filter)
        if parser:
            parsers.append(parser) 
            parsers.append(test_base.format(name = name)) 
    write_file(_(path, "__init__.py"), init_base)
    write_file(_(path, "rule.py"), rule_base.format(rule="".join(rules).format(site=fn)))
    write_file(_(path, "filter.py"), filter_base.format(rule="".join(filters).format(site=fn)))
    write_file(_(path, "parser.py"), parser_base.format(rule="".join(parsers).format(site=fn))) 
