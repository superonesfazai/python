# coding = utf-8

'''
@author = super_fazai
@File    : tcp_模拟QQ聊天_client.py
@Time    : 2017/8/11 11:49
@connect : superonesfazai@gmail.com
'''

import socket


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 创建socket

server_addr = ('127.0.0.1', 8000)       # 链接服务器
client_sock.connect(server_addr)

while True:
    msg = input("请输入要发送的消息：")       # 提示用户输入数据


    if len(msg) > 0:        # 若用户输入了内容，则发送，否则退出
        client_sock.send(msg.encode())
        recv_data = client_sock.recv(1024)      # 接收对方发送过来的数据，最大接收1024个字节
        print("收到的消息：%s" % recv_data.decode())
    else:
        break

client_sock.close()     # 关闭套接字