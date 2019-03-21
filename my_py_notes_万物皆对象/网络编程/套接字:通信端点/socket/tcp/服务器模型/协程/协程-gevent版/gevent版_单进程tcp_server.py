# coding = utf-8

'''
@author = super_fazai
@File    : gevent版_单进程tcp_server.py
@Time    : 2017/8/18 12:42
@connect : superonesfazai@gmail.com
'''

import sys
import time
import gevent
from gevent import monkey
from socket import AF_INET, SOCK_STREAM

monkey.patch_all()  # 替换平常用到的函数

def handle_request(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            break
        print("recv:", data.decode())
        conn.send(data)

def main(port):
    # 注意是从gevent包中的socket类来创建对象
    s = gevent.socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8080))
    s.listen(5)
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli)

if __name__ == '__main__':
    main(7788)