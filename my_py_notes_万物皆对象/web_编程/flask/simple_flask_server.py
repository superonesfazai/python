# coding = utf-8

'''
@author = super_fazai
@File    : simple_flask_server.py
@Time    : 2017/8/15 21:45
@connect : superonesfazai@gmail.com
'''

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

if __name__ == "__main__":
    app.run()