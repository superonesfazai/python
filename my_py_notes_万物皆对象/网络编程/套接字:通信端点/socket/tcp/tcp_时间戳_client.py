# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午2:54
# @File    : tcp_时间戳_client.py

from socket import *

# # 创建TCP客户端的伪代码
# cs = socket()       # 创建客户端套接字
# cs.connect()        # 尝试连接服务器
# comm_loop           # 通信循环
#     cs.send()/cs.recv()     # 对话(发送与接收)
# cs.close()          # 关闭客户端套接字

host = '127.0.0.1'
port = 8081
buf_size = 1024
addr = (host, port)

tcp_cli_sock = socket(AF_INET, SOCK_STREAM)
tcp_cli_sock.connect(addr)      # 当connect执行完毕后, 表示已于服务器完成三次握手, 可以进行数据传输

try:
    while True:
        data = input('请输入传输数据> ')
        if not data:
            break
        tcp_cli_sock.send(data.encode())
        data = tcp_cli_sock.recv(buf_size)
        if not data:
            break
        print(data.decode())
except EOFError as e:
    print('EOFError')
except KeyError as ek:
    print('KeyError')
finally:
    tcp_cli_sock.close()

