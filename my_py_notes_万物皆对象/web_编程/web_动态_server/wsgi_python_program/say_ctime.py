import time


def application(environ, start_response):
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
