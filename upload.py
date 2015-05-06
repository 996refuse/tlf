
from fabric.api import *
import os

env.hosts = [
        "spider@115.182.16.78:22"
        ]

env.passwords = {
        "spider@115.182.16.78:22": "spider#@!" 
        }


def upload():
    x = os.system
    if not os.path.exists("./spider"):
        raise ValueError("can't find spider")
    x("mkdir temp")
    x("rsync -r spider temp/ --exclude spider/.git") 
    x("cd temp; find spider | grep .*pyc |xargs rm") 
    x("cd temp; find spider | grep .*sw. |xargs rm") 
    x("cd temp; tar -cjf spider.tar.bz2 spider")
    put("temp/spider.tar.bz2", "~")
    run("tar -mxvf spider.tar.bz2")
    x("rm -rf temp") 


def clean():
    run("cd work; rm -rf spider")



def killall():
    put("kill_worker.py", "~")
    run("python kill_worker.py spider")


