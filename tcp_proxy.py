#-*-encoding=utf-8-*-
import socket
from select import *
from cStringIO import StringIO
import pdb
import errno
import os
import time
import re

#client: allow ip
#listen: listen address
#server: forward to server

roles = {
        "test":{
            "client": {
                "src": "127.0.0.1", 
                "listen": "127.0.0.1:9000",
                "server": "127.0.0.1:9001"
                },
            "server": {
                'src': "127.0.0.1",
                'listen': "127.0.0.1:9001",
                'server': "127.0.0.1:6379" 
                },
            }, 
        "promo":{
            "client": {
                "src": "127.0.0.1",
                "listen": "0.0.0.0:9000",
                "server": "118.144.88.212:8731"
                },
            "server": {
                'src': "(115.159.50.207|115.159.81.185|115.159.55.245|115.159.52.83|115.159.44.122|115.159.147.205|115.159.58.230|115.159.3.168|115.159.4.30|115.159.81.90|115.159.147.245|115.159.147.245|182.254.147.205|182.254.147.245)",
                'listen': "118.144.88.212:8731",
                'server': "192.168.1.191:6379" 
                },
            },
        "offshelf":{
            "client": {
                "src": "127.0.0.1",
                "listen": "0.0.0.0:6380",
                "server": "118.144.88.212:8732"
                },
            "server": {
                'src': "(115.159.50.207|115.159.81.185|115.159.55.245|115.159.52.83|115.159.44.122|115.159.147.205|115.159.58.230|115.159.3.168|115.159.4.30|115.159.81.90|115.159.147.245|115.159.147.245|182.254.147.205|182.254.147.245)",
                'listen': "118.144.88.212:8732",
                'server': "192.168.1.193:6380" 
                }, 
            }
        }


##########################
#dont' modify
##########################

profile = None

STATUS_CONNECT = 0x1 << 1
STATUS_DATA = 0x1 << 2 

FD_CON = {} 

SERVER_FD = -1
SERVER_CON = None
EP = None
MY_SERVER = None


MODE_CLIENT = 0
MODE_SERVER = 1

mode = MODE_CLIENT

CONVERT_ENCODE = 0x1 << 1
CONVERT_DECODE = 0x1 << 2
CONVERT_NONE = 0x1 << 3

EAGAIN = errno.EAGAIN

#random ascii table
DS = '\x1f\xf6\xb4P\x01\xbcAz)\xae\xd8$=u\xf16\x08\xde\x14R\x04y\xb0\xcc\xf4\xfa\xfck\xfd\xa1\xfe\xb5_\x87\xa3\xa58G]^\x84\xa9\x12\xaf\x19\xd7\xe62\x94\xc5\xa4\xcbK\x8eD\xb8\x07\xb1\xcd\x15Ta\x91\x9b\xeb\x0b\xf7\xff*\x02\x06C\x8a\x0e\x90B\x85\x95/\x8c\xb9\xd6[!.\x9a4Q\x7f\x92\x0f\xa2\xad\xda\x1b\xce\x03\x1cIYJ\xc1\xdb\xe3\x82\xbaH\xe0V\xc7S\xbe\xe4g\xe5\xe7\x9e\xec7Uit\xa6\xbd\xbf\xf2\xf3\x96&\x86\x89\x9f\xfb:c(O?N\x10}~\x88\xa7\xb6\xc3\xdd\xf0\xf5\xf8\x8f<qE#n@\x05\x97\\\x00jX\x80\xbbZ\xc8\xcf\xd3\xd5\x17{\'w\xcab0lpW\x93\x11\xc2\x9c\xb23\x83\x1a\xb3\x16 `oh\x81\x1e\x8b\xb7"\xc4d\x0c+>\xab\xd2\xd9F\xd4\xe8\r\x189\xa0f\n\tv-\x1d\xa8\xaa%\xc6;\xd1\xdf\x98\xe1\xc0\xe9\xed\xac1r\x8d,5|Ms\xc9\x99\x13m\x9d\xe2L\xea\xee\xd0x\xdce\xef\xf9'

SD = '\xa0\x04E`\x14\x9dF8\x10\xd8\xd7A\xc9\xd2IZ\x8b\xb5*\xf3\x12;\xbd\xaa\xd3,\xbb^a\xdb\xc3\x00\xbeS\xc6\x9a\x0b\xde\x80\xac\x87\x08D\xca\xec\xdaTN\xb0\xe9/\xb9V\xed\x0fv$\xd4\x85\xe0\x97\x0c\xcb\x89\x9c\x06KG6\x99\xcf%jbd4\xf7\xef\x8a\x88\x03W\x13n<wl\xb3\xa2c\xa5R\x9f&\' \xbf=\xaf\x86\xc8\xfd\xd6q\xc1x\xa1\x1b\xb1\xf4\x9b\xc0\xb2\x98\xea\xf0y\r\xd9\xad\xfb\x15\x07\xab\xee\x8c\x8dX\xa3\xc2h\xba(L\x81!\x8e\x82H\xc4O\xeb5\x96J>Y\xb40M\x7f\x9e\xe3\xf2U?\xb7\xf5t\x83\xd5\x1d["2#z\x8f\xdc)\xdd\xcc\xe8\\\t+\x169\xb8\xbc\x02\x1f\x90\xc57Pi\xa4\x05{o|\xe5e\xb6\x91\xc71\xdfm\xa6\xf1\xae3\x17:_\xa7\xfa\xe1\xcd\xa8\xd0\xa9Q-\n\xce]f\xfc\x92\x11\xe2k\xe4\xf6gpr.s\xd1\xe6\xf8@u\xe7\xf9\xfe\x93\x0e}~\x18\x94\x01B\x95\xff\x19\x84\x1a\x1c\x1eC'


def log_with_time(msg):
    print time.ctime() + repr(msg)


def handle_event(): 
    for fd, event in EP.poll(2): 
        if fd == SERVER_FD:
            if event & EPOLLIN:
                accept_con()
            else:
                log_with_time("server died")
                exit(1)
            return
        con = FD_CON.get(fd)
        if not con:
            try:
                EP.unregister(fd)
            except:
                pass
            continue 
        if event & EPOLLERR: 
            die_con(con)
            continue 
        if event & EPOLLOUT: 
            event_write(con)
        if event & EPOLLIN: 
            event_read(con) 


def clear_con(con): 
    sock = con["from"]
    fd = con["fd"]
    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except (socket.error, IOError, ValueError):
        pass
    con["send"].close()
    con["recv"].close() 
    if fd in FD_CON:
        del FD_CON[fd] 



def die_con(con):
    clear_con(con)
    to_conn = FD_CON.get(con["to"])
    if to_conn:
        clear_con(to_conn) 


def send_remain(con): 
    to_conn = FD_CON.get(con["to"])
    conn = con["from"]
    send = con["send"] 
    if not send.tell():
        remove_pollout(con)
        return
    data = send.getvalue() 
    data_count = len(data)
    try:
        data_sent = conn.send(data)
    except socket.error as e:
        if e.errno != EAGAIN:
            die_con(con)
        return
    send.truncate(0)
    if data_sent != data_count:
        send.write(data[data_sent:]) 
        add_pollout(con)
        if data_count - data_sent > 102400:
            remote_pollin(to_conn)
    else:
        remove_pollout(con) 
    if send.tell() < 102400: 
        add_pollin(to_conn)

    

def add_pollin(con):
    fd = con["from"].fileno()
    EP.modify(fd, EPOLLIN | EPOLLOUT | EPOLLERR)


def add_pollout(con):
    fd = con["from"].fileno()
    EP.modify(fd, EPOLLIN | EPOLLOUT | EPOLLERR) 


def remove_pollout(con):
    fd = con["from"].fileno()
    EP.modify(fd, EPOLLIN | EPOLLERR) 


def remote_pollin(con): 
    fd = con["from"].fileno()
    EP.modify(fd, EPOLLOUT | EPOLLERR) 



def event_write(con):
    status = con["status"] 
    if status & STATUS_CONNECT: 
        con["status"] = STATUS_DATA 
    send_remain(con)



def event_read(con): 
    remote = FD_CON.get(con["to"])
    if not remote: 
        die_con(con) 
        return
    buf = remote["send"]
    conn = con["from"]
    convert = con["convert"]
    while True:
        mark = buf.tell() 
        try: 
            data = conn.recv(40960) 
        except socket.error as e:
            if e.errno != EAGAIN:
                die_con(con)
                return
            break 
        if convert & CONVERT_ENCODE:
            data = data.translate(SD)
        elif convert & CONVERT_DECODE:
            data = data.translate(DS)
        buf.write(data) 
        if buf.tell() == mark:
            die_con(con)
            return
    if buf.tell():
        add_pollout(remote)


def new_con(sock, fd=-1): 
    return { 
            "send": StringIO(),
            "recv": StringIO(),
            "from": sock, 
            "fd": sock.fileno(),
            "to": fd,
            "status": STATUS_CONNECT, 
            }



def connect_remote(con):
    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.setblocking(0)
        rfd = remote.fileno()
        EP.register(rfd, EPOLLIN|EPOLLOUT|EPOLLERR)
    except Exception as e: 
        if e.errno != errno.EMFILE: 
            remote_task(task, why="create socket: %s" % e)
        return 
    fd = con["from"].fileno()
    remote_con = new_con(remote, fd)
    FD_CON[rfd] = remote_con
    con["to"] = rfd
    remote_con["status"] = STATUS_CONNECT
    if mode == MODE_CLIENT:
        remote_con["convert"] = CONVERT_DECODE
    else:
        remote_con["convert"] = CONVERT_ENCODE 
    try:
        remote.connect(MY_SERVER)
    except socket.error as e:
        if e.errno != errno.EINPROGRESS:
            die_con(con) 


def accept_con(): 
    conn, addr = SERVER_CON.accept() 
    #检查来源
    if not re.match(profile["src"], addr[0]) and not addr[0] == "127.0.0.1":
        log_with_time("unexpected client: %s:%d" % addr)
        conn.close()
        return
    log_with_time("new client: %s:%d" % addr)
    fd = conn.fileno()
    conn.setblocking(0)
    flag = EPOLLIN | EPOLLERR
    EP.register(fd, flag)
    con = new_con(conn) 
    con["status"] = STATUS_DATA
    FD_CON[fd] = con
    connect_remote(con) 
    if mode == MODE_CLIENT:
        con["convert"] = CONVERT_ENCODE
    else:
        con["convert"] = CONVERT_DECODE 


def apply_config(): 
    global EP, SERVER_FD, SERVER_CON, MY_SERVER
    ip, port = profile["server"].split(":")
    MY_SERVER = ((ip, int(port)))
    SERVER_CON = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    SERVER_CON.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    ip, port = profile["listen"].split(":")
    SERVER_CON.bind((ip, int(port)))
    SERVER_CON.listen(1024)
    SERVER_FD = SERVER_CON.fileno()
    EP = epoll()
    EP.register(SERVER_FD, EPOLLIN | EPOLLERR) 



def run(): 
    apply_config()
    while True:
        handle_event() 


def daemonize(func, log): 
    log_file = open(log, "a+", buffering=0)
    if not os.fork(): 
        infile = open("/dev/null")
        os.dup2(infile.fileno(), 0)
        os.dup2(log_file.fileno(), 1)
        os.dup2(log_file.fileno(), 2)
        if not os.fork():
            sys.stdin = open("/dev/null", "r") 
            sys.stderr = log_file
            sys.stdout = log_file 
            func()
        exit()
    else: 
        os.wait()
        exit() 



if __name__ == "__main__": 
    import sys 
    assert sys.argv[1] in roles
    assert sys.argv[2] in ("client", "server")

    role = roles[sys.argv[1]]
    type = sys.argv[2]

    if type == "client":
        mode = MODE_CLIENT 
        profile = role["client"]
    else:
        mode = MODE_SERVER 
        profile = role["server"] 
    daemonize(run, "/tmp/tunnel-%s-%s.log" % (sys.argv[1], sys.argv[2]))
