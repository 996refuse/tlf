from lxml import etree 

def cats_parser(url, content,  rule): 
    t = etree.HTML(content)
    ret = []
    for i in rule:
        items = t.xpath(i)
        ret.extend(items)
    return ret

