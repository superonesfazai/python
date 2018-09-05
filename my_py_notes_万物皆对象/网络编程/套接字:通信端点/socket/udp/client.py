# encoding: utf-8

import socket

port = 8081
host = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('hello,this is a 避免死锁.md info !'.encode(), (host, port))

'''
测试
服务端与客户端的程序我们都已完成，可以同时开启进行测试。
我们也可以用nc充当udf服务端来单独测试客户端程序。

# -l 表示作为服务端开启，进行监听listen
# -u 表示使用udp协议
# nc -lu 绑定的服务器ip地址 端口
nc -lu 127.0.0.1 8080
'''