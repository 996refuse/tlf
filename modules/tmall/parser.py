
from lxml import etree
import pdb



def chaoshi_cats(url, res, rule):
    t = etree.HTML(res["text"]) 
    return t.xpath(rule)


def chaoshi_pager(task, rule): 
    pass


def chaoshi_list(task, rule):
    pass
