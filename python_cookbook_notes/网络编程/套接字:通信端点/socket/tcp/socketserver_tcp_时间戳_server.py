# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午4:26
# @File    : socketserver_tcp_时间戳_server.py

from socketserver import (TCPServer as tcp, StreamRequestHandler as srh)
from time import ctime

host = ''
port = 21567
addr = (host, port)

class MyRequestHandler(srh):
    def handle(self):       # 重写方法
        print('...connected from:', self.client_address)
        self.wfile.write('[%s] %s' %
                            (ctime(), self.rfile.readline()))

tcp_serv = tcp(addr, MyRequestHandler)
print('waiting for connection...')
tcp_serv.serve_forever()

