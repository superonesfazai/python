# coding = utf-8

'''
@author = super_fazai
@File    : web_动态_server_demo2(传递数据给应用).py
@Time    : 2017/8/20 18:18
@connect : superonesfazai@gmail.com
'''
import socket
import sys
from multiprocessing import Process
import re

class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5

    def __init__(self, server_address):
        #创建一个tcp套接字
        self.listen_socket = socket.socket(self.address_family, self.socket_type)
        #允许重复使用上次的套接字绑定的port
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #绑定
        self.listen_socket.bind(server_address)
        #变为被动，并制定队列的长度
        self.listen_socket.listen(self.request_queue_size)

        self.servr_name = "localhost"
        self.server_port = server_address[1]

    def serve_forever(self):
        '循环运行web服务器，等待客户端的链接并为客户端服务'
        while True:
            #等待新客户端到来
            self.client_socket, client_address = self.listen_socket.accept()

            #方法2，多进程服务器，并发服务器于多个客户端
            new_client_process = Process(target = self.handle_request)
            new_client_process.start()

            #因为创建的新进程中，会对这个套接字+1，所以需要在主进程中减去依次，即调用一次close
            self.client_socket.close()

    def set_app(self, application):
        '设置此WSGI服务器调用的应用程序入口函数'
        self.application = application

    def handle_request(self):
        '用一个新的进程，为一个客户端进行服务'
        self.recv_data = self.client_socket.recv(2014)
        request_header_lines = self.recv_data.splitlines()
        for line in request_header_lines:
            print(line.decode())

        http_request_method_line = request_header_lines[0]
        get_file_name = re.match("[^/]+(/[^ ]*)", http_request_method_line.decode()).group(1)
        print("file name is ===>%s"%get_file_name) #for test

        if get_file_name[-3:] != ".py":

            if get_file_name == '/':
                get_file_name = document_root + "/index.html"
            else:
                get_file_name = document_root + get_file_name

            print("file name is ===2>%s"%get_file_name) #for test

            try:
                f = open(get_file_name)
            except IOError:
                response_header_lines = r"HTTP/1.1 404 not found\r\n"
                response_header_lines += r"\r\n"
                response_body = "====sorry ,file not found===="
            else:
                response_header_lines = r"HTTP/1.1 200 OK\r\n"
                response_header_lines += r"\r\n"
                response_body = f.read()
                f.close()
            finally:
                response = response_header_lines + response_body
                self.client_socket.send(response.encode())
                self.client_socket.close()
        else:
            #处理接收到的请求头
            self.parse_request()

            #根据接收到的请求头构造环境变量字典
            env = self.get_environ()

            #调用应用的相应方法，完成动态数据的获取
            body_content = self.application(env, self.start_response)

            #组织数据发送给客户端
            self.finish_response(body_content)

    def parse_request(self):
        '提取出客户端发送的request'
        request_line = self.recv_data.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        self.request_method, self.path, self.request_version = request_line.split(" ")

    def get_environ(self):
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.input']        = self.recv_data
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path             # /index.html
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', 'Tue, 31 Mar 2016 10:11:12 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, body_content):
        try:
            status, response_headers = self.headers_set
            #response的第一行
            response = r'HTTP/1.1 {status}\r\n'.format(status=status)
            #response的其他头信息
            for header in response_headers:
                response += r'{0}: {1}\r\n'.format(*header)
            #添加一个换行，用来和body进行分开
            response += r'\r\n'
            #添加发送的数据
            for data in body_content:
                response += data

            self.client_socket.send(response.encode())
        finally:
            self.client_socket.close()

#设定服务器的端口
server_addr = (HOST, PORT) = '', 8888
#设置服务器静态资源的路径
document_root = './html'
#设置服务器动态资源的路径
python_root = './wsgiPy'

def make_server(server_addr, application):
    server = WSGIServer(server_addr)
    server.set_app(application)
    return server

def main():

    if len(sys.argv) < 2:
        sys.exit('请按照要求，指定模块名称:应用名称,例如 module:callable')

    #获取module:callable
    app_path = sys.argv[1]
    #根据冒号切割为module和callable
    module, application = app_path.split(':')
    #添加路径套sys.path
    sys.path.insert(0, python_root)
    #动态导入module变量中指定的模块
    module = __import__(module)
    #获取module变量中制定的模块的application变量指定的属性
    application = getattr(module, application)
    httpd = make_server(server_addr, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()

if __name__ == '__main__':
    main()
