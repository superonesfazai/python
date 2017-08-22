# coding = utf-8

'''
@author = super_fazai
@File    : 3_使用类.py
@Time    : 2017/8/20 17:20
@connect : superonesfazai@gmail.com
'''

import socket
import sys
from multiprocessing import Process
import re

serv_addr = (HOST, PORT) = ('', 7788)
document_root = './html'


class WSGIServer(object):
    addr_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 10

    def __init__(self, serv_addr):
        self.listen_socket = socket.socket(self.addr_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(serv_addr)
        self.listen_socket.listen(self.request_queue_size)
        self.error = None   # 用于记录抛出的异常值

    def serv_forever(self):
        self.cli_socket, self.cli_addr = self.listen_socket.accept()
        new_cli_process = Process(target=self.handle_request)
        new_cli_process.start()
        self.cli_socket.close()

    def handle_request(self):
        recv_data = self.cli_socket.recv(2017)
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

        print('file name is ===2>{}'.format(get_file_name))

        try:
            f = open(get_file_name, 'rb')

        except IOError as e:
            self.error = e
            response_header_lines = 'HTTP/1.1 404 not found\r\n'
            response_header_lines += '\r\n'
            # response_body = '====sorry, file not found===='
            with open('./html/404.html', 'rb') as f:
                response_body = f.read()
        else:
            response_header_lines = 'HTTP/1.1 200 OK\r\n'
            response_header_lines += '\r\n'
            response_body = f.read()
            f.close()
        finally:
            response = response_header_lines + response_body.decode()
            self.cli_socket.send(response.encode())
            self.cli_socket.close()

def make_server(serv_addr):
    server = WSGIServer(serv_addr)
    return server

def main():
    httpd = make_server(serv_addr)
    print('web Server: Serving HTTP on port %d ...\n' % PORT)
    httpd.serv_forever()

if __name__ == '__main__':
    main()