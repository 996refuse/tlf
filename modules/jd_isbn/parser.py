from spider import urlcrc
from spider import log_with_time
import pdb 
import re

def dp_filter(url):
    return {
            "url": url
            } 

def dp_parser(task, rule): 
    desc_url = re.findall("desc: '(http.*?desc/[0-9]+)'", task["text"]) 
    if not desc_url:
        log_with_time("no desc: %s" % task["url"])
        return
    crc = urlcrc.get_urlcrc(3, task["url"])
    return [(desc_url[0], str(crc), "")] 

def test_dp(items):
    pdb.set_trace()
