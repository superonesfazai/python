# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午7:24
# @File    : 简单的web服务器.py

from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):

def do_get(self):
    try:
        f = open(curdir + seq + self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
    except IOError:
        self.send_error(404, 'File not found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print('welcome to the machine...', end='')
        print('press ^C once or twice to quit.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socker.close()

if __name__ == '__main__':
    main()
