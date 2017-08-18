# coding = utf-8

'''
@author = super_fazai
@File    : send也会发生阻塞.py
@Time    : 2017/8/18 11:11
@connect : superonesfazai@gmail.com
'''

import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('127.0.0.1', 8080)

client_sock.connect(server_addr)
client_sock.setblocking(False)  # 将发送数据的socket设置为非阻塞

while True:
    try:
        client_sock.send(b'aaaaaaaaaa')
    except BlockingIOError as e:
        # 表示此次发送收到阻止, 不能立即发送出去, 相当于阻塞方式使用时的阻塞等待
        print("数据没有立即发送出去")