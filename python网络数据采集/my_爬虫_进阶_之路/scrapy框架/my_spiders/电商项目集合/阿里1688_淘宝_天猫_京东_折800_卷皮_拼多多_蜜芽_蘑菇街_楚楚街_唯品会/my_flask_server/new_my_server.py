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

from ali_1688_parse import ALi1688LoginAndParse
from taobao_parse import TaoBaoLoginAndParse
from tmall_parse import TmallParse
from jd_parse import JdParse
from zhe_800_parse import Zhe800Parse
from juanpi_parse import JuanPiParse
from pinduoduo_parse import PinduoduoParse
from vip_parse import VipParse
from my_pipeline import UserItemPipeline
from settings import ALi_SPIDER_TO_SHOW_PATH, TAOBAO_SPIDER_TO_SHWO_PATH, TMALL_SPIDER_TO_SHOW_PATH, JD_SPIDER_TO_SHOW_PATH, ZHE_800_SPIDER_TO_SHOW_PATH, JUANPI_SPIDER_TO_SHOW_PATH, PINDUODUO_SPIDER_TO_SHOW_PATH, VIP_SPIDER_TO_SHOW_PATH
from settings import ADMIN_NAME, ADMIN_PASSWD, SERVER_PORT
from settings import ERROR_HTML_CODE
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import BASIC_APP_KEY
from settings import TAOBAO_SLEEP_TIME
from settings import SELECT_HTML_NAME

import hashlib
import json
import time
from time import sleep
import datetime
import re
from decimal import Decimal

from gevent.wsgi import WSGIServer      # 高并发部署
import gc
import pytz

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
app.secret_key = 'fjusfbubvnighwwf#%&'     # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单

# 内部员工口令
inner_pass = 'adminss'

# key 用于加密
key = 21

tmp_wait_to_save_data_list = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username', '') != '' and request.form.get('passwd', '') != '':
            username = str(request.form.get('username'))
            passwd = str(request.form.get('passwd'))
            print(username + ' : ' + passwd)
        else:
            username, passwd = ('', '',)

        if request.form.get('superUser', '') != '' and request.form.get('superPass', '') != '':
            super_name = str(request.form.get('superUser', ''))
            super_passwd = str(request.form.get('superPass', ''))
            # print('super_name:', super_name, ' ', 'super_passwd:', super_passwd)
        else:
            super_name, super_passwd = ('', '',)

        if super_name == ADMIN_NAME and super_passwd == ADMIN_PASSWD:   # 先判断是否为admin，如果是转向管理员管理界面
            print('超级管理员密码匹配正确')
            response = make_response(redirect('admin'))    # 重定向到新的页面

            # 加密
            has_super_name = encrypt(key, super_name)
            has_super_passwd = encrypt(key, super_passwd)

            outdate = datetime.datetime.today() + datetime.timedelta(days=1)

            response.set_cookie('super_name', value=has_super_name, max_age=60 * 60 * 5, expires=outdate)  # 延长过期时间(1天)
            response.set_cookie('super_passwd', value=has_super_passwd, max_age=60 * 60 * 5, expires=outdate)
            return response

        else:                   # 否则为普通用户，进入选择页面
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
        if request.form.get('confirm_login'):       # 根据ajax请求类型的分别处理
            ajax_request = request.form.get('confirm_login')
            if ajax_request == 'ali_login':
                # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
                # return send_file(SPIDER_TO_SHOW_PATH)
                response = make_response(redirect('show_ali'))    # 重定向到新的页面
                return response

            elif ajax_request == 'taob_login':
                response = make_response(redirect('show_taobao'))  # 重定向到新的页面
                return response

            elif ajax_request == 'tianm_login':
                response = make_response(redirect('show_tmall'))  # 重定向到新的页面
                return response

            elif ajax_request == 'jd_login':
                response = make_response(redirect('show_jd'))
                return response

            elif ajax_request == 'zhe_800_login':
                response = make_response(redirect('show_zhe_800'))
                return response

            elif ajax_request == 'juanpi_login':
                response = make_response(redirect('show_juanpi'))
                return response

            elif ajax_request == 'pinduoduo_login':
                response = make_response(redirect('show_pinduoduo'))
                return response

            elif ajax_request == 'vip_login':
                response = make_response(redirect('show_vip'))
                return response

            else:
                return ERROR_HTML_CODE
        else:
            return render_template(SELECT_HTML_NAME)
    else:   # 非法登录显示错误网页
        return ERROR_HTML_CODE

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    '''
    管理员页面
    :return:
    '''
    # print('正在获取登录界面...')
    if request.cookies.get('super_name', '') == encrypt(key, ADMIN_NAME) and request.cookies.get('super_passwd', '') == encrypt(key, ADMIN_PASSWD):   # 判断是否为非法登录
        if request.method == 'POST':
            tmp_user = UserItemPipeline()

            # 查找
            if request.form.get('find_name', '') != '':
                find_name = request.form.get('find_name', '')

                if len(find_name) == 11 and re.compile(r'^1').findall(find_name) != []:                            # 根据手机号查找
                    result = tmp_user.find_user_by_username(username=find_name)
                    if result != []:
                        print('查找成功!')
                        # print(result)     # 只返回的是一个list 如: ['15661611306', 'xxxx', datetime.datetime(2017, 10, 13, 10, 0), '杭州', 'xxx']
                        data = [{
                            'username': result[0],
                            'passwd': encrypt(key, result[1]),
                            'createtime': str(result[2]),    # datetime类型转换为字符串 .strftime('%Y-%m-%d %H:%M:%S')
                            'department': result[3],
                            'realnane': result[4]}]
                        result = {
                            'reason': 'success',
                            'data': data,
                            'error_code': 1,
                        }
                        result = json.dumps(result, ensure_ascii=False).encode()
                        return result.decode()

                    else:
                        print('查找失败!')
                        result = {
                            'reason': 'error',
                            'data': [],
                            'error_code': 0,  # 表示goodsLink为空值
                        }
                        result = json.dumps(result)
                        return result

                elif len(find_name) > 1 and len(find_name) <= 4:     # 根据用户名查找
                    result = tmp_user.find_user_by_real_name(name=find_name)
                    print(result)
                    if result != []:
                        print('查找成功!')
                        data = [{
                            'username': item[0],
                            'passwd': encrypt(key, item[1]),
                            'createtime': str(item[2]),
                            'department': item[3],
                            'realnane': item[4]} for item in result]
                        result = {
                            'reason': 'success',
                            'data': data,
                            'error_code': 1,
                        }
                        result = json.dumps(result, ensure_ascii=False).encode()
                        return result.decode()

                    else:
                        print('查找失败!')
                        result = {
                            'reason': 'error',
                            'data': [],
                            'error_code': 0,  # 表示goodsLink为空值
                        }

                        result = json.dumps(result)
                        return result
                else:
                    print('find_name非法!')
                    result = {
                        'reason': 'error',
                        'data': [],
                        'error_code': 0,  # 表示goodsLink为空值
                    }
                    result = json.dumps(result)
                    return result

            # 重置
            elif request.form.get('update', '') != '':
                update_name = request.form.get('update', '')
                result = tmp_user.init_user_passwd(username=update_name)
                if result:
                    print('重置密码成功!')
                    # 返回所有数据
                    result = tmp_user.select_all_info()
                    data = [{
                        'username': item[0],
                        'passwd': encrypt(key, item[1]),
                        'createtime': str(item[2]),
                        'department': item[3],
                        'realnane': item[4]} for item in result]
                    result = {
                        'reason': 'error',
                        'data': data,
                        'error_code': 1,
                    }
                    result = json.dumps(result, ensure_ascii=False).encode()
                    return result.decode()

                else:
                    print('重置密码失败!')
                    result = tmp_user.select_all_info()
                    data = [{
                        'username': item[0],
                        'passwd': encrypt(key, item[1]),
                        'createtime': str(item[2]),
                        'department': item[3],
                        'realnane': item[4]} for item in result]
                    result = {
                        'reason': 'error',
                        'data': data,
                        'error_code': 1,
                    }
                    result = json.dumps(result, ensure_ascii=False).encode()
                    return result.decode()

            # 删除
            elif request.form.getlist('user_to_delete_list[]') != []:
                user_to_delete_list = list(request.form.getlist('user_to_delete_list[]'))
                result = tmp_user.delete_users(item=user_to_delete_list)
                if result:
                    print('删除成功!')
                    result = tmp_user.select_all_info()
                    data = [{
                        'username': item[0],
                        'passwd': encrypt(key, item[1]),
                        'createtime': str(item[2]),
                        'department': item[3],
                        'realnane': item[4]} for item in result]
                    result = {
                        'reason': 'success',
                        'data': data,
                        'error_code': 1,
                    }
                    result = json.dumps(result, ensure_ascii=False).encode()
                    return result.decode()

                else:       # 删除失败(删除失败也返回数据库中所有注册员工的数据)，让前端提醒下，数据库异常，删除失败
                    print('删除失败!')
                    result = tmp_user.select_all_info()
                    data = [{
                        'username': item[0],
                        'passwd': encrypt(key, item[1]),
                        'createtime': str(item[2]),
                        'department': item[3],
                        'realnane': item[4]} for item in result]
                    result = {
                        'reason': 'error',
                        'data': data,
                        'error_code': 1,
                    }
                    result = json.dumps(result, ensure_ascii=False).encode()
                    return result.decode()

            # 查看现有所有用户数据
            elif request.form.get('check_all_users', '') == 'True':
                print('返回所有注册员工信息!')
                result = tmp_user.select_all_info()
                data = [{
                    'username': item[0],
                    'passwd': encrypt(key, item[1]),
                    'createtime': str(item[2]),
                    'department': item[3],
                    'realnane': item[4]} for item in result]
                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 1,
                }
                result = json.dumps(result, ensure_ascii=False).encode()
                return result.decode()

            elif request.form.get('username', '') != '':
                username = request.form.get('username', '')
                passwd = request.form.get('passwd', '')

                real_name = request.form.get('ralenane', '')
                department = request.form.get('department', '')

                '''
                时区处理，时间处理到上海时间
                '''
                tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                now_time = datetime.datetime.now(tz)

                # 处理为精确到秒位，删除时区信息
                now_time = re.compile(r'\..*').sub('', str(now_time))
                # 将字符串类型转换为datetime类型
                now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
                create_time = now_time

                item = [
                    str(username),
                    str(passwd),
                    create_time,
                    str(department),
                    str(real_name),
                ]
                is_insert_into = tmp_user.insert_into_table(item)

                if is_insert_into:
                    print('用户 %s 注册成功!' % username)
                else:
                    print("用户注册失败!")

                return send_file('templates/admin.html')

            else:
                pass

        else:
            # return render_template('admin.html')
            return send_file('templates/admin.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件

    else:   # 非法登录显示错误网页
        return ERROR_HTML_CODE

@app.route('/Reg', methods=['GET', 'POST'])
def regist():
    '''
    注册新用户页面
    :return:
    '''
    if request.method == 'POST':
        username = request.form.get('username', '')
        passwd = request.form.get('passwd', '')

        real_name = request.form.get('ralenane', '')
        department = request.form.get('department', '')
        tmp_inner_pass = request.form.get('inner_pass', '')

        if real_name == '' or department == '' or username == '' or passwd == '':
            return '''
            <html><header></header><body>(真实姓名,所属部门,手机号,密码)皆不能为空，请返回注册页面继续进行相关注册操作!<a href="/Reg"></br></br>返回注册页面</a></body></html>
            '''

        if tmp_inner_pass == inner_pass:    # 正确输入员工口令
            tmp_user = UserItemPipeline()

            '''
            时区处理，时间处理到上海时间
            '''
            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
            now_time = datetime.datetime.now(tz)

            # 处理为精确到秒位，删除时区信息
            now_time = re.compile(r'\..*').sub('', str(now_time))
            # 将字符串类型转换为datetime类型
            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
            create_time = now_time

            item = [
                str(username),
                str(passwd),
                create_time,
                str(department),
                str(real_name),
            ]
            is_insert_into = tmp_user.insert_into_table(item)

            if is_insert_into:
                print('用户 %s 注册成功!' % username)
                return redirect('/')
            else:
                return "用户注册失败!"

        else:       # 输入员工口令错误
            return "内部员工口令错误, 请返回重新注册!"

    else:
        return render_template('Reg.html')

######################################################

@app.route('/show_ali', methods=['GET', 'POST'])
def show_ali_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:     # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass        # 让前端发个post请求, 重置页面
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(ALi_SPIDER_TO_SHOW_PATH)

@app.route('/show_taobao', methods=['GET', 'POST'])
def show_taobao_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE

    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(TAOBAO_SPIDER_TO_SHWO_PATH)

@app.route('/show_tmall', methods=['GET', 'POST'])
def show_tmall_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(TMALL_SPIDER_TO_SHOW_PATH)

@app.route('/show_jd', methods=['GET', 'POST'])
def show_jd_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(JD_SPIDER_TO_SHOW_PATH)

@app.route('/show_zhe_800', methods=['GET', 'POST'])
def show_zhe_800_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(ZHE_800_SPIDER_TO_SHOW_PATH)

@app.route('/show_juanpi', methods=['GET', 'POST'])
def show_juanpi_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(JUANPI_SPIDER_TO_SHOW_PATH)

@app.route('/show_pinduoduo', methods=['GET', 'POST'])
def show_pinduoduo_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(PINDUODUO_SPIDER_TO_SHOW_PATH)

@app.route('/show_vip', methods=['GET', 'POST'])
def show_vip_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(VIP_SPIDER_TO_SHOW_PATH)

######################################################
# ali_1688
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

            login_ali = ALi1688LoginAndParse()

            goods_id = login_ali.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del login_ali       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            tmp_result = login_ali.get_ali_1688_data(goods_id=goods_id)

            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del login_ali
                gc.collect()
                result = json.dumps(result)
                return result

            data = login_ali.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del login_ali
                gc.collect()
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
            # wait_to_save_data['deal_with_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tmp_goods_id = re.compile(r'.*?/offer/(.*?).html').findall(wait_to_deal_with_url)[0]
            wait_to_save_data['goods_id'] = tmp_goods_id        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            # print('------>>> 下面是爬取到的页面信息: ')
            # print(result_json.decode())
            # print('-------------------------------')

            del login_ali       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':      # 除去传过来是空值
                        pass
                    else:
                        tmp_goods_id = re.compile(r'.*?/offer/(.*?).html.*?').findall(item)[0]
                        tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))       # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []           # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):      # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']                                 # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']                             # 商品地址
                            tmp['username'] = data_list['username']                                 # 操作人员username
                            # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)

                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time                                        # 操作时间
                            tmp['modfiy_time'] = now_time                                           # 修改时间

                            tmp['company_name'] = data_list['company_name']                         # 公司名称
                            tmp['title'] = data_list['title']                                       # 商品名称
                            tmp['link_name'] = data_list['link_name']                               # 卖家姓名

                            # 设置最高价price， 最低价taobao_price
                            if len(data_list['price_info']) > 1:
                                tmp_ali_price = []
                                for item in data_list['price_info']:
                                    tmp_ali_price.append(float(item.get('price')))

                                if tmp_ali_price == []:
                                    tmp['price'] = Decimal(0).__round__(2)
                                    tmp['taobao_price'] = Decimal(0).__round__(2)
                                else:
                                    tmp['price'] = Decimal(sorted(tmp_ali_price)[-1]).__round__(2)          # 得到最大值并转换为精度为2的decimal类型
                                    tmp['taobao_price'] = Decimal(sorted(tmp_ali_price)[0]).__round__(2)
                            elif len(data_list['price_info']) == 1:         # 由于可能是促销价, 只有一组然后价格 类似[{'begin': '1', 'price': '485.46-555.06'}]
                                if re.compile(r'-').findall(data_list['price_info'][0].get('price')) != []:
                                    tmp_price_range = data_list['price_info'][0].get('price')
                                    tmp_price_range = tmp_price_range.split('-')
                                    tmp['price'] = tmp_price_range[1]
                                    tmp['taobao_price'] = tmp_price_range[0]
                                else:
                                    tmp['price'] = Decimal(data_list['price_info'][0].get('price')).__round__(2)  # 得到最大值并转换为精度为2的decimal类型
                                    tmp['taobao_price'] = tmp['price']
                            else:   # 少于1
                                tmp['price'] = Decimal(0).__round__(2)
                                tmp['taobao_price'] = Decimal(0).__round__(2)

                            tmp['price_info'] = data_list['price_info']                             # 价格信息

                            spec_name = []
                            for item in data_list['sku_props']:
                                tmp_dic = {}
                                tmp_dic['spec_name'] = item.get('prop')
                                spec_name.append(tmp_dic)

                            tmp['spec_name'] = spec_name                                            # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['sku_map'] = data_list.get('sku_map')                               # 每个规格对应价格及其库存

                            tmp['all_img_url_info'] = data_list.get('all_img_url')                  # 所有示例图片地址

                            tmp['property_info'] = data_list.get('property_info')                   # 详细信息
                            tmp['detail_info'] = data_list.get('detail_info')                       # 下方div

                            # 采集的来源地
                            tmp['site_id'] = 2                                                      # 采集来源地(阿里1688批发市场)
                            tmp['is_delete'] = 0                                                    # 逻辑删除, 未删除为0, 删除为1
                            # tmp['is_modfiy'] = 0                                                    # 表示是否已修改，0未修改

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]    # 删除已被插入
                print('存入完毕'.center(100, '*'))
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# taobao
@app.route('/taobao_data', methods=['POST'])
def get_taobao_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            login_taobao = TaoBaoLoginAndParse()

            goods_id = login_taobao.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del login_taobao       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id   # 构造成标准干净的淘宝商品地址
            tmp_result = login_taobao.get_goods_data(goods_id=goods_id)
            time.sleep(TAOBAO_SLEEP_TIME)     # 这个在服务器里面可以注释掉为.5s
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del login_taobao
                gc.collect()
                result = json.dumps(result)
                return result

            data = login_taobao.deal_with_data(goods_id=goods_id)   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del login_taobao
                gc.collect()
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
            # wait_to_save_data['deal_with_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            wait_to_save_data['goods_id'] = goods_id        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del login_taobao       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/taobao_to_save_data', methods=['POST'])
def taobao_to_save_data():
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(item)
                        if is_taobao_url != []:
                            if re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item) != []:
                                tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item)[0]
                                # print(tmp_taobao_url)
                                if tmp_taobao_url != []:
                                    goods_id = tmp_taobao_url
                                else:
                                    item = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)').findall(item)[0]
                            else:  # 处理存数据库中取出的如: https://item.taobao.com/item.htm?id=560164926470
                                # print('9999')
                                item = re.compile(r';').sub('', item)
                                goods_id = re.compile(r'https://item.taobao.com/item.htm\?id=(\d+)&{0,20}.*?').findall(item)[0]
                                # print('------>>>| 得到的淘宝商品id为:', goods_id)
                            tmp_goods_id = goods_id
                            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                        else:
                            print('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']             # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']         # 商品地址
                            tmp['username'] = data_list['username']             # 操作人员username
                            # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)

                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time                    # 操作时间

                            tmp['modfiy_time'] = now_time                       # 修改时间

                            tmp['shop_name'] = data_list['shop_name']           # 公司名称
                            tmp['title'] = data_list['title']                   # 商品名称
                            tmp['sub_title'] = data_list['sub_title']           # 商品子标题
                            tmp['link_name'] = ''                               # 卖家姓名
                            tmp['account'] = data_list['account']               # 掌柜名称
                            tmp['month_sell_count'] = data_list['sell_count']   # 月销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []                              # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']     # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')   # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')      # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')              # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')          # 下方div

                            # 采集的来源地
                            tmp['site_id'] = 1      # 采集来源地(淘宝)
                            tmp['is_delete'] = data_list.get('is_delete')    # 逻辑删除, 未删除为0, 删除为1

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                # print(tmp_list)
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_taobao_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# tmall
@app.route('/tmall_data', methods=['POST'])
def get_tmall_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            login_tmall = TmallParse()

            goods_id = login_tmall.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del login_tmall       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
            #####################################################
            if goods_id[0] == 0:        # [0, '1111']
                wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]   # 构造成标准干净的天猫商品地址
            elif goods_id[0] == 1:      # [1, '1111']
                wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
            elif goods_id[0] == 2:      # [2, '1111', 'https://xxxxx']
                wait_to_deal_with_url = str(goods_id[2]) + goods_id[1]
            tmp_result = login_tmall.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del login_tmall
                gc.collect()
                result = json.dumps(result)
                return result

            data = login_tmall.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del login_tmall
                gc.collect()
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
            wait_to_save_data['goods_id'] = goods_id[1]        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del login_tmall       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/tmall_to_save_data', methods=['POST'])
def tmall_to_save_data():
    ## 此处注意保存的类型是天猫(3)，还是天猫超市(4)，还是天猫国际(6)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?').findall(item)
                        if is_tmall_url != []:  # 天猫常规商品
                            tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item)
                            if tmp_tmall_url != []:
                                is_tmp_tmp_tmall_url = re.compile(r'https://detail.tmall.com/item.htm.*?&id=(\d+)&{0,20}.*?').findall(item)
                                if is_tmp_tmp_tmall_url != []:
                                    goods_id = is_tmp_tmp_tmall_url[0]
                                else:
                                    goods_id = tmp_tmall_url[0]
                            else:
                                tmall_url = re.compile(r';').sub('', item)
                                goods_id = re.compile(r'https://detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                            tmp_goods_id = goods_id
                            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                        else:
                            is_tmall_supermarket = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(item)
                            if is_tmall_supermarket != []:  # 天猫超市
                                tmp_tmall_url = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)&.*?').findall(item)
                                if tmp_tmall_url != []:
                                    goods_id = tmp_tmall_url[0]
                                else:
                                    tmall_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
                                tmp_goods_id = goods_id
                                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                            else:
                                is_tmall_hk = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(item)  # 因为中间可能有国家的地址 如https://detail.tmall.hk/hk/item.htm?
                                if is_tmall_hk != []:  # 天猫国际， 地址中有地域的也能正确解析, 嘿嘿 -_-!!!
                                    tmp_tmall_url = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)&.*?').findall(item)
                                    if tmp_tmall_url != []:
                                        goods_id = tmp_tmall_url[0]
                                    else:
                                        tmall_url = re.compile(r';').sub('', item)
                                        goods_id = re.compile(r'https://detail.tmall.hk/.*?item.htm.*?id=(\d+)').findall(tmall_url)[0]
                                    # before_url = re.compile(r'https://detail.tmall.hk/.*?item.htm').findall(item)[0]
                                    tmp_goods_id = goods_id
                                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                                else:       # 非正确的天猫商品url
                                    print('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                                    pass

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username
                            # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time            # 操作时间
                            tmp['modfiy_time'] = now_time               # 修改时间

                            tmp['shop_name'] = data_list['shop_name']   # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']   # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            tmp['month_sell_count'] = data_list['sell_count']  # 月销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            # 采集的来源地
                            if data_list.get('type') == 0:
                                tmp['site_id'] = 3                  # 采集来源地(天猫)
                            elif data_list.get('type') == 1:
                                tmp['site_id'] = 4                  # 采集来源地(天猫超市)
                            elif data_list.get('type') == 2:
                                tmp['site_id'] = 6                  # 采集来源地(天猫国际)
                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_tmall_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# jd
@app.route('/jd_data', methods=['POST'])
def get_jd_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            jd = JdParse()

            goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del jd       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            # 改进判断，根据传入数据判断是京东(京东超市属于其中)，还是京东全球购，还是京东大药房
            #####################################################
            if goods_id[0] == 0:        # [0, '1111']
                wait_to_deal_with_url = 'https://item.jd.com/' + goods_id[1] + '.html'   # 构造成标准干净的淘宝商品地址
            elif goods_id[0] == 1:      # [1, '1111']
                wait_to_deal_with_url = 'https://item.jd.hk/' + goods_id[1] + '.html'
            elif goods_id[0] == 2:      # [2, '1111', 'https://xxxxx']
                wait_to_deal_with_url = 'https://item.yiyaojd.com/' + goods_id[1] + '.html'
            tmp_result = jd.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del jd
                gc.collect()
                result = json.dumps(result)
                return result

            data = jd.deal_with_data(goods_id=goods_id)   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del jd
                gc.collect()
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
            wait_to_save_data['goods_id'] = goods_id[1]        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del jd       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/jd_to_save_data', methods=['POST'])
def jd_to_save_data():
    ## 此处注意保存的类型是京东(7)，还是京东超市(8)，还是京东全球购(9)，还是京东大药房(10)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_jd_url = re.compile(r'https://item.jd.com/.*?').findall(item)
                        if is_jd_url != []:
                            goods_id = re.compile(r'https://item.jd.com/(.*?).html.*?').findall(item)[0]
                            tmp_goods_id = goods_id
                            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                        else:
                            is_jd_hk_url = re.compile(r'https://item.jd.hk/.*?').findall(item)
                            if is_jd_hk_url != []:
                                goods_id = re.compile(r'https://item.jd.hk/(.*?).html.*?').findall(item)[0]
                                tmp_goods_id = goods_id
                                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                            else:
                                is_yiyao_jd_url = re.compile(r'https://item.yiyaojd.com/.*?').findall(item)
                                if is_yiyao_jd_url != []:
                                    goods_id = re.compile(r'https://item.yiyaojd.com/(.*?).html.*?').findall(item)[0]
                                    tmp_goods_id = goods_id
                                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                                else:
                                    print('京东商品url错误, 非正规的url, 请参照格式(https://item.jd.com/)或者(https://item.jd.hk/)开头的...')
                                    pass

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username
                            # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time  # 操作时间
                            tmp['modfiy_time'] = now_time  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']  # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']  # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            tmp['all_sell_count'] = data_list['all_sell_count']  # 总销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            # 采集的来源地
                            if data_list.get('jd_type') == 7:
                                tmp['site_id'] = 7  # 采集来源地(京东)
                            elif data_list.get('jd_type') == 8:
                                tmp['site_id'] = 8  # 采集来源地(京东超市)
                            elif data_list.get('jd_type') == 9:
                                tmp['site_id'] = 9  # 采集来源地(京东全球购)
                            elif data_list.get('jd_type') == 10:
                                tmp['site_id'] = 10 # 采集来源地(京东大药房)

                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_jd_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# 折800
@app.route('/zhe_800_data',  methods=['POST'])
def get_zhe_800_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            zhe_800 = Zhe800Parse()

            goods_id = zhe_800.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del zhe_800       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            #####################################################
            wait_to_deal_with_url = 'https://shop.zhe800.com/products/' + str(goods_id)

            tmp_result = zhe_800.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del zhe_800
                gc.collect()
                result = json.dumps(result)
                return result

            data = zhe_800.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del zhe_800
                gc.collect()
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
            wait_to_save_data['goods_id'] = str(goods_id)        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del zhe_800       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/zhe_800_to_save_data', methods=['POST'])
def zhe_800_to_save_data():
    ## 此处注意保存的类型是折800常规商品(11)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/.*?').findall(item)
                        if is_zhe_800_url != []:
                            if re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(item) != []:
                                tmp_zhe_800_url = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(item)[0]
                                if tmp_zhe_800_url != '':
                                    goods_id = tmp_zhe_800_url
                                else:
                                    zhe_800_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'https://shop.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]
                            else:  # 处理从数据库中取出的数据
                                zhe_800_url = re.compile(r';').sub('', item)
                                goods_id = re.compile(r'https://shop.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                            tmp_goods_id = goods_id
                            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

                        else:
                            is_miao_sha_url = re.compile(r'https://miao.zhe800.com/products/.*?').findall(item)
                            if is_miao_sha_url != []:  # 先不处理这种链接的情况
                                if re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(item) != []:
                                    tmp_zhe_800_url = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(item)[0]
                                    if tmp_zhe_800_url != '':
                                        goods_id = tmp_zhe_800_url
                                    else:
                                        zhe_800_url = re.compile(r';').sub('', item)
                                        goods_id = re.compile(r'https://miao.zhe800.com/products/(.*?)\?.*?').findall(zhe_800_url)[0]

                                else:  # 处理从数据库中取出的数据
                                    zhe_800_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'https://miao.zhe800.com/products/(.*)').findall(zhe_800_url)[0]
                                pass    # 不处理
                            else:
                                print('折800商品url错误, 非正规的url, 请参照格式(https://shop.zhe800.com/products/)开头的...')
                                pass    # 不处理

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username

                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time  # 操作时间
                            tmp['modfiy_time'] = now_time  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']  # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']  # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            # tmp['all_sell_count'] = data_list['all_sell_count']  # 总销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            tmp['schedule'] = data_list.get('schedule')

                            # 采集的来源地
                            tmp['site_id'] = 11  # 采集来源地(折800常规商品)

                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_zhe_800_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# 卷皮
@app.route('/juanpi_data', methods=['POST'])
def get_juanpi_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            juanpi = JuanPiParse()

            goods_id = juanpi.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del juanpi       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            #####################################################
            wait_to_deal_with_url = 'http://shop.juanpi.com/deal/' + str(goods_id)

            tmp_result = juanpi.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del juanpi
                gc.collect()
                result = json.dumps(result)
                return result

            data = juanpi.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del juanpi
                gc.collect()
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
            wait_to_save_data['goods_id'] = str(goods_id)        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del juanpi       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/juanpi_to_save_data', methods=['POST'])
def juanpi_to_save_data():
    ## 此处注意保存的类型是卷皮常规商品(12)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/.*?').findall(item)
                        if is_juanpi_url != []:
                            if re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(item) != []:
                                tmp_juanpi_url = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(item)[0]
                                if tmp_juanpi_url != '':
                                    goods_id = tmp_juanpi_url
                                else:  # 只是为了在pycharm运行时不调到chrome，其实else完全可以不要的
                                    juanpi_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'http://shop.juanpi.com/deal/(\d+).*?').findall(juanpi_url)[0]
                                print('------>>>| 得到的卷皮商品的地址为:', goods_id)
                                tmp_goods_id = goods_id
                                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

                        else:
                            print('卷皮商品url错误, 非正规的url, 请参照格式(http://shop.juanpi.com/deal/)开头的...')
                            pass    # 不处理

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username

                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time  # 操作时间
                            tmp['modfiy_time'] = now_time  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']  # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']  # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            # tmp['all_sell_count'] = data_list['all_sell_count']  # 总销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            tmp['schedule'] = data_list.get('schedule')

                            # 采集的来源地
                            tmp['site_id'] = 12  # 采集来源地(卷皮常规商品)

                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_juanpi_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# 拼多多
@app.route('/pinduoduo_data', methods=['POST'])
def get_pinduoduo_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            pinduoduo = PinduoduoParse()

            goods_id = pinduoduo.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                del pinduoduo       # 每次都回收一下
                gc.collect()
                result = json.dumps(result)
                return result

            #####################################################
            wait_to_deal_with_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)

            tmp_result = pinduoduo.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                del pinduoduo
                gc.collect()
                result = json.dumps(result)
                return result

            data = pinduoduo.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                del pinduoduo
                gc.collect()
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
            wait_to_save_data['goods_id'] = str(goods_id)        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            del pinduoduo       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()

        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/pinduoduo_to_save_data', methods=['POST'])
def pinduoduo_to_save_data():
    ## 此处注意保存的类型是拼多多常规商品(13)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html.*?').findall(item)
                        if is_pinduoduo_url != []:
                            if re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item) != []:
                                tmp_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item)[0]
                                if tmp_pinduoduo_url != '':
                                    goods_id = tmp_pinduoduo_url
                                else:  # 只是为了在pycharm里面测试，可以不加
                                    pinduoduo_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(pinduoduo_url)[0]
                                print('------>>>| 得到的拼多多商品id为:', goods_id)
                                tmp_goods_id = goods_id
                                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                            else:
                                pass
                        else:
                            print('拼多多商品url错误, 非正规的url, 请参照格式(http://mobile.yangkeduo.com/goods.html)开头的...')
                            pass        # 不处理

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username

                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time  # 操作时间
                            tmp['modfiy_time'] = now_time  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']  # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']  # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            tmp['all_sell_count'] = str(data_list['all_sell_count'])  # 总销量

                            # 设置最高价price， 最低价taobao_price
                            tmp['price'] = Decimal(data_list['price']).__round__(2)
                            tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            tmp['schedule'] = data_list.get('schedule')

                            # 采集的来源地
                            tmp['site_id'] = 13  # 采集来源地(卷皮常规商品)

                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError as e:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_pinduoduo_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                del my_page_info_save_item_pipeline
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################
# 唯品会
@app.route('/vip_data', methods=['POST'])
def get_vip_data():
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,     # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            vip = VipParse()

            goods_id = vip.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                try:
                    del vip       # 每次都回收一下
                except Exception:
                    pass
                gc.collect()
                result = json.dumps(result)
                return result

            #####################################################
            wait_to_deal_with_url = 'https://m.vip.com/product-0-' + str(goods_id[1]) + '.html'

            tmp_result = vip.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                }

                try:
                    del vip
                except: pass
                gc.collect()
                result = json.dumps(result)
                return result

            data = vip.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                }

                try: del vip
                except: pass
                gc.collect()
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
            wait_to_save_data['goods_id'] = str(goods_id[1])        # goods_id  官方商品link的商品id

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            print('------>>>| 下面是爬取到的页面信息: ')
            print(result_json.decode())
            print('-------------------------------')

            try: del vip       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            except: pass
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()

        else:       # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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

@app.route('/vip_to_save_data', methods=['POST'])
def vip_to_save_data():
    ## 此处注意保存的类型是唯品会常规商品(25)
    global tmp_wait_to_save_data_list
    if request.cookies.get('username') is not None and request.cookies.get('passwd') is not None:  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            print('获取到的待存取的url的list为: ', wait_to_save_data_url_list)
            if wait_to_save_data_url_list != []:
                tmp_wait_to_save_data_goods_id_list = []
                for item in wait_to_save_data_url_list:
                    if item == '':  # 除去传过来是空值
                        pass
                    else:
                        is_vip_irl = re.compile(r'https://m.vip.com/product-(\d*)-.*?.html.*?').findall(item)
                        if is_vip_irl != []:
                            if re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(item) != []:
                                tmp_vip_url = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(item)[0]
                                if tmp_vip_url != '':
                                    goods_id = tmp_vip_url
                                else:  # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                                    vip_url = re.compile(r';').sub('', item)
                                    goods_id = re.compile(r'https://m.vip.com/product-.*?-(\d+).html.*?').findall(vip_url)[0]
                                print('------>>>| 得到的唯品会商品的goods_id为:', goods_id)
                                tmp_goods_id = goods_id
                                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                            else:
                                pass
                        else:
                            # 唯品会预售商品
                            is_vip_preheading = re.compile(r'https://m.vip.com/preheating-product-(\d+)-.*?.html.*?').findall(item)
                            if is_vip_preheading != []:
                                if re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(item) != []:
                                    tmp_vip_url = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(item)[0]
                                    if tmp_vip_url != '':
                                        goods_id = tmp_vip_url
                                    else:  # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                                        vip_url = re.compile(r';').sub('', item)
                                        goods_id = re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                                    print('------>>>| 得到的唯品会 预售商品 的goods_id为:', goods_id)
                                    tmp_goods_id = goods_id
                                    tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                            else:
                                print('唯品会商品url错误, 非正规的url, 请参照格式(https://m.vip.com/product-0-xxxxxxx.html) or (https://m.vip.com/preheating-product-xxxx-xxxx.html)开头的...')
                                pass    # 不处理

                wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
                print('获取到的待存取的goods_id的list为: ', wait_to_save_data_goods_id_list)

                # list里面的dict去重
                ll_list = []
                [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
                tmp_wait_to_save_data_list = ll_list
                # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

                goods_to_delete = []
                tmp_list = []  # 用来存放筛选出来的数据, 里面一个元素就是一个dict
                for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
                    for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
                        if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                            print('匹配到该goods_id, 其值为: %s' % wait_to_save_data_goods_id)
                            data_list = tmp_wait_to_save_data_list[index]
                            tmp = {}
                            tmp['goods_id'] = data_list['goods_id']  # 官方商品id
                            tmp['spider_url'] = data_list['spider_url']  # 商品地址
                            tmp['username'] = data_list['username']  # 操作人员username

                            '''
                            时区处理，时间处理到上海时间
                            '''
                            tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
                            now_time = datetime.datetime.now(tz)
                            # 处理为精确到秒位，删除时区信息
                            now_time = re.compile(r'\..*').sub('', str(now_time))
                            # 将字符串类型转换为datetime类型
                            now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

                            tmp['deal_with_time'] = now_time  # 操作时间
                            tmp['modfiy_time'] = now_time  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']  # 公司名称
                            tmp['title'] = data_list['title']  # 商品名称
                            tmp['sub_title'] = data_list['sub_title']  # 商品子标题
                            tmp['link_name'] = ''  # 卖家姓名
                            tmp['account'] = data_list['account']  # 掌柜名称
                            tmp['all_sell_count'] = str(data_list['all_sell_count'])  # 总销量

                            # 设置最高价price， 最低价taobao_price
                            if isinstance(data_list['price'], Decimal):
                                tmp['price'] = data_list['price']
                            else:
                                tmp['price'] = Decimal(data_list['price']).__round__(2)
                            if isinstance(data_list['taobao_price'], Decimal):
                                tmp['taobao_price'] = data_list['taobao_price']
                            else:
                                tmp['taobao_price'] = Decimal(data_list['taobao_price']).__round__(2)
                            tmp['price_info'] = []  # 价格信息

                            tmp['detail_name_list'] = data_list['detail_name_list']  # 标签属性名称

                            """
                            得到sku_map
                            """
                            tmp['price_info_list'] = data_list.get('price_info_list')  # 每个规格对应价格及其库存

                            tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

                            tmp['p_info'] = data_list.get('p_info')  # 详细信息
                            tmp['div_desc'] = data_list.get('div_desc')  # 下方div

                            tmp['schedule'] = data_list.get('schedule')

                            # 采集的来源地
                            tmp['site_id'] = 25  # 采集来源地(卷皮常规商品)

                            tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
                            # print('is_delete=', tmp['is_delete'])

                            # print('------>>> | 待存储的数据信息为: |', tmp)
                            print('------>>> | 待存储的数据信息为: |', tmp.get('goods_id'))

                            tmp_list.append(tmp)
                            try:
                                goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                            except IndexError:
                                print('索引越界, 此处我设置为跳过')
                            # tmp_wait_to_save_data_list.pop(index)
                            finally:
                                pass
                        else:
                            pass

                my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                # tmp_list = [dict(t) for t in set([tuple(d.items()) for d in tmp_list])]
                for item in tmp_list:
                    # print('------>>> | 正在存储的数据为: |', item)
                    print('------>>> | 正在存储的数据为: |', item.get('goods_id'))

                    is_insert_into = my_page_info_save_item_pipeline.insert_into_vip_table(item)
                    if is_insert_into:  # 如果返回值为True
                        pass
                    else:
                        # print('插入失败!')
                        pass

                tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
                print('存入完毕'.center(100, '*'))
                try: del my_page_info_save_item_pipeline
                except: pass
                gc.collect()

                # 处理完毕后返回一个处理结果避免报错
                result = {
                    'reason': 'success',
                    'data': '',
                    'error_code': 11,
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

######################################################

@app.route('/basic_data', methods=['POST'])
def get_basic_data():
    '''
    返回一个商品地址的基本信息
    :return: 一个json
    '''
    if request.form.get('basic_app_key') is not None and request.form.get('basic_app_key') == BASIC_APP_KEY:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            print('正在获取相应数据中...')

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                print('goodsLink为空值...')

                result = {
                    'reason': 'error',
                    'data': '',
                    'error_code': 4042,  # 表示goodsLink为空值
                }

                result = json.dumps(result)
                return result

            if re.compile(r'https://item.taobao.com/item.htm.*?').findall(wait_to_deal_with_url) != []:
                basic_taobao = TaoBaoLoginAndParse()

                goods_id = basic_taobao.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id
                if goods_id == '':  # 如果得不到goods_id, 则return error
                    print('获取到的goods_id为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 4042,  # 表示goodsLink为空值
                    }

                    del basic_taobao  # 每次都回收一下
                    gc.collect()
                    result = json.dumps(result)
                    return result

                wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id  # 构造成标准干净的淘宝商品地址
                tmp_result = basic_taobao.get_goods_data(goods_id=goods_id)
                time.sleep(TAOBAO_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
                if tmp_result == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                    }

                    del basic_taobao
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = basic_taobao.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象

                if data == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                    }

                    del basic_taobao
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = {
                    'title': data.get('title'),
                    'price': data.get('taobao_price'),
                    'month_sell_count': data.get('sell_count'),     # 月销量
                    'img_url': [data.get('all_img_url')[0]],
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': goods_id,
                }

                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }

                result_json = json.dumps(result, ensure_ascii=False).encode()
                print('------>>>| 下面是爬取到的页面信息: ')
                print(result_json.decode())
                print('-------------------------------')

                del basic_taobao  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  # 手动回收即可立即释放需要删除的资源
                return result_json.decode()

            if re.compile(r'https://detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
                or re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
                or re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(wait_to_deal_with_url) != []:

                basic_tmall = TmallParse()

                goods_id = basic_tmall.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                if goods_id == []:  # 如果得不到goods_id, 则return error
                    print('获取到的goods_id为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 4042,  # 表示goodsLink为空值
                    }

                    del basic_tmall  # 每次都回收一下
                    gc.collect()
                    result = json.dumps(result)
                    return result

                # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
                #####################################################
                if goods_id[0] == 0:  # [0, '1111']
                    wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]  # 构造成标准干净的淘宝商品地址
                elif goods_id[0] == 1:  # [1, '1111']
                    wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
                elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
                    wait_to_deal_with_url = str(goods_id[2]) + goods_id[1]
                tmp_result = basic_tmall.get_goods_data(goods_id=goods_id)
                if tmp_result == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                    }

                    del basic_tmall
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = basic_tmall.deal_with_data()  # 如果成功获取的话, 返回的是一个data的dict对象

                if data == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                    }

                    del basic_tmall
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = {
                    'title': data.get('title'),
                    'price': data.get('taobao_price'),
                    'month_sell_count': data.get('sell_count'),     # 月销量
                    'img_url': [data.get('all_img_url')[0]],
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': goods_id[1],
                }

                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }

                result_json = json.dumps(result, ensure_ascii=False).encode()
                print('------>>>| 下面是爬取到的页面信息: ')
                print(result_json.decode())
                print('-------------------------------')

                del basic_tmall  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  # 手动回收即可立即释放需要删除的资源
                return result_json.decode()

            if re.compile(r'https://item.jd.com/.*?').findall(wait_to_deal_with_url) != [] \
                or re.compile(r'https://item.jd.hk/.*?').findall(wait_to_deal_with_url) != [] \
                or re.compile(r'https://item.yiyaojd.com/.*?').findall(wait_to_deal_with_url) != []:

                jd = JdParse()

                goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                if goods_id == []:  # 如果得不到goods_id, 则return error
                    print('获取到的goods_id为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 4042,  # 表示goodsLink为空值
                    }

                    del jd  # 每次都回收一下
                    gc.collect()
                    result = json.dumps(result)
                    return result

                # 改进判断，根据传入数据判断是京东(京东超市属于其中)，还是京东全球购，还是京东大药房
                #####################################################
                if goods_id[0] == 0:  # [0, '1111']
                    wait_to_deal_with_url = 'https://item.jd.com/' + goods_id[1] + '.html'  # 构造成标准干净的淘宝商品地址
                elif goods_id[0] == 1:  # [1, '1111']
                    wait_to_deal_with_url = 'https://item.jd.hk/' + goods_id[1] + '.html'
                elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
                    wait_to_deal_with_url = 'https://item.yiyaojd.com/' + goods_id[1] + '.html'
                tmp_result = jd.get_goods_data(goods_id=goods_id)
                if tmp_result == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 333,  # 表示能获取到goods_id，但是待爬取的地址非常规商品的地址，无法正常解析
                    }

                    del jd
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = jd.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象

                if data == {}:
                    print('获取到的data为空!')
                    result = {
                        'reason': 'error',
                        'data': '',
                        'error_code': 444,  # 表示能获取到goods_id，无法正确解析
                    }

                    del jd
                    gc.collect()
                    result = json.dumps(result)
                    return result

                data = {
                    'title': data.get('title'),
                    'price': str(data.get('taobao_price')),
                    'all_sell_count': data.get('all_sell_count'),  # 月销量
                    'img_url': [data.get('all_img_url')[0]],
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': goods_id[1],
                }

                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }

                result_json = json.dumps(result, ensure_ascii=False).encode()
                print('------>>>| 下面是爬取到的页面信息: ')
                print(result_json.decode())
                print('-------------------------------')

                del jd  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  # 手动回收即可立即释放需要删除的资源
                return result_json.decode()

            # 直接把空值给pass，不打印信息
            # print('goodsLink为空值...')
            result = {
                'reason': 'error',
                'data': '',
                'error_code': 4042,  # 表示goodsLink为空值
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
    print('http://0.0.0.0:{}'.format(str(SERVER_PORT),))

    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()      # 采用高并发部署

    # 简单的多线程
    # app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
