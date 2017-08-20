# coding = utf-8

'''
@author = super_fazai
@File    : 2_显示需要的页面.py
@Time    : 2017/8/20 16:35
@connect : superonesfazai@gmail.com
'''

import socket
from multiprocessing import Process
import re

# 这里配置服务器
document_root = './html'

def handle_request(cli_socket):
    recv_data = cli_socket.recv(2017)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print(line.decode())

    http_request_method_line = request_header_lines[0]
    get_file_name = re.compile('[^/]+(/[^ ]*)').findall(http_request_method_line.decode())[0]
    print('file name is ===>{}'.format(get_file_name))

    if get_file_name == '/':
        get_file_name = document_root + '/index.html'
    else:
        get_file_name = document_root + get_file_name
    print('file name is ===>2>{}'.format(get_file_name))

    try:
        f = open(get_file_name)
    except IOError:
        response_header_lines = 'HTTP/1.1 404 not found\\r\\n'
        response_header_lines += '\\r\\n'
        response_body = '====sorry, file not found===='
    else:
        response_header_lines = 'HTTP/1.1 200 OK\\r\\n'
        response_header_lines += '\\r\\n'
        response_body = f.read()
        f.close()
    finally:
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
        tmp_cli = Process(target=handle_request, args=(cli_socket,))
        tmp_cli.start()
        cli_socket.close()

if __name__ == '__main__':
    main()