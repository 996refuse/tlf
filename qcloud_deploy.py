from fabric.api import *
import os
import re
import json
import pprint
import pdb
import socket

UDP_PORT = 9966

HOST_PREFIX = "qcloud"

env.hosts = [ 
        "spider@10.105.59.79:22",
        "spider@10.105.18.152:22",
        "spider@10.105.32.144:22",
        "spider@10.105.32.238:22",
        "spider@10.105.32.109:22",
        "spider@10.131.174.91:22",
        "spider@10.105.32.88:22",
        "spider@10.131.224.162:22",
        "spider@10.131.222.225:22",
        "spider@10.105.32.229:22",
        "spider@10.131.155.1:22" 
        ] 


env.passwords = {
        "spider@10.105.59.79:22": "spider#@!", 
        "spider@10.105.18.152:22": "spider#@!", 
        "spider@10.105.32.144:22": "spider#@!", 
        "spider@10.105.32.238:22": "spider#@!", 
        "spider@10.105.32.109:22": "spider#@!", 
        "spider@10.131.174.91:22": "spider#@!", 
        "spider@10.105.32.88:22": "spider#@!", 
        "spider@10.131.224.162:22": "spider#@!", 
        "spider@10.131.222.225:22": "spider#@!", 
        "spider@10.105.32.229:22": "spider#@!", 
        "spider@10.131.155.1:22": "spider#@!", 
        } 


def upload(): 
    with settings(warn_only=True):
        run("mkdir ~/work") 
    os.system("find spider | grep .*pyc. |xargs rm") 
    os.system("find spider | grep .*sw. |xargs rm") 
    os.system("tar -cjf spider.tar.bz2 spider") 
    put("spider.tar.bz2", "~/work/")
    run("cd work; rm -rf spider; tar -mxvf spider.tar.bz2")


def set_hosts():
    l3, l4 = re.findall("([0-9]+)\.([0-9]+)$", env.host)[0]
    hostname = "%s-%s-%s" %  (HOST_PREFIX, l3, l4)
    sudo("echo '\n127.0.0.1 localhost %s\n' > /etc/hosts" % hostname)
    sudo("echo %s > /etc/hostname" % hostname)  
    sudo("hostname %s" % hostname) 


def install_tess():
    sudo("add-apt-repository -y ppa:ubuntu-toolchain-r/test")
    sudo("apt-get update")
    sudo("apt-get install -y g++-4.9") 
    put("tess", "~/")
    sudo("cd ~/tess; dpkg -i leptonica_1.71-1_amd64.deb")
    sudo("cd ~/tess; dpkg -i tesseract-ocr_3.02.02-1_amd64.deb")
    sudo("cd ~/tess; dpkg -i tesseract-ocr-eng_3.02-2_all.deb")
    sudo("cd ~/tess; python setup.py install") 


def install_deps():
    sudo("apt-get update")
    _ = lambda x : sudo("apt-get -q -y install %s" % x) 
    _("p7zip-full")
    _("pkg-config")
    _("python-dev")
    _("python-lxml")
    _("python-pip")
    _("python-mysqldb") 
    _("libpng12-dev")
    _("make cmake") 
    _("software-properties-common python-software-properties")
    _("autoconf") 
    _ = lambda x : sudo("apt-get -q -y remove %s" % x) 
    _("tesseract-ocr") 
    _("liblept4")
    _("libleptonica-dev")
    _("libtesseract3")
    _("libtesseract-dev") 
    __ = lambda x: sudo("pip install %s" %x)
    __("redis")
    __("hiredis")
    __("msgpack-python") 



def start_tcp_proxy():
    run("cd work; python spider/tcp_proxy.py promo client", pty=False) 
    run("cd work; python spider/tcp_proxy.py offshelf client", pty=False)

def stop_tcp_proxy():
    run("cd work; python spider/kill_worker.py tcp_proxy")



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



def setup():
    with settings(warn_only=True):
        run("cd ~; rm -rf spider")
        run("cd ~; mkdir work") 

