
from lxml import etree

def cats_filter(url, content, rule):
    c = etree.HTML(content) 
    cats = t.xpath(rule[0])
    ret = []
    for i in cats:
        href = i.attrib["href"]
        if "list.jd" in href:
            ret.append((i.attrib["href"].encode("utf-8")))
    return ret


def pager_filter(x):
    return {
            "url": x
            }



def list_filter(x):
    return {
            "url": x
            }



#两个组过滤
def price_filter(b):
    pdb.set_trace()
    

def stock_filter(b):
    pdb.set_trace()

