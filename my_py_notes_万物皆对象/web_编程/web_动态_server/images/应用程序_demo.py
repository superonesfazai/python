# coding = utf-8

'''
@author = super_fazai
@File    : 应用程序_demo.py
@Time    : 2017/8/20 18:16
@connect : superonesfazai@gmail.com
'''

import time

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [str(environ)+'==Hello world from a simple WSGI application!--->%s\n'%time.ctime()]