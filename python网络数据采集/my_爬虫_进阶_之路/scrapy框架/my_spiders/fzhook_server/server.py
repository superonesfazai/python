# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

"""
server端: 提供多种本地服务
"""

from flask import (
    Flask,
    send_file,)
from os import getcwd

from settings import (
    SERVER_PORT,
)

from json import dumps
from pprint import pprint

try:
    from gevent.wsgi import WSGIServer      # 高并发部署
except Exception as e:
    from gevent.pywsgi import WSGIServer

app = Flask(__name__, root_path=getcwd())

@app.route('/', methods=['GET', 'POST'])
def home():
    return '欢迎来到 fzhook_server 主页!'

@app.route('/dy', methods=['GET', 'POST'])
def dy():
    """
    获取dy 无水印视频
    :return:
    """
    return send_file('templates/douyin.php')

def main():
    print('server 已启动...\nhttp://0.0.0.0:{}\n'.format(SERVER_PORT))
    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

if __name__ == '__main__':
    main()
