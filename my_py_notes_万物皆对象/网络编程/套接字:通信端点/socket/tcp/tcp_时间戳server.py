# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午2:40
# @File    : tcp_时间戳server.py

from socket import *
from time import ctime

'''
TCP用三次握手过程创建一个连接。在连接创建过程中，很多参数要被初始化，例如序号被初始化以保证按序传输和连接的强壮性
'''

# # *服务器设置的伪代码
# ss = socket()       # 创建服务器的套接字
# ss.bind()           # 把地址绑定在套接字上
# ss.listen()         # 监听连接
# inf_loop:           # 服务器无线循环
#     cs = ss.accept()    # 接受客户端连接
# comm_loop:          # 通信循环
#     cs.recv()/cs.send()     # 对话(接收与发送)
# cs.close()          # 关闭客户端套接字
# ss.close()          # 关闭服务器套接字(可选)

host = ''
port = 21567
buf_size = 1024     # 设置缓存区为1k
addr = (host, port)

tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
tcp_ser_sock.bind(addr)
tcp_ser_sock.listen(5)

try:
    while True:
        print('waiting for connection...')
        tcp_cli_sock, addr = tcp_ser_sock.accept()
        print('...connected from:', addr)

        while True:
            data = tcp_cli_sock.recv(buf_size)
            if not data:
                break
            tcp_cli_sock.send('[%s] %s' % (ctime(), data))
            tcp_cli_sock.close()
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    tcp_ser_sock.close()
