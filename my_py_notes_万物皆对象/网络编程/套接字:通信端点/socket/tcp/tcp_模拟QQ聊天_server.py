# coding = utf-8

'''
@author = super_fazai
@File    : tcp_模拟QQ聊天_server.py
@Time    : 2017/8/11 11:48
@connect : superonesfazai@gmail.com
'''

import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 创建socket
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 设置socket可以重用地址

address = ('', 8000)    # 绑定本地信息
server_sock.bind(address)

server_sock.listen(128)     # 开启监听

while True:
    client_sock, client_addr = server_sock.accept()     # 接收客户端的连接请求
    print("与客户端%s:%s建立了连接" % (client_addr, client_addr))

    while True:
        recv_data = client_sock.recv(1024)
        if len(recv_data) > 0:                  # 如果接收的数据的长度为0，则意味着客户端关闭了链接
            print("客户端说:%s" % recv_data.decode())
            msg = input("请输入回复的内容：")      # 发送一些数据到客户端
            client_sock.send(msg.encode())
        else:
            break

    print("客户端%s:%s已下线" % (client_addr, client_addr))
    client_sock.close()     # 关闭客户端socket

server_sock.close()     # 关闭服务器socket
