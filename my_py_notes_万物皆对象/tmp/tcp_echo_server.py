# coding = utf-8

'''
@author = super_fazai
@File    : tcp_echo_server.py
@Time    : 2017/8/24 10:16
@connect : superonesfazai@gmail.com
'''

from threading import Thread
import socket

PORT = 7788
home = '127.0.0.1'
addr = (home, PORT)

def server():
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(addr)
    serv_socket.listen(10)

    while True:
        b = Thread(target=tmp_accept, args=(serv_socket,))
        b.start()
        b.join()


def tmp_accept(serv_socket):    # 生产者
    while True:
        cli_socket, cli_addr = serv_socket.accept()
        data = cli_socket.recv(1024)
        print('收到客户端%s 发来的数据:%s' % (cli_addr, data.decode()))
        c = Thread(target=tmp_send, args=(cli_socket, data))
        c.start()
        c.join()

def tmp_send(cli_socket, data):
    cli_socket.send(data)

if __name__ == '__main__':
    a = Thread(target=server)
    a.start()
    a.join()

'''
服务端的测试结果:
收到客户端('127.0.0.1', 55870) 发来的数据:aaaaaa

客户端的结果:
请输入传输数据> aaaaaa
收到服务端的回显数据: aaaaaa
'''