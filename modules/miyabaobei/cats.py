from lxml import etree
import pdb

base = "http://www.miyabaobei.com"

def cats_parser(url, content, rule): 
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        ret.extend([base+j for j in items if not j.startswith("http")]) 
    return ret
