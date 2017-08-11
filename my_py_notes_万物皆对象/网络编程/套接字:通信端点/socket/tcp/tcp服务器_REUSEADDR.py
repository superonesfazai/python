# coding = utf-8

'''
@author = super_fazai
@File    : tcp服务器_REUSEADDR.py
@Time    : 2017/8/11 11:46
@connect : superonesfazai@gmail.com
'''

'''
为了解决服务器socket可能的2MSL延迟问题，我们可以为服务器socket设置SO_REUSEADDR选项
'''

import socket

# 创建socket
# 注意TCP协议对应的为SOCK_STREAM 流式
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 使用setsockopt()方法设置socket的选项参数
# SOL_SOCKET = Set Option Level _ SOCKET 设置选项级别为socket级
# SO_REUSEADDR = Socket Option _ REUSEADDR 设置socket的选项参数为重用地址功能
# 1 表示开启此选项功能，即开启重用地址功能
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定IP地址和端口
address = ("", 8000)
server_sock.bind(address)

# 让服务端的socket开启监听，等待客户端的连接请求
server_sock.listen(128)

# 使用accept方法接收客户端的连接请求
client_sock, client_addr = server_sock.accept()
print("客户端%s:%s进行了连接!" % client_addr)

# recv()方法可以接收客户端发送过来的数据，指明最大收取1024个字节的数据
recv_data = client_sock.recv(1024)
print("接收到的数据为：", recv_data.decode())

# send()方法向客户端发送数据，要求发送bytes类型的数据
client_sock.send("thank you!\n".encode())

# 关闭与客户端连接的socket
client_sock.close()

# 关闭服务端的监听socket
server_sock.close()