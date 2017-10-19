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
from flask import send_file
from flask_login import LoginManager

from login_and_parse import LoginAndParse
# from .login_and_parse import LoginAndParse
from my_pipeline import UserItemPipeline
# from .my_pipeline import UserItemPipeline

# from my_pipeline import MyPageInfoSaveItemPipeline
from .my_pipeline import MyPageInfoSaveItemPipeline

import hashlib
import json
import time
import datetime
import re

from gevent.wsgi import WSGIServer      # 高并发部署

# 全局变量
login_ali = LoginAndParse()

app = Flask(__name__, root_path=os.getcwd())

# login_manager = LoginManager(app)

# login_manager.session_protection = 'basic'
# 可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户

# login_manager.login_view = "/"
# 这里填写你的登陆界面的路由

# login_manager.remember_cookie_duration=datetime.timedelta(days=1)

# app.config.update(
#     PERMANENT_SESSION_LIFETIME=datetime.timedelta(seconds=12*60*60)
# )

app.CSRF_ENABLED = True                 # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护。在大多数情况下，你需要激活该配置使得你的应用程序更安全些
app.secret_key = 'fjusfbubvnighwwf'     # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单

# 内部员工口令
inner_pass = 'adminss'

# key 用于加密
key = 15

tmp_wait_to_save_data_list = []

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
                has_username = encrypt(key, username)
                has_passwd = encrypt(key, passwd)

                outdate = datetime.datetime.today() + datetime.timedelta(days=1)

                response.set_cookie('username', value=has_username, max_age=60*60*5, expires=outdate)    # 延长过期时间(1天)
                response.set_cookie('passwd', value=has_passwd, max_age=60*60*5, expires=outdate)
                # session['islogin'] = '1'      # 设置session的话会有访问的时间限制,故我不设置
                # session.permanent = True        # 切记：前面虽然设置了延时时间，但是只有通过这句话才能让其生效
                #                                 # 注意先设置session的permanent为真
                # # 设置session的过期时间为1天(只有设置下面两句话才会生效, 第二句要在请求中才能使用)
                # app.permanent_session_lifetime = datetime.timedelta(seconds=12*60*60)

                return response
        else:
            # session['islogin'] = '0'
            print('登录失败!请重新登录')
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    print('正在获取选择界面...')
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:   # 判断是否为非法登录
        if request.form.get('confirm_login'):       # 二维码已扫描的ajax请求的处理
            is_success_login = login_ali.login()

            if is_success_login:        # 扫码成功
                print('成功获取到cookies')

                return redirect('show')
                # return make_response(redirect('show'))

            else:                       # 未扫码返回下面错误json
                unlogin = {
                    'reason': 'error',
                    'error_code': 0
                }

                unlogin_json = json.dumps(unlogin)
                return unlogin_json
        else:
            return render_template('select.html')
    else:   # 非法登录显示错误网页
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''

@app.route('/js_call_qrcode', methods=['GET', 'POST'])
def js_call_qrcode():
    '''
    根据ajax请求获取验证码url, 并返回二维码地址的json数据
    :return:
    '''
    print(request.form.get('ip'))
    # print("method: " + request.values['method'] + " --- text: " + request.values['text'])

    qrcode_url = login_ali.get_qrcode_url()

    # print(qrcode_url)
    data_qrcode_url = {
        'qrcode_url': qrcode_url,
        'success': 'True',
    }
    data_qrcode_url = json.dumps(data_qrcode_url)
    return data_qrcode_url

@app.route('/Reg', methods=['GET', 'POST'])
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
                str(username),
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

@app.route('/show', methods=['GET', 'POST'])
def show_info():
    '''
    扫码成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:     # request.cookies -> return a dict
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后, 并且成功扫描二维码后，再继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件

@app.route("/data", methods=['POST'])
def get_all_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                tmp_item = re.compile(r'(.*?)\?.*?').findall(goodsLink)  # 过滤筛选出唯一的阿里1688商品链接
                if tmp_item == []:
                    wait_to_deal_with_url = goodsLink
                else:
                    wait_to_deal_with_url = tmp_item[0]
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            login_ali.set_wait_to_deal_with_url(wait_to_deal_with_url)
            data = login_ali.deal_with_page_url()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data is 4041:    # 4041表示给与的待爬取的地址错误, 前端重置输入框，并提示输入的内容非正确网址，请重新输入
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': data,
                }

                result = json.dumps(result)
                return result

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = data
            wait_to_save_data['spider_url'] = wait_to_deal_with_url
            wait_to_save_data['username'] = username
            wait_to_save_data['deal_with_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('-->> 下面是爬取到的页面信息: ')
            print(result_json.decode())
            return result_json.decode()
        else:
            print('goodsLink为空!')

    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        result = json.dumps(result)
        return result

@app.route('/to_save_data', methods=['POST'])
def to_save_data():
    '''
    存储请求存入的每个url对应的信息
    :return:
    '''
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):      # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))   # 一个待存取的url的list

            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                my_page_info_save_item_pipeline = MyPageInfoSaveItemPipeline()
                for item in wait_to_save_data_url_list:
                    tmp_item = re.compile(r'(.*?)\?.*?').findall(item)  # 过滤筛选出唯一的阿里1688商品链接
                    if tmp_item == []:
                        wait_to_save_data_url = item
                    else:
                        wait_to_save_data_url = tmp_item[0]

                    for index in range(0, len(tmp_wait_to_save_data_list)-1):
                        if wait_to_save_data_url == tmp_wait_to_save_data_list[index]['spider_url']:
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['spider_url'] = data_list['spider_url']
                            tmp['username'] = data_list['username']
                            tmp['deal_with_time'] = data_list['deal_with_time']

                            tmp['title'] = data_list['title']
                            tmp['price'] = ';'.join(data_list['price'])
                            tmp['trade_number'] = ';'.join(data_list['trade_number'])   # list为[], 值就为'', 不为空, 1个就是'xx', 多个就是'xx;yy'
                            tmp['color'] = ';'.join(data_list['color'])
                            tmp['color_img_url'] = ';'.join(data_list['color_img_url'])
                            tmp['size_info'] = ';'.join(data_list['size_info'])
                            tmp['detail_price'] = ';'.join(data_list['detail_price'])
                            tmp['rest_number'] = ';'.join(data_list['rest_number'])
                            tmp['center_img_url'] = ';'.join(data_list['center_img_url'])
                            tmp['all_img_url'] = ';'.join(data_list['all_img_url'])

                            is_insert_into = my_page_info_save_item_pipeline.insert_into_table(tmp)
                            if is_insert_into:      # 如果返回值为True
                                tmp_wait_to_save_data_list.pop(index)
                            else:
                                print('插入失败!')
                                pass

            else:
                print('saveData为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4043,  # batchGoodsLink为空
                }
                result = json.dumps(result)
                return result
        else:
            print('saveData为空!')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4043,  # batchGoodsLink为空
            }
            result = json.dumps(result)
            return result

    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        result = json.dumps(result)
        return result

"""
@app.route("/much_data", methods=['POST'])
def get_all_muckh_data():
    '''
    批量获取对应网址的info
    :return:
    '''
    all_data = []
    print('客户端正在请求批量抓取...')
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('batchGoodsLink[]'):    # 切记：从客户端获取list数据的方式
            print('正在获取相应数据中...')
            wait_to_deal_with_url_list = list(request.form.getlist('batchGoodsLink[]'))    # 获取到的是一个待爬取的url的list

            print('获取到的待爬取的list为: ', wait_to_deal_with_url_list)
            if wait_to_deal_with_url_list != []:
                for item in wait_to_deal_with_url_list:
                    tmp_item = re.compile(r'(.*?)&.*?').findall(item)  # 过滤筛选出唯一的阿里1688商品链接
                    if tmp_item == []:
                        wait_to_deal_with_url = item
                    else:
                        wait_to_deal_with_url = tmp_item[0]

                    login_ali.set_wait_to_deal_with_url(wait_to_deal_with_url)
                    data = login_ali.deal_with_page_url()  # 如果成功获取的话, 返回的是一个data的json对象

                    if data is 4041:  # 4041表示给与的待爬取的地址错误, 前端重置输入框，并提示输入的内容非正确网址，请重新输入
                        result = {
                            'reason': 'error',
                            'data': '',
                            'error_code': data,
                        }

                        result = json.dumps(result)
                        return result

                    print(data)
                    all_data.append(data)       # 一个list里面存放的是所有的dict
                result = {
                    'reason': 'success',
                    'data': all_data,
                    'error_code': 0,
                }

                result_json = json.dumps(result, ensure_ascii=False).encode()
                print('-->> 下面是爬取到的页面信息: ')
                print(result_json.decode())
                return result_json.decode()
            else:
                print('batchGoodsLink为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4043,     # batchGoodsLink为空
                }
                result = json.dumps(result)
                return result
        else:
            print('batchGoodsLink为空!')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4043,  # batchGoodsLink为空
            }
            result = json.dumps(result)
            return result
    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        result = json.dumps(result)
        return result
"""

def encrypt(key, s):
    '''
    加密算法
    :param key:
    :param s:
    :return:
    '''
    b = bytearray(str(s).encode("gbk"))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")

def decrypt(key, s):
    '''
    解密算法
    :param key:
    :param s:
    :return:
    '''
    c = bytearray(str(s).encode("gbk"))
    n = len(c) # 计算 b 的字节数
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except:
        return "failed"


if __name__ == "__main__":
    print('服务器已经启动...等待接入中...')
    print('http://0.0.0.0:5000')
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()      # 采用高并发部署
    # app.run(host= '0.0.0.0', debug=False, port=5000)

    # 简单的多线程
    # app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
