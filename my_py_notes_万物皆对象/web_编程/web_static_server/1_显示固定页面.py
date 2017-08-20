# coding = utf-8

'''
@author = super_fazai
@File    : 1_显示固定页面.py
@Time    : 2017/8/20 15:40
@connect : superonesfazai@gmail.com
'''

import socket
from multiprocessing import Process

def handle_cli(cli_socket):
    """
    用一个进程为一个客户端服务
    """
    recv_data = cli_socket.recv(2017)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print(line.decode())

    response_header_lines = r'HTTP/1.1 200 OK\r\n'
    response_header_lines += r'\r\n'
    response_body = 'hello, world!'

    response = response_header_lines + response_body
    cli_socket.send(response.encode())
    cli_socket.close()

def main():
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_socket.bind(('', 7788))
    serv_socket.listen(10)
    while True:
        cli_socket, cli_addr = serv_socket.accept()
        tmp_cli = Process(target=handle_cli, args=(cli_socket,))
        tmp_cli.start()
        cli_socket.close()

if __name__ == '__main__':
    main()