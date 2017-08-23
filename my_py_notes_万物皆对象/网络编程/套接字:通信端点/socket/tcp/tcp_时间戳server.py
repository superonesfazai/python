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
#     c_socket, c_addr = ss.accept()    # 接受客户端连接
# comm_loop:          # 通信循环
#     cs.recv()/cs.send()     # 对话(接收与发送)
# cs.close()          # 关闭客户端套接字
# ss.close()          # 关闭服务器套接字(可选)

host = ''
port = 8081
buf_size = 1024     # 设置缓存区为1k
addr = (host, port)

tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
tcp_ser_sock.bind(addr)
tcp_ser_sock.listen(5)      # listen()的参数是指明监听队列的容器有多大
                            # 监听队列：保存跟每个客户端进行三次握手需要用到的数据
                            # 当队列已满, 新请求客户端发送的请求数据将被丢弃
                            # 当跟一个客户端的三次握手完成后, 会将客户端三次握手数据从监听队列中删除, 后面发起连接的客户端数据就能被放到监听队列里面

try:
    while True:
        print('waiting for connection...')
        # tcp_cli_sock是用来跟客户端一对一通讯用的socket对像
        # addr 接受了请求的客户端的地址信息(ip和端口)(元组类型)
        tcp_cli_sock, addr = tcp_ser_sock.accept()      # 没有客户端连接时, 就是阻塞状态
        print('...connected from:', addr)

        while True:
            data = tcp_cli_sock.recv(buf_size)
            if not data:
                break
            tcp_cli_sock.send(('[%s] %s' % (ctime(), data)).encode())
            # tcp_cli_sock.close()
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    tcp_ser_sock.close()

'''
服务器要维护每个与之通讯的客户端的用到的数据, 这些数据都保存在socket中
'''
