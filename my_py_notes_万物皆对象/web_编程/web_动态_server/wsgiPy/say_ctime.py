# coding = utf-8

'''
@author = super_fazai
@File    : say_ctime.py
@Time    : 2017/8/22 10:09
@connect : superonesfazai@gmail.com
'''
import time

def application(envion, start_response):
    '''
    处理客户端动态请求
    :param envion:
    :param start_response:
    :return:
    '''
    status_code = '200 OK'      # 状态码
    response_headers = [('Server', 'MyServer'), ('Content-Type', 'text')]
    # 通过调用start_response函数, 让服务器接收状态和响应头
    start_response(status_code, response_headers)

    return time.ctime()
