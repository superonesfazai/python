# coding = utf-8

'''
@author = super_fazai
@File    : 简单的dns客户端.py
@Time    : 2017/8/11 10:53
@connect : superonesfazai@gmail.com
'''

import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ('127.0.0.1', 8053)
domain = input("请输入要查询的域名：")
while domain:
    # 向服务端发送要查询的域名
    client_sock.sendto(domain.encode("utf-8"), server_addr)
    # 接收服务端发送过来的ip信息
    ip = client_sock.recv(1024)
    print(ip.decode("utf-8"))
    domain = input("请输入要查询的域名：")

client_sock.close()