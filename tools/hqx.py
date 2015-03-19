#!/usr/bin/python2
#-*-encoding=utf-8-*-
import tornado.httpserver   
import tornado.ioloop
import tornado.options
import tornado.web   
from tornado.options import define, options
import webbrowser
import pdb
import subprocess
import sys
import simple_http as hh

define("port", default=8080, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):   
    def get(self):
        self.write(open("index.html").read())

    def post(self):
        #pdb.set_trace()
        m = self.get_arguments("sfile")
        t = self.get_arguments("stype")
        e = self.get_arguments("sexpr")
        if not m or not t or not e:
                self.write("arguments not enough")
                return
        m = m[0]
        t = t[0]
        e = e[0]

        f = open("list.html", "w")
        h, rr = hh.get(m)
        if h["status"] != 200:
            self.write("err, bad response. %r" % h["status"])
            return
        f.write(rr)
        f.close()
        e=e.encode("utf-8")
        #pdb.set_trace()
        p = ""
        if t == "xpath":
                p = ","
        elif t == "text":
                p = "-"
        elif t == "line":
                p = ">"
        elif t == "attr":
                p = "."
        try:
            rt = subprocess.check_output(["./qxt", "list.html", p+e], stderr=sys.stderr)
        except:
            self.write("call failed.")
            return
        self.write(rt)

if __name__ == "__main__":
    tornado.options.parse_command_line()   
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])   
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    webbrowser.open_new('http://127.0.0.1:8080')
    tornado.ioloop.IOLoop.instance().start()
