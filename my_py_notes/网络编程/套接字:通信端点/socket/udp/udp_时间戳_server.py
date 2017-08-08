# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午3:16
# @File    : udp_时间戳_server.py

from socket import *
from time import ctime

# 由于udp服务器不是面向连接的,所以不用像tcp服务器那样那么多的设置工作
# 事实上不需要设置什么东西,直接等待进来的连接就好了
# udp和tcp一个重要的区别是,由于数据报套接字是无连接的,所以无法把客户端连接交给另外套接字进行后续的通讯
# 这些服务器只是接收消息,需要的话,给客户端返回一个结果就可以了

# ss = socket()       # 创建一个服务器套接字
# ss.bind()           # 绑定服务器套接字
# inf_loop:           # 服务器无线循环
#     cs = ss.recvfrom()/ss.sendto()  # 对话(接收与发送)
# ss.close()          # 关闭服务器套接字

host = ''
port = 21567
buf_size = 1024
addr = (host, port)

udp_ser_sock = socket(AF_INET, SOCK_DGRAM)
udp_ser_sock.bind(addr)

try:
    while True:
        print('waiting for message...')
        data, addr = udp_ser_sock.recvfrom(buf_size)
        udp_ser_sock.sendto('[%s] %s' %
                                (ctime(), data), addr)
        print('...received from and returned to:', addr)
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    udp_ser_sock.close()

