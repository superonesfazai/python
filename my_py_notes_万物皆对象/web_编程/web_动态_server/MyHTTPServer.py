import socket
import re
import sys
import MyFramework

from multiprocessing import Process


class HTTPServer(object):
    """自定义的HTTP服务器类"""
    def __init__(self, application):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.app = application

    def bind(self, port):
        """
        为服务器绑定端口
        :param port:  int  服务器的端口
        :return: None
        """
        address = ("", port)
        self.listen_sock.bind(address)

    def start_response(self, status_code, response_headers):
        """
        服务器提供的用来接收状态码与响应头的函数
        :param status_code:  "200 OK" 状态码
        :param response_headers: [("Servre", "MyServer"), ("Content-Type", "text")]   响应头的列表
        :return: None
        """
        resp_start_line = "HTTP/1.0 " + status_code + "\r\n"  # 形成响应起始行
        # 处理响应头，
        resp_headers = ""
        for header_name, header_value in response_headers:
            resp_headers += (header_name + ": " + header_value + "\r\n")
        # 将处理好的起始行与响应头拼接好后保存起来
        self.resp_start_line_headers = resp_start_line + resp_headers

    def handle_client(self, c_sock, c_addr):
        """
        子进程处理客户端的请求的
        :param c_sock:  socket类型对象  用来与客户端通信的socket对象
        :param c_addr:  元祖类型 (ip, port)  请求的客户端的地址信息
        :return: None
        """
        # 接受客户端传来的数据, 是http协议的请求数据
        http_req_data = c_sock.recv(1024)
        print("客户端%s发送的HTTP请求报文：\n %s" % (c_addr, http_req_data.decode()))

        # 解析客户端的请求报文
        http_req_data_str = http_req_data.decode()
        req_start_line = http_req_data_str.split("\r\n")[0]  # 从报文提取请求起始行

        # GET /index.html HTTP/1.1\r\n
        # GET /say_ctime.py HTTP/1.1\r\n
        # 借助正则从起始行提取用户请求的文件路径
        match_result = re.match(r"(\w+) +(/[^ ]*) +", req_start_line)
        req_method = match_result.group(1)  # 请求方式
        file_path = match_result.group(2)  # 请求的路径
        # 将解析后的数据放入字典中
        environ = {
            "PATH_INFO": file_path,
            "REQUEST_METHOD": req_method
        }
        response_body = self.app(environ, self.start_response)
        # 构造最终的响应报文
        response_data = (self.resp_start_line_headers + "\r\n").encode() + response_body
        c_sock.send(response_data)

        c_sock.close()

    def start(self):
        """开启http服务器的运行，接收客户端的连接并处理客户端的数据"""
        self.listen_sock.listen(128)

        while True:
            client_sock, client_addr = self.listen_sock.accept()
            print("客户端%s已连接" % (client_addr,))

            # 创建子进程，处理客户端的请求数据
            p = Process(target=self.handle_client, args=(client_sock, client_addr))
            p.start()

            # 在主进程中释放client_sock资源
            client_sock.close()


if __name__ == '__main__':
    http_server = HTTPServer(MyFramework.app)
    http_server.bind(8080)
    http_server.start()



