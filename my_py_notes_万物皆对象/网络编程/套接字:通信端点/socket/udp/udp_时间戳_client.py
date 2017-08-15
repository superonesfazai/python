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

# 客户端无需绑定地址信息, 操作系统会随机分配一个端口号供通讯使用
host = '127.0.0.1'
port = 8082
buf_size = 1024
ser_addr = (host, port)

udp_cli_sock = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        data = input('请输入要发送的内容> ')
        # if not data:
        #     print('不能发送空消息')
        #     break
        # sendto(要发送的数据bytes类型, 接收方地址信息ip和端口(是一个元组))
        udp_cli_sock.sendto(data.encode(), ser_addr)
        #接收服务器(传回来的)数据
        recv_data, addr = udp_cli_sock.recvfrom(buf_size)
        # if not data:
        #     print('无有效信息')
        #     break
        print('接收到来自服务端的回显:', recv_data.decode())
        # udp_cli_sock.close()
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    udp_cli_sock.close()