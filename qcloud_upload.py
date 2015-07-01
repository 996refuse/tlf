
from fabric.api import *
import os

env.hosts = [ 
        "spider@115.159.50.207:22"
        ]

env.passwords = { 
        "spider@115.159.50.207:22": "spider#@!"
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


def install_tess():
    put("tess", "~/")
    sudo("cd ~/tess; dpkg -i leptonica_1.71-1_amd64.deb")
    sudo("cd ~/tess; dpkg -i tesseract-ocr_3.02.02-1_amd64.deb")
    sudo("cd ~/tess; dpkg -i tesseract-ocr-eng_3.02-2_all.deb")
    sudo("cd ~/tess; python setup.py install") 


def clean():
    run("cd work; rm -rf spider")



def killall():
    put("kill_worker.py", "~")
    run("python kill_worker.py spider")


