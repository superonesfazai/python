# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午4:36
# @File    : socketserver_tcp_时间戳_client.py

from socket import *

host = ' localhost '
port = 21567
buf_size = 1024
addr = (host, port)

while True:
    tcp_cli_sock = socket(AF_INET, SOCK_STREAM)
    tcp_cli_sock.connect(addr)
    data = input('> ')
    if not data:
        break
    tcp_cli_sock.send('%s\r\n' % data)
    data = tcp_cli_sock.recv(buf_size)
    if not data:
        break
    print(data.strip())
    tcp_cli_sock.close()