# coding:utf-8

'''
@author = super_fazai
@File    : myflask.py.py
@Time    : 2017/10/21 21:36
@connect : superonesfazai@gmail.com
'''

from flask import Flask, jsonify
from gevent.wsgi import WSGIServer
from time import sleep

app = Flask(__name__)

#这里的json使用中文key
@app.route("/", methods=['GET', 'POST'])
def index():
    # sleep(1)
    return jsonify({'ret':'hi'})

print('高并发的flask程序已经运行')
WSGIServer(('0.0.0.0', 5000), app).serve_forever()
