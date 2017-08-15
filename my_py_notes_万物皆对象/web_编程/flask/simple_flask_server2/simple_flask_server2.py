# coding = utf-8

'''
@author = super_fazai
@File    : simple_flask_server2.py
@Time    : 2017/8/15 21:49
@connect : superonesfazai@gmail.com
'''
"""
在Flask中一个非常重要的概念是请求上下文。Flask使用线程本地对象，如request，session和其他代表当前请求的元素
这些对象只有在初始化请求上下文时可用，当Flask收到HTTP请求时，这些对象才能完成。

Flask与jinja2是一个非常好的模板引擎。模板应该保存为文件templates/夹下的.html文件。
该render_template(filename, **kwargs)功能是一个很简单的方法来渲染它们。
"""

from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D'

@app.route('/')
def home():
    return render_template('index.html')

# @app.route()默认情况下仅限于GET请求。可以使用methods关键字arg 指定允许的操作的HTTP方法
@app.route('/signup', methods=['POST'])
def signup():           # 在该signup()函数中，通过request对象访问请求的数据
    session['username'] = request.form['username']      # request.form是一个MultiDict(在大多数情况下，它的行为就像一个普通的dict)与所有的POST数据，request.args是一个MultiDict与GET参数，request.values是两者的组合
    session['message'] = request.form['message']
    return redirect(url_for('message'))     # url_for(route_name, **kwargs)应该用于为您的处理程序生成URL。它作为第一个参数，函数名称和关键字args任何所需的参数来生成url
                                            # redirect(url) 使用重定向代码和位置创建HTTP响应
@app.route('/message')
def message():          # 用户将在第一页上输入他们的姓名和想要说的内容。数据将存储在会话中 ，并将显示在/message页面上
    if not 'username' in session:
        return abort(403)                   # abort(http_code) 用于创建错误响应并停止执行功能
    return render_template('message.html', username=session['username'],
                                           message=session['message'])

if __name__ == '__main__':
    app.run()