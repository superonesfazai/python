# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午3:33
# @File    : udp_时间戳_client.py

from socket import *

# # 创建一个udp客户端的伪代码如下
# cs = socket()       # 创建客户端套接字
# comm_loop:          # 通讯循环
#     cs.sendto()/cs.recvfrom()   # 对话(发送与接收)
# cs.close()          # 关闭客户端套接字

host = ' localhost '
port = 21567
buf_size = 1024
addr = (host, port)

udp_cli_sock = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        data = input('> ')
        if not data:
            break
        udp_cli_sock.sendto(data, addr)
        data, addr = udp_cli_sock.recvfrom(buf_size)
        if not data:
            break
        print(data.decode('utf-8'))
        udp_cli_sock.close()
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    udp_cli_sock.close()