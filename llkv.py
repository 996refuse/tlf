import socket 
import pdb 

from struct import pack 
from struct import unpack
from struct import calcsize


class Connection: 
    TYPE_PING = 0
    TYPE_PONG = 1
    TYPE_GET = 2
    TYPE_GET_BULK = 3
    TYPE_SET = 4
    TYPE_SET_BULK = 5
    TYPE_DELETE = 6
    TYPE_DELETE_BULK = 7
    TYPE_RELOAD = 8
    TYPE_DUMP = 9 
    TYPE_UNKNOWN = 10
    TYPE_KILLALL = 11
    TYPE_HLEN = 12
    TYPE_FLUSH = 13
    TYPE_PKT_MAX = 14 
    NULL = 0xffffffffffffffff 
    hdr_fmt = "II"
    hdr_size = calcsize("II") 
    def __init__(self, host = "127.0.0.1", port = 8000): 
        self.host = host 
        self.port = port 
        if not isinstance(host, (str, unicode)):
            raise ValueError("invalid host")
        if not isinstance(port, int):
            raise ValueError("invalid port")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.connect((host, port)) 
        self.ping() 


    def send_command(self, b): 
        self.sock.send(b)


    def ping(self):
        self.send_command(pack("I", self.TYPE_PING))
        b = self.sock.recv(self.hdr_size)
        tp, code = unpack("II", b)
        if not b:
            raise socket.error("connection closed") 
        if tp != self.TYPE_PONG or code != 0:
            raise ValueError("invalid response: get") 


    def get(self, key):
        fmt = "Q"
        fmt_size = calcsize(fmt)
        total_fmt = self.hdr_fmt+ fmt
        total_size = calcsize(total_fmt) 
        self.send_command(pack(total_fmt,
            self.TYPE_GET, fmt_size, key))
        b = self.get_size_n_from_sock(total_size)
        tp, code, value= unpack(total_fmt, b)
        if not b:
            raise socket.error("connection closed") 
        if tp != self.TYPE_GET or code != 0:
            raise ValueError("invalid response: get")
        if value == self.NULL:
            return None
        return value 

    def multi_get(self, keys):
        fmt = "Q" * len(keys)
        fmt_size = calcsize(fmt)
        total_fmt = self.hdr_fmt+ fmt
        total_size = calcsize(total_fmt)

        self.send_command(pack(total_fmt,
            self.TYPE_GET_BULK, fmt_size, *keys)) 

        b = self.get_size_n_from_sock(total_size) 
        result = unpack(total_fmt, b) 
        if len(result) - len(keys) != 2:
            raise ValueError("invalid response: multi_get") 

        if result[0] != self.TYPE_GET_BULK or result[1] != 0: 
            raise ValueError("invalid response: multi_get") 

        ret = dict(zip(keys, result[2:]))
        for k, v in ret.items():
            if v == self.NULL:
                ret[k] = None 
        return ret 

    def get_size_n_from_sock(self, n):
        b = []
        i = 0
        while True:
            x = self.sock.recv(n) 
            if not x:
                raise ValueError("remote closed")
            b.append(x)
            i += len(x)
            if i >= n:
                break 
        return "".join(b) 


    def set(self, key, value):
        fmt = "QQ"
        fmt_size = calcsize(fmt) 
        self.send_command(pack(self.hdr_fmt + fmt,
            self.TYPE_SET, fmt_size, key, value)) 
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_SET or code != 0: 
            raise ValueError("invalid response: set") 


    def multi_set(self, d):
        fmt = "Q" * 2 * len(d)
        fmt_size = calcsize(fmt)
        total_fmt = self.hdr_fmt+ fmt
        total_size = calcsize(total_fmt) 
        q = []
        for item in d.items():
            q.append(item[0])
            q.append(item[1]) 
        self.send_command(pack(total_fmt, 
            self.TYPE_SET_BULK, fmt_size, *q))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_SET_BULK or code != 0: 
            raise ValueError("invalid response: set") 


    def delete(self, key):
        fmt = "Q"
        fmt_size = calcsize(fmt)
        total_fmt = self.hdr_fmt+ fmt
        total_size = calcsize(total_fmt) 
        self.send_command(pack(total_fmt,
            self.TYPE_DELETE, fmt_size, key))
        b = self.get_size_n_from_sock(total_size)
        tp, code = unpack(self.hdr_fmt, b)
        if not b:
            raise socket.error("connection closed") 
        if tp != self.TYPE_DELETE or code != 0:
            raise ValueError("invalid response: delete")


    def multi_delete(self,  keys): 
        fmt = "Q" * len(keys)
        fmt_size = calcsize(fmt)
        total_fmt = self.hdr_fmt+ fmt
        total_size = calcsize(total_fmt) 
        self.send_command(pack(total_fmt, 
            self.TYPE_DELETE_BULK, fmt_size, *keys))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_DELETE_BULK or code != 0: 
            raise ValueError("invalid response: multi_delete") 

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR) 


    def reload(self):
        self.send_command(pack("II", self.TYPE_RELOAD, 0))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_RELOAD or code != 0: 
            raise ValueError("invalid response: reload") 


    def hlen(self): 
        self.send_command(pack("II", self.TYPE_HLEN, 0))
        b = self.get_size_n_from_sock(self.hdr_size+8) 
        tp, code, value= unpack("IIQ", b) 
        if not b:
            raise socket.error("connection closed") 
        if tp != self.TYPE_HLEN or code != 0:
            raise ValueError("invalid response: hlen")
        if value == self.NULL:
            return None
        return value 


    def dump(self):
        self.send_command(pack("II", self.TYPE_DUMP, 0))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_DUMP or code != 0: 
            raise ValueError("invalid response: dump") 


    def killall(self):
        self.send_command(pack("II", self.TYPE_KILLALL, 0))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_KILLALL or code != 0: 
            raise ValueError("invalid response: killall") 

    def flush(self):
        self.send_command(pack("II", self.TYPE_FLUSH, 0))
        b = self.get_size_n_from_sock(self.hdr_size)
        if not b:
            raise socket.error("connection closed")
        tp, code = unpack(self.hdr_fmt, b) 
        if tp != self.TYPE_FLUSH or code != 0: 
            raise ValueError("invalid response: flush") 
