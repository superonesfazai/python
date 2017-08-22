import socket
import re
import sys

from multiprocessing import Process


# 用户可以访问的html文件的目录
HTML_ROOT_DIR = "./html"

# 存放wsgi协议程序的路径
WSGI_PYTHON_DIR = "./wsgi_python_program"

# 将要导入模块的路径放到python的搜索路径终
sys.path.insert(1, WSGI_PYTHON_DIR)

class HTTPServer(object):
    """自定义的HTTP服务器类"""
    def __init__(self):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        # 处理响应头
        resp_headers = ''
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
        http_req_data = c_sock.recv(1024)        # 接受客户端传来的数据, 是http协议的请求数据
        print("客户端%s发送的HTTP请求报文：\n %s" % (c_addr, http_req_data.decode()))

        # 解析客户端的请求报文
        http_req_data_str = http_req_data.decode()
        req_start_line = http_req_data_str.split("\r\n")[0]  # 从报文提取请求起始行

        # GET /index.html HTTP/1.1\r\n
        # GET /say_ctime.py HTTP/1.1\r\n
        match_result = re.match(r"(\w+) +(/[^ ]*) +", req_start_line)   # 借助正则从起始行提取用户请求的文件路径

        req_method = match_result.group(1)  # 请求方式
        file_path = match_result.group(2)   # 请求的路径
        environ = {                         # 将解析后的数据放入字典中
            "PATH_INFO": file_path,
            "REQUSET_METHOD": req_method
        }

        # 提取出来file_path参数可能是静态文件路径，也可能是动态程序路径
        # file_path = "/index.html"  "/say_ctime.py"
        if file_path.endswith(".py"):   # 表示是动态的程序请求
            # 调用程序
            # 获取模块名
            mod_name = file_path[1:-3]  # "/say_ctime.py"
            try:
                # 借助内建函数__import__导入模块，传递的参数是要导入的模块名字，字符类型
                mod = __import__(mod_name)  # __import__会把导入的模块对象返回，可以用一个变量接收
            except ModuleNotFoundError:     # 表示用户请求的动态程序不存在，导入失败
                # 构造一个http的响应报文
                start_line = "HTTP/1.0 404 NOT FOUND\r\n"  # 起始行
                headers = "Server: MyServer\r\n"  # 响应头
                headers += "Content-Type: text/html\r\n"
                body = '<h1 style="color:red;">program not exsit</h1>'  # 响应体
                http_resp_data = start_line + headers + "\r\n" + body
                print("返回给客户端的HTTP响应报文：\n %s" % http_resp_data)
                # 将http响应报文传回给客户端
                c_sock.send(http_resp_data.encode())
            else:   # 表示导入成功，用户请求的程序存在
                # 调用模块里的动态程序,会返回响应体
                resp_body = mod.application(environ, self.start_response)
                # 构造最终的响应报文
                resp_data = self.resp_start_line_headers + "\r\n" + resp_body
                c_sock.send(resp_data.encode())

        else:       # 表示是静态的文件请求
            # file_path = "/index.html"  或 "/"
            # 如果用户请求的路径是/，则返回index.html
            if file_path == "/":
                file_path = "/index.html"
            # 读取文件数据
            try:
                file = open(HTML_ROOT_DIR + file_path, "rb")
            except IOError:     # 表示用户请求的文件不存在，打开失败
                start_line = "HTTP/1.0 404 NOT FOUND\r\n"               # 起始行
                headers = "Server: MyServer\r\n"                        # 响应头
                headers += "Content-Type: text/html\r\n"
                body = '<h1 style="color:red;">file not exsit</h1>'     # 响应体
                http_resp_data = start_line + headers + "\r\n" + body
                print("返回给客户端的HTTP响应报文：\n %s" % http_resp_data)
                c_sock.send(http_resp_data.encode())
            else:
                file_data = file.read()
                file.close()

                # 构造一个http的响应报文
                start_line = "HTTP/1.0 200 OK\r\n"                      # 起始行
                headers = "Server: MyServer\r\n"                        # 响应头
                headers += "Content-Type: text/html\r\n"

                http_resp_data = (start_line + headers + "\r\n").encode() + file_data
                c_sock.send(http_resp_data)

        # 关闭这次请求的连接
        c_sock.close()

    def start(self):
        """开启http服务器的运行，接收客户端的连接并处理客户端的数据"""
        self.listen_sock.listen(128)

        while True:
            client_sock, client_addr = self.listen_sock.accept()
            print("客户端%s已连接" % (client_addr,))

            p = Process(target=self.handle_client, args=(client_sock, client_addr))
            p.start()
            # 在主进程中释放client_sock资源
            client_sock.close()


if __name__ == '__main__':
    http_server = HTTPServer()
    http_server.bind(7788)
    http_server.start()



