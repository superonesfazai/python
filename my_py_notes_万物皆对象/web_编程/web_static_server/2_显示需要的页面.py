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

# 这里配置服务器, 用户可以访问的html文件的目录
document_root = './html'

def handle_request(cli_socket):
    recv_data = cli_socket.recv(2017)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print(line.decode())

    http_request_method_line = request_header_lines[0]
    # 请求路径只要不是空格就匹配
    get_file_path = re.compile('[^/]+(/[^ ]*)').findall(http_request_method_line.decode())[0]
    print('file path is ===>{}'.format(get_file_path))

    if get_file_path == '/':
        get_file_path = document_root + '/index.html'   # 构建到index.html路径
    else:
        get_file_path = document_root + get_file_path   # 否则根据用户实际请求的路径进行构造路径
    print('file path is ===>2>{}'.format(get_file_path))

    try:
        f = open(get_file_path, 'rb')   # 用rb 因为有像图片一样的二进制数据
    except IOError:     # 表示没有成功打开, 则抛出一个IOError
        response_header_lines = 'HTTP/1.1 404 not found\r\n'
        response_header_lines += '\r\n'
        # response_body = '====sorry, file not found===='
        response_body = b'''
        <html>
            <head>
                <title>404 not found</title>
            </head>
            <body>
                <p>sorry, file not found!</p>
            </body>
        </html>
        '''
    else:
        response_header_lines = 'HTTP/1.1 200 OK\r\n'
        response_header_lines += '\r\n'
        response_body = f.read()
        f.close()
    finally:
        response = response_header_lines + response_body.decode()
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