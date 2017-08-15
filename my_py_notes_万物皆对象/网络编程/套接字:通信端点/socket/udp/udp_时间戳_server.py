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
port = 8082
buf_size = 1024
ser_addr = (host, port)

udp_ser_sock = socket(AF_INET, SOCK_DGRAM)  # AF_INET 用于internet进程间通讯, AF_UNIX 用于本机进程间通讯
                                            # socket.SOCK_DGRAM 指明传输层协议使用udp
udp_ser_sock.bind(ser_addr)

try:
    while True:
        print('waiting for message...')
        client_data, client_addr = udp_ser_sock.recvfrom(buf_size)    # recvfrom默认阻塞, 会等待直到客户端传输数据
                                                            # recv()方法只有一个返回值, 那就是接收到的数据, 但是没有地址
        # 通过decode()方法把bytes转换为str类型, 因为传输用的数据类型都是bytes
        print('...received from and returned to:', client_addr, 'info:', client_data.decode())
        # 切记sendto(要发送数据的bytes类型, 目标的ip和端口(一个元组))
        udp_ser_sock.sendto(('[%s] %s' % (ctime(), client_data.decode())).encode(), client_addr)
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    udp_ser_sock.close()

