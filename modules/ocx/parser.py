
from lxml import etree
 
def cats_parser(url, res, rule):
    t = etree.HTML(res["text"])
    return t.xpath(rule)

def cats_test(items):
    assert items 

def pager(task, rule):
    t = etree.HTML(res["text"]) 

def pager_test(items):
    assert items 

def list_parser(task, rule):
    t = etree.HTML(res["text"]) 

def list_test(items):
    assert items 

