# coding:utf-8

'''
@author = super_fazai
@File    : my_server.py
@Time    : 2017/10/13 09:30
@connect : superonesfazai@gmail.com
'''

import sys, os
sys.path.append(os.getcwd())

from flask import Flask, render_template, url_for, request,redirect,make_response,session, jsonify, Response
from MySQLdb import *
import base64

# from login_and_parse import LoginAndParse
from .login_and_parse import LoginAndParse
# from my_pipeline import UserItemPipeline
from .my_pipeline import UserItemPipeline

import hashlib

# 全球变量
login_ali = LoginAndParse()

app = Flask(__name__)
app.CSRF_ENABLED = True                 # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护。在大多数情况下，你需要激活该配置使得你的应用程序更安全些
app.secret_key = 'fjusfbubvnighwwf'     # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单
user_list = [
    ('admin', 'admin'),
]

# 内部员工口令
inner_pass = 'adminss'

data = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        passwd = str(request.form.get('passwd'))
        print(username + ' : ' + passwd)

        tmp_user = UserItemPipeline()
        is_have_user = tmp_user.select_is_had_username(username, passwd)

        if is_have_user:
                response = make_response(redirect('select'))    # 重定向到新的页面

                # 加密
                has_ = hashlib.sha256()
                has_.update(username.encode())
                has_username = has_.hexdigest()

                has_ = hashlib.sha256()
                has_.update(passwd.encode())
                has_passwd = has_.hexdigest()

                response.set_cookie('username', value=has_username, max_age=400)
                response.set_cookie('passwd', value=has_passwd, max_age=400)
                session['islogin'] = '1'
                return response
        else:
            session['islogin'] = '0'
            print('失败!')
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/js_call_qrcode', methods=['GET', 'POST'])
def js_call_qrcode():
    '''
    根据ajax请求获取验证码url, 并返回二维码地址的json数据
    :return:
    '''
    print(request.values['ip'])
    print("method: " + request.values['method'] + " --- text: " + request.values['text'])

    qrcode_url = login_ali.get_qrcode_url()

    data_qrcode_url = [
        {
            'qrcode_url': qrcode_url,
            'success': 'True',
        }
    ]
    return jsonify({"data": data_qrcode_url})

@app.route("/data", methods=['POST'])
def get_all_data():
    if request.method == 'POST':
        print('正在获取相应数据中...')
        data = login_ali.deal_with_page_url()   # 如果成功获取的话, 返回的是一个data的json对象

        if data is 4041:    # 4041表示给与的待爬取的地址错误, 前端重置输入框，并提示输入的内容非正确网址，请重新输入
            result = {
                'reason': 'error',
                'data': '',
                'error_code': data,
            }
            return jsonify(result)

        return jsonify(data)

    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        return jsonify(result)

@app.route('/Reg', methods=['GET','POST'])
def regist():
    '''
    注册新用户页面
    :return:
    '''
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        tmp_inner_pass = request.form['inner_pass']

        if tmp_inner_pass == inner_pass:    # 正确输入员工口令

            tmp_user = UserItemPipeline()
            item = [
                username,
                passwd,
            ]
            is_insert_into = tmp_user.insert_into_table(item)

            if is_insert_into:
                return redirect('/')
            else:
                return "用户注册失败!"

        else:       # 输入员工口令错误
            return "内部员工口令错误, 请返回重新注册!"

    else:
        #request.args['username']
        return render_template('Reg.html')

def get_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


if __name__ == "__main__":
    app.run(debug=False, port=5000)
