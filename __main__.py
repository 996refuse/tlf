#! /usr/bin/env python
#-*-encoding=utf8-*-
import os 
import sys 
import pdb 

if __name__ == "__main__": 
    path = "/".join(os.path.dirname(__file__).split("/")[:-1])
    sys.path.append(path) 
    import spider 
    argv = sys.argv
    arg1 = argv[1] 
    if arg1 == "all":
        spider.run() 
    elif arg1 == "debug":
        spider.debug = True
        spider.run_cat(argv[2], argv[3]) 
    elif arg1 == "test":
        if argv[2] == "me":
            spider.test_me()
        elif argv[2] == "modules":
            spider.test_modules()
        else:
            spider.load_worker_and_test(argv[2], argv[3]) 
    elif arg1 == "redis_proxy":
        from spider import redis_proxy
        redis_proxy.run()
    elif arg1 == "create":
        from spider import template
        template.create_module(argv[2], *argv[3:])
    else: 
        spider.run_cat(argv[1], argv[2]) 
