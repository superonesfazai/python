import time

# 用户可以访问的html文件的目录
HTML_ROOT_DIR = "./html"


class Application(object):
    """抽象出来的中间人，可以理解为网站的核心应用，框架"""
    def __init__(self, urls):
        """
        创建一个http应用程序，保存路由列表
        :param urls: [(路径，处理的函数),()]  路由列表
        """
        self.urls = urls

    def __call__(self, environ, start_response):
        """
        当HTTP服务器收到客户端请求并解析好HTTP报文后，调用
        :param environ:  dict 保存了解析好的HTTP报文数据
        :param start_response:  function对象，http服务器传入进来的，用来接收状态码和响应头
        :return: 返回响应体
        """
        path = environ["PATH_INFO"]     # 从environ请求数据字典中读取用户的请求路径
        # path  "/static/index.html"   "/say_ctime"
        if path.startswith("/static"):  # 表示用户请求的是静态文件
            file_path = path[7:]        # path == "/static/index.html"
            # file_path = "/index.html"  或 "/"
            # 如果用户请求的路径是/，则返回index.html
            if file_path == "/":
                file_path = "/index.html"
            # 读取文件数据
            try:
                file = open(HTML_ROOT_DIR + file_path, "rb")
            except IOError:
                # 表示用户请求的文件不存在，打开失败
                status_code = "404 Not Found" # 状态码
                response_headers = [("Server", "MyServer"), ("Content-Type", "text/html")]  # 响应头
                start_response(status_code, response_headers)
                return b'<h1 style="color:red;">file not exist</h1>'  # 响应体
            else:
                # 表示请求的文件存在，
                # 读取文件数据, python3中 文件读取出的数据bytes类型
                file_data = file.read()
                file.close()

                # 构造一个http的响应报文
                status_code = "200 OK" # 状态码
                response_headers = [("Server", "MyServer"), ("Content-Type", "text/html")]  # 响应头
                start_response(status_code, response_headers)

                return file_data
        else:
            # 表示用户请求的是动态程序
            # path == "/say_ctime"
            # 遍历保存的路径列表，找到对应于用户请求的函数
            for view_path, view_fun in self.urls:
                if view_path == path:
                    # 找到了用户请求对应的函数
                    response_body = view_fun(environ, start_response)
                    # 将接受到的视图函数中的字符串返回值转换为字节类型
                    return response_body.encode()

            # 当循环执行完，还没有返回，表示用户请求的路径不存在
            status_code = "404 Not Found"  # 状态码
            response_headers = [("Server", "MyServer"), ("Content-Type", "text/html")]  # 响应头
            start_response(status_code, response_headers)
            return b'<h1 style="color:red;">program not exist</h1>'  # 响应体


# 定义视图函数  view
def say_ctime(environ, start_response):
    """
    处理客户端的动态请求
    :param environ:   dict  服务器传递的参数，包含了解析之后的客户端http请求数据
    :param start_response:  function对象， 处理响应状态码和响应头
    :return: 响应体数据
    """
    status_code = "200 OK"  # 状态码
    response_headers = [("Servre", "MyServer"), ("Content-Type", "text")]  # 响应头

    # 通过调用start_response函数，让服务器接收状态和响应头
    start_response(status_code, response_headers)

    # 通过返回值返回响应体
    return time.ctime()

def say_hello(environ, start_response):
    """
    处理客户端的动态请求
    :param environ:   dict  服务器传递的参数，包含了解析之后的客户端http请求数据
    :param start_response:  function对象， 处理响应状态码和响应头
    :return: 响应体数据
    """
    status_code = "200 OK"  # 状态码
    response_headers = [("Servre", "MyServer"), ("Content-Type", "text")]  # 响应头

    # 通过调用start_response函数，让服务器接收状态和响应头
    start_response(status_code, response_headers)

    # 通过返回值返回响应体
    return "hello" + str(time.time())


urls = [("/say_ctime", say_ctime), ("/hello", say_hello)]  # 路由信息 （路由列表）
app = Application(urls)



# app最终是被HTTP服务器按照WSGI协议使用的

# response_body = app(environ, start_response)