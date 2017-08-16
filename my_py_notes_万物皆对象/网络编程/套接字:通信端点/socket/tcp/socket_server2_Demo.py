#!/usr/bin/env python
# coding=utf-8

from socketserver import TCPServer, BaseRequestHandler
import traceback

class MyBaseRequestHandler(BaseRequestHandler):
    # 从BaseRequesyHandler继承，并重写handler方法
    def handle(self):

        while True:     # 循环监听(读取)来自客户端的数据
            try:        # 当客户端主动断开连接时，self.recv(1024)会抛出异常
                data = self.request.recv(1024).strip()      # 一次读取1024字节，并除去两端的空白字符(包括空格,Tab,\r,\n)
                print("receive from (%r):%r" % (self.client_address, data))     # self.client_address是客户端的连接(host, port)的元组
                self.request.sendall(data.upper() + '\n')   # 转换成大写后写回(发送到)客户端
            except:
                traceback.print_exc()
                break

if __name__ == '__main__':
    #telnet 127.0.0.1 9999
    host = ''  #主机名,可以是ip,像localhost的主机名,或""
    port = 8112  #端口
    addr = (host, port)

    server = TCPServer(addr, MyBaseRequestHandler) # 购置TVPServer对象

    #启动服务监听
    server.serve_forever()
