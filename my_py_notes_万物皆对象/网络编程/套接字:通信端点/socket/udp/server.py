# encoding: utf-8

import socket

port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # 1. 创建套接字
# 从指定的端口，从任何发送者，接收UDP数据
s.bind(('', port))
print('正在等待接入...')
while True:
    # recv方法接收发送过来的数据
    # 返回值为接收到的数据，参数（这里为1024）表示本次收取数据的最大字节数
    # receive_data = server_sock.recv(1024)
    # recvfrom与recv方法类似，不同的是可以将发送数据的客户端的地址也返回
    # 接收一个数据
    data, address = s.recvfrom(1024)
    print('Received:', data, 'from', address)

'''
测试
如果, 暂时还没有写udp客户端, 可以用nc命令来作为客户端进行测试。
# -u 表示使用udp协议
# nc -u 服务器ip 服务器端口
nc -u 127.0.0.1 8080
'''