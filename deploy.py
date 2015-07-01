from fabric.api import *
import os
import re
import json
import pprint
import pdb
import socket

UDP_PORT = 9966


env.hosts = [ 
        "spider@192.168.1.191:22",
        "spider@192.168.1.192:22",
        "spider@192.168.1.193:22",
        "spider@192.168.1.194:22", 
        ] 


env.passwords = {
        "spider@192.168.1.191:22": "spider#@!",
        "spider@192.168.1.192:22": "spider#@!", 
        "spider@192.168.1.193:22": "spider#@!", 
        "spider@192.168.1.194:22": "spider#@!", 
        } 



def upload(): 
    with settings(warn_only=True):
        run("mkdir ~/work") 
    os.system("find spider | grep .*pyc. |xargs rm") 
    os.system("find spider | grep .*sw. |xargs rm") 
    os.system("tar -cjf spider.tar.bz2 spider") 
    put("spider.tar.bz2", "~/work/")
    run("cd work; rm -rf spider; tar -mxvf spider.tar.bz2")



def install_deps():
    _ = lambda x : sudo("apt-get -q -y install %s" % x) 
    _("pkg-config")
    _("python-dev")
    _("python-lxml")
    _("python-pip")
    _("python-mysqldb") 
    _("libpng12-dev")
    _("make cmake") 
    _("aria2")
    _("software-properties-common python-software-properties")
    _("autoconf") 
    _ = lambda x : sudo("apt-get -q -y remove %s" % x) 
    _("tesseract-ocr") 
    _("tesseract-ocr-eng")
    _("libleptonica")
    _("libleptonica-dev")
    _("libtesseract3")
    _("libtesseract-dev") 
    __ = lambda x: sudo("pip install %s" %x)
    __("redis")
    __("hiredis")
    __("msgpack-python") 


def run_all():
    run("cd work; python spider all") 


def single_command(command, site=None, worker=False, response=False): 
    packet = {
            "id": 1235,
            "cmd": command,
            } 
    if site:
        packet["site"] = site
    if worker:
        packet["worker"] = worker
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind(("0.0.0.0", 9967)) 
    s.sendto(json.dumps(packet), (env.host, UDP_PORT)) 
    if response:
        p, addr = s.recvfrom(40960) 
        s.close()
        return json.loads(p)
    else:
        s.close() 


def start_all(): 
    single_command("startall")


def stop_all(): 
    single_command("stopall") 


def kill_all(): 
    with settings(warn_only=True): 
        run("cd ~/work; python spider/kill_worker.py spider") 


def stat(site, worker): 
    resp = single_command("stat", site, worker, response=True)
    print "host", env.host
    pprint.pprint(resp)


def stop(site, worker): 
    single_command("stop", site, worker) 


def start(site, worker):
    single_command("start", site, worker) 


def get_all(): 
    resp = single_command("getall", response=True)
    print "host", env.host
    pprint.pprint(resp)


def refresh():
    resp = single_command("refresh", response=True)
    print "host", env.host
    pprint.pprint(resp) 


def setup():
    with settings(warn_only=True):
        run("cd ~; rm -rf spider")
        run("cd ~; mkdir work") 

