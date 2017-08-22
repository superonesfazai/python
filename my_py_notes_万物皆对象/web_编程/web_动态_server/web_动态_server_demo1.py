# coding = utf-8

'''
@author = super_fazai
@File    : web_动态_server_demo1.py
@Time    : 2017/8/20 18:04
@connect : superonesfazai@gmail.com
'''

import socket
import sys
from multiprocessing import Process
import re

server_addr = (HOST, PORT) = '', 7788
document_root = './html'
# 设置服务器动态资源的路径(存放wsgi协议程序的路径)
python_root = './wsgiPy'

class WSGIServer(object):

    addr_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5

    def __init__(self, serv_address):
        self.listen_socket = socket.socket(self.addr_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(serv_address)
        self.listen_socket.listen(self.request_queue_size)

        self.serv_name = "127.0.0.1"
        self.serv_port = serv_address[1]

    def serve_forever(self):
        '循环运行web服务器，等待客户端的链接并为客户端服务'
        while True:
            self.cli_socket, cli_addr = self.listen_socket.accept()
            new_client_process = Process(target = self.handle_request)
            new_client_process.start()

            #因为创建的新进程中，会对这个套接字+1，所以需要在主进程中减去依次，即调用一次close
            self.cli_socket.close()

    def set_app(self, application):
        '设置此WSGI服务器调用的应用程序入口函数'
        self.application = application

    def handle_request(self):
        '用一个新的进程，为一个客户端进行服务'
        self.recv_data = self.cli_socket.recv(2017)
        request_header_lines = self.recv_data.splitlines()
        for line in request_header_lines:
            print(line.decode())

        http_request_method_line = request_header_lines[0]
        get_file_name = re.match("[^/]+(/[^ ]*)", http_request_method_line.decode()).group(1)
        print("file name is ===>{}".format(get_file_name)) # for test

        if get_file_name[-3:] != ".py":     # 如果是假的话就是非动态的程序请求
            if get_file_name == '/':
                get_file_name = document_root + "/index.html"
            else:
                get_file_name = document_root + get_file_name

            print("file name is ===2>{}".format(get_file_name)) # for test

            try:
                f = open(get_file_name)
            except IOError:
                start_line = "HTTP/1.1 404 not found\r\n"
                start_line += "\r\n"
                # response_body = "====sorry ,file not found===="
                response_body = '''
                <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset='utf-8'/>
                        <title>404 not found</title>
                    </head>
                    <body>
                        <p>你访问的页面不存在, 不妨回主页看看</p>
                        <a href="http://127.0.0.1:7788" target="_blank">
                            <font size=2><font color="#00ff00">  主页 → </font>
                        </a>
                    </body>
                </html>
                '''
            else:
                start_line = "HTTP/1.1 200 OK\r\n"
                start_line += "\r\n"
                response_body = f.read()
                f.close()
            finally:
                response = start_line + response_body.decode()
                self.cli_socket.send(response.encode())
                self.cli_socket.close()
        else:       # 表示是动态程序请求,调用相应程序
            # mod_name = get_file_name[1:-3]   # 获取模块名
            # try:
            #     # 借助内建函数__import__导入模块, 传入的参数为要导入模块的name, 字符类型
            #     mod = __import__(mod_name)
            # except ModuleNotFoundError:     # 用户请求的不存在
            #     start_line = "HTTP/1.1 404 not found\r\n"
            #     start_line += "\r\n"
            #     response_body = '''
            #     <!DOCTYPE html>
            #     <html>
            #         <head>
            #             <meta charset='utf-8'/>
            #             <title>404 not found</title>
            #         </head>
            #         <body>
            #             <p>你访问的页面不存在, 不妨回主页看看</p>
            #             <a href="http://127.0.0.1:7788" target="_blank">
            #                 <font size=2><font color="#00ff00">  主页 → </font>
            #             </a>
            #         </body>
            #     </html>
            #     '''
            #     response = start_line + response_body
            #     self.cli_socket.send(response.encode())
            # else: 下面是被包含到else中的
            #根据接收到的请求头构造环境变量字典
            env = {}

            #调用应用的相应方法，完成动态数据的获取
            body_content = self.application(env, self.start_response)   # 处理状态码和响应头

            #组织数据发送给客户端
            self.finish_response(body_content)

    def start_response(self, status, response_headers):     # 处理状态码和响应头
        server_headers = [
            ('Date', 'Tue, 31 Mar 2016 10:11:12 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, body_content):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            #response的其他头信息
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            #添加发送的数据
            for data in body_content:
                response += data

            self.cli_socket.send(response.encode())
        finally:
            self.cli_socket.close()

def make_server(server_addr, application):
    server = WSGIServer(server_addr)
    server.set_app(application)
    return server

def main():

    if len(sys.argv) < 2:
        sys.exit('请按照要求，指定模块名称:应用名称,例如 module:callable')

    app_path = sys.argv[1]                      # 获取module:callable
    module, application = app_path.split(':')   # 根据冒号切割为module和callable
    sys.path.insert(0, python_root)             # 添加路径到sys.path
    module = __import__(module)                 # 动态导入module变量中指定的模块
    application = getattr(module, application)  # 获取module变量中指定的模块的，application变量指定的属性
    httpd = make_server(server_addr, application)
    print('WSGIServer: Serving HTTP on port {} ...\n'.format(PORT))
    httpd.serve_forever()

if __name__ == '__main__':
    main()
