# coding:utf-8

'''
@author = super_fazai
@File    : my_server.py
@Time    : 2017/10/13 09:30
@connect : superonesfazai@gmail.com
'''

import sys, os
sys.path.append(os.getcwd())

from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    make_response,
    session,
    jsonify,
    Response,
    send_file,
    abort,
)
from flask_login import LoginManager

from ali_1688_parse import ALi1688LoginAndParse
from taobao_parse import TaoBaoLoginAndParse
# from tmall_parse import TmallParse
from tmall_parse_2 import TmallParse
from jd_parse import JdParse
from zhe_800_parse import Zhe800Parse
from juanpi_parse import JuanPiParse
from pinduoduo_parse import PinduoduoParse
from vip_parse import VipParse

from settings import (
    ALi_SPIDER_TO_SHOW_PATH,
    TAOBAO_SPIDER_TO_SHWO_PATH,
    TMALL_SPIDER_TO_SHOW_PATH,
    JD_SPIDER_TO_SHOW_PATH,
    ZHE_800_SPIDER_TO_SHOW_PATH,
    JUANPI_SPIDER_TO_SHOW_PATH,
    PINDUODUO_SPIDER_TO_SHOW_PATH,
    VIP_SPIDER_TO_SHOW_PATH,
    ADMIN_NAME,
    ADMIN_PASSWD,
    SERVER_PORT,
    MY_SPIDER_LOGS_PATH,
    TMALL_SLEEP_TIME,
    ERROR_HTML_CODE,
    IS_BACKGROUND_RUNNING,
    BASIC_APP_KEY,
    TAOBAO_SLEEP_TIME,
    SELECT_HTML_NAME,
    INIT_PASSWD,
)

from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
)
from my_logging import set_logger
from my_utils import (
    get_shanghai_time,
    daemon_init,
)
from my_items import GoodsItem
from my_signature import Signature

import hashlib
import json
import time
from time import sleep
import datetime
import re
from decimal import Decimal
from logging import (
    INFO,
    ERROR,
)
from json import dumps
from pprint import pprint

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
app.secret_key = 'fjusfbubvnighwwf#%&'  # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单

# 内部员工口令
inner_pass = 'adminss'

# key 用于加密
key = 21

tmp_wait_to_save_data_list = []

my_lg = set_logger(
    log_file_name=MY_SPIDER_LOGS_PATH + '/my_spiders_server/day_by_day/' + str(get_shanghai_time())[0:10] + '.txt',
    console_log_level=INFO,
    file_log_level=ERROR
)

Sign = Signature()

# server数据插入失败 -> 运行此sql_str
error_insert_sql_str = '''
select UserName, CreateTime, GoodsID, GoodsName, ConvertTime, MainGoodsID
from dbo.GoodsInfoAutoGet 
where GoodsID=%s
'''

# saveData[]为空的msg
save_data_null_msg = 'saveData为空! <br/><br/>可能是抓取后, 重复点存入数据按钮导致!<br/><br/>** 请按正常流程操作:<br/>先抓取，后存入，才有相应抓取后存储信息的展示!<br/><br/>^_^!!!  感谢使用!!!'

######################################################

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') is not None and request.form.get('passwd') is not None:
            username = str(request.form.get('username', ''))
            passwd = str(request.form.get('passwd', ''))
            my_lg.info(str(username) + ' : ' + str(passwd))
        else:
            username, passwd = ('', '',)

        if request.form.get('superUser', '') != '' and request.form.get('superPass', '') != '':
            super_name = str(request.form.get('superUser', ''))
            super_passwd = str(request.form.get('superPass', ''))
            # print('super_name:', super_name, ' ', 'super_passwd:', super_passwd)
        else:
            super_name, super_passwd = ('', '',)

        if super_name == ADMIN_NAME and super_passwd == ADMIN_PASSWD:   # 先判断是否为admin，如果是转向管理员管理界面
            my_lg.info('超级管理员密码匹配正确')
            response = make_response(redirect('admin'))    # 重定向到新的页面

            # 加密
            has_super_name = encrypt(key, super_name)
            has_super_passwd = encrypt(key, super_passwd)

            outdate = datetime.datetime.today() + datetime.timedelta(days=1)

            response.set_cookie('super_name', value=has_super_name, max_age=60 * 60 * 5, expires=outdate)  # 延长过期时间(1天)
            response.set_cookie('super_passwd', value=has_super_passwd, max_age=60 * 60 * 5, expires=outdate)
            return response

        else:                   # 否则为普通用户，进入选择页面
            tmp_user = SqlServerMyPageInfoSaveItemPipeline()
            sql_str = 'select username from dbo.ali_spider_employee_table where username = %s and passwd = %s'
            is_have_user = tmp_user._select_table(sql_str=sql_str, params=(username, passwd,))

            if is_have_user is not None and is_have_user != []:
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
                my_lg.info('登录失败!请重新登录')
                return redirect('/')

    else:
        return render_template('login.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    my_lg.info('正在获取选择界面...')
    if is_login(request=request):   # 判断是否为非法登录
        if request.form.get('confirm_login'):       # 根据ajax请求类型的分别处理
            ajax_request = request.form.get('confirm_login')
            if ajax_request == 'ali_login':
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
    # my_lg.info('正在获取登录界面...')
    if request.cookies.get('super_name', '') == encrypt(key, ADMIN_NAME) and request.cookies.get('super_passwd', '') == encrypt(key, ADMIN_PASSWD):   # 判断是否为非法登录
        if request.method == 'POST':
            tmp_user = SqlServerMyPageInfoSaveItemPipeline()

            # 查找
            if request.form.get('find_name', '') != '':
                find_name = request.form.get('find_name', '')

                return find_user_name(find_name=find_name, tmp_user=tmp_user)

            # 重置
            elif request.form.get('update', '') != '':
                update_name = request.form.get('update', '')

                return init_passwd(update_name=update_name, tmp_user=tmp_user)

            # 删除
            elif request.form.getlist('user_to_delete_list[]') != []:
                user_to_delete_list = list(request.form.getlist('user_to_delete_list[]'))

                return del_user(tmp_user=tmp_user, user_to_delete_list=user_to_delete_list)

            # 查看现有所有用户数据
            elif request.form.get('check_all_users', '') == 'True':
                my_lg.info('返回所有注册员工信息!')

                return check_all_user(tmp_user=tmp_user)

            # 注册新用户
            elif request.form.get('username', '') != '':
                admin_add_new_user(request=request, tmp_user=tmp_user)

                return send_file('templates/admin.html')

            else:
                my_lg.error('来自admin页面中的未知操作!')

        else:
            return send_file('templates/admin.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件

    else:   # 非法登录显示错误网页
        return ERROR_HTML_CODE

@app.route('/Reg', methods=['GET', 'POST'])
def register():
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
            tmp_user = SqlServerMyPageInfoSaveItemPipeline()
            create_time = get_shanghai_time()

            item = (
                str(username),
                str(passwd),
                create_time,
                str(department),
                str(real_name),
            )
            sql_str = 'insert into dbo.ali_spider_employee_table(username, passwd, createtime, department, realnane) values(%s, %s, %s, %s, %s)'
            is_insert_into = tmp_user._insert_into_table_2(sql_str=sql_str, params=item, logger=my_lg)

            if is_insert_into:
                my_lg.info('用户 %s 注册成功!' % str(username))
                return redirect('/')
            else:
                return "用户注册失败!"

        else:       # 输入员工口令错误
            return "内部员工口令错误, 请返回重新注册!"

    else:
        return render_template('Reg.html')

######################################################
# admin相关操作func

def find_user_name(**kwargs):
    '''
    查找
    :param kwargs:
    :return:
    '''
    find_name = kwargs.get('find_name', '')
    tmp_user = kwargs.get('tmp_user')

    if len(find_name) == 11 and re.compile(r'^1').findall(find_name) != []:  # 根据手机号查找
        sql_str = 'select * from dbo.ali_spider_employee_table where username=%s'
        result = tmp_user._select_table(sql_str=sql_str, params=(find_name,))
        if result is not None and result != []:
            my_lg.info('查找成功!')
            result = result[0]
            # print(result)     # 只返回的是一个list 如: ['15661611306', 'xxxx', datetime.datetime(2017, 10, 13, 10, 0), '杭州', 'xxx']
            data = [{
                'username': result[0],
                'passwd': encrypt(key, result[1]),
                'createtime': str(result[2]),  # datetime类型转换为字符串 .strftime('%Y-%m-%d %H:%M:%S')
                'department': result[3],
                'realnane': result[4],
            }]
            result = {
                'reason': 'success',
                'data': data,
                'error_code': 1,
            }
            result = json.dumps(result, ensure_ascii=False).encode()
            return result.decode()

        else:
            my_lg.info('查找失败!')
            result = {
                'reason': 'error',
                'data': [],
                'error_code': 0,  # 表示goodsLink为空值
            }
            result = json.dumps(result)
            return result

    elif len(find_name) > 1 and len(find_name) <= 4:  # 根据用户名查找
        sql_str = 'select * from dbo.ali_spider_employee_table where realnane=%s'
        result = tmp_user._select_table(sql_str=sql_str, params=(find_name,))
        # my_lg.info(str(result))
        if result is not None and result != []:
            my_lg.info('查找成功!')
            data = [{
                'username': item[0],
                'passwd': encrypt(key, item[1]),
                'createtime': str(item[2]),
                'department': item[3],
                'realnane': item[4]
            } for item in result]
            result = {
                'reason': 'success',
                'data': data,
                'error_code': 1,
            }
            result = json.dumps(result, ensure_ascii=False).encode()
            return result.decode()

        else:
            my_lg.info('查找失败!')
            result = {
                'reason': 'error',
                'data': [],
                'error_code': 0,  # 表示goodsLink为空值
            }

            result = json.dumps(result)
            return result
    else:
        my_lg.info('find_name非法!')
        result = {
            'reason': 'error',
            'data': [],
            'error_code': 0,  # 表示goodsLink为空值
        }
        result = json.dumps(result)
        return result

def init_passwd(**kwargs):
    '''
    重置用户密码
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')
    update_name = kwargs.get('update_name', '')

    sql_str = 'update dbo.ali_spider_employee_table set passwd=%s where username=%s'
    result = tmp_user._update_table_2(sql_str=sql_str, params=(INIT_PASSWD, update_name), logger=my_lg)
    if result:
        my_lg.info('重置密码成功!')

    else:
        my_lg.error('重置密码失败!')

    # 返回所有数据
    return check_all_user(tmp_user=tmp_user)

def del_user(**kwargs):
    '''
    删除用户
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')
    user_to_delete_list = kwargs.get('user_to_delete_list')

    sql_str = 'delete from dbo.ali_spider_employee_table where username=%s'
    for item in user_to_delete_list:
        tmp_user._delete_table(sql_str=sql_str, params=(item,))

    my_lg.info('删除操作执行成功!')

    return check_all_user(tmp_user=tmp_user)

def check_all_user(**kwargs):
    '''
    查看现有所有用户数据
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')

    sql_str = 'select * from dbo.ali_spider_employee_table'
    result = tmp_user._select_table(sql_str=sql_str) if tmp_user._select_table(sql_str=sql_str) is not None else []
    data = [{
        'username': item[0],
        'passwd': encrypt(key, item[1]),
        'createtime': str(item[2]),
        'department': item[3],
        'realnane': item[4]
    } for item in result]

    result = {
        'reason': 'success',
        'data': data,
        'error_code': 1,
    }
    result = json.dumps(result, ensure_ascii=False).encode()

    return result.decode()

def admin_add_new_user(**kwargs):
    '''
    在admin页面add new user
    :param kwargs:
    :return:
    '''
    request = kwargs.get('request')
    tmp_user = kwargs.get('tmp_user')

    username = request.form.get('username', '')
    passwd = request.form.get('passwd', '')

    real_name = request.form.get('ralenane', '')
    department = request.form.get('department', '')

    create_time = get_shanghai_time()

    item = (
        str(username),
        str(passwd),
        create_time,
        str(department),
        str(real_name),
    )
    sql_str = 'insert into dbo.ali_spider_employee_table(username, passwd, createtime, department, realnane) values(%s, %s, %s, %s, %s)'
    is_insert_into = tmp_user._insert_into_table_2(sql_str=sql_str, params=item, logger=my_lg)

    if is_insert_into:
        my_lg.info('用户 %s 注册成功!' % str(username))
    else:
        my_lg.info("用户注册失败!")

    return

######################################################

@app.route('/show_ali', methods=['GET', 'POST'])
def show_ali_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if not is_login(request=request):
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):
        return ERROR_HTML_CODE

    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
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
    if not is_login(request=request):  # request.cookies -> return a dict
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            return send_file(VIP_SPIDER_TO_SHOW_PATH)

######################################################
# 阿里1688
@app.route("/data", methods=['POST'])
def get_all_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: %s' % str(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                tmp_item = re.compile(r'(.*?)\?.*?').findall(goodsLink)  # 过滤筛选出唯一的阿里1688商品链接
                if tmp_item == []:
                    wait_to_deal_with_url = goodsLink
                else:
                    wait_to_deal_with_url = tmp_item[0]
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            login_ali = ALi1688LoginAndParse()
            goods_id = login_ali.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id
            if goods_id == '':      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del login_ali  # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            tmp_result = login_ali.get_ali_1688_data(goods_id=goods_id)
            if tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del login_ali
                gc.collect()

                return _null_goods_data()

            data = login_ali.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {}:
                my_lg.info('获取到的data为空!')
                del login_ali
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            tmp_goods_id = re.compile(r'.*?/offer/(.*?).html').findall(wait_to_deal_with_url)[0]

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=tmp_goods_id
            )

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
            return _null_goods_link()

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
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):      # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))   # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='ali',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, GoodsName, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, DetailInfo, PropertyInfo, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='ali',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_ali_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

    tmp_wait_to_save_data_goods_id_list = []
    for item in wait_to_save_data_url_list:
        if item == '':  # 除去传过来是空值
            pass
        else:
            tmp_goods_id = re.compile(r'.*?/offer/(.*?).html.*?').findall(item)[0]
            tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)

    return tmp_wait_to_save_data_goods_id_list

def _get_ali_right_data(data):
    '''
    得到规范格式的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = GoodsItem()
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

    tmp['shop_name'] = data_list['company_name']  # 公司名称
    tmp['title'] = data_list['title']  # 商品名称
    tmp['link_name'] = data_list['link_name']  # 卖家姓名

    tmp['price'] = Decimal(data_list.get('price')).__round__(2)
    tmp['taobao_price'] = Decimal(data_list.get('taobao_price')).__round__(2)
    tmp['price_info'] = data_list['price_info']  # 价格信息

    spec_name = []
    for item in data_list['sku_props']:
        tmp_dic = {}
        tmp_dic['spec_name'] = item.get('prop')
        spec_name.append(tmp_dic)

    tmp['detail_name_list'] = spec_name  # 标签属性名称

    """
    得到sku_map
    """
    tmp['price_info_list'] = data_list.get('sku_map')  # 每个规格对应价格及其库存

    tmp['all_img_url'] = data_list.get('all_img_url')  # 所有示例图片地址

    tmp['p_info'] = data_list.get('property_info')  # 详细信息
    tmp['div_desc'] = data_list.get('detail_info')  # 下方div

    # 采集的来源地
    tmp['site_id'] = 2  # 采集来源地(阿里1688批发市场)
    tmp['is_delete'] = 0  # 逻辑删除, 未删除为0, 删除为1

    return tmp

def _get_db_ali_insert_params(item):
    '''
    得到阿里待插入的数据
    :param item:
    :return: tuple
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['detail_name_list'], ensure_ascii=False),
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        item['div_desc'],  # 存入到DetailInfo
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 淘宝
@app.route('/taobao_data', methods=['POST'])
def get_taobao_data():
    global my_lg
    if is_login(request=request):
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username', ''))
            my_lg.info('发起获取请求的员工的username为: %s' % str(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            login_taobao = TaoBaoLoginAndParse(logger=my_lg)
            goods_id = login_taobao.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id
            if goods_id == '':      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del login_taobao  # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id   # 构造成标准干净的淘宝商品地址
            tmp_result = login_taobao.get_goods_data(goods_id=goods_id)
            time.sleep(TAOBAO_SLEEP_TIME)     # 这个在服务器里面可以注释掉为.5s
            if tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del login_taobao
                gc.collect()

                return _null_goods_data()

            data = login_taobao.deal_with_data(goods_id=goods_id)   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {}:
                my_lg.info('获取到的data为空!')
                del login_taobao
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(result_json.decode()))
            my_lg.info('-------------------------------')

            del login_taobao       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # my_lg.info('goodsLink为空值...')
            return _null_goods_link()
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
    global tmp_wait_to_save_data_list, my_lg
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            msg = '获取到的待存取的url的list为: ' + str(wait_to_save_data_url_list)
            my_lg.info(msg)
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='taobao',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='taobao',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_taobao_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

    tmp_wait_to_save_data_goods_id_list = []
    for item in wait_to_save_data_url_list:
        if item == '':  # 除去传过来是空值
            pass
        else:
            is_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?').findall(item)
            if is_taobao_url != []:
                if re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item) != []:
                    tmp_taobao_url = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)&{0,20}.*?').findall(item)[0]
                    # my_lg.info(tmp_taobao_url)
                    if tmp_taobao_url != []:
                        goods_id = tmp_taobao_url
                    else:
                        item = re.compile(r';').sub('', item)
                        goods_id = re.compile(r'https://item.taobao.com/item.htm.*?id=(\d+)').findall(item)[0]
                else:  # 处理存数据库中取出的如: https://item.taobao.com/item.htm?id=560164926470
                    # my_lg.info('9999')
                    item = re.compile(r';').sub('', item)
                    goods_id = re.compile(r'https://item.taobao.com/item.htm\?id=(\d+)&{0,20}.*?').findall(item)[0]
                    # my_lg.info('------>>>| 得到的淘宝商品id为:' + goods_id)
                tmp_goods_id = goods_id
                tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
            else:
                my_lg.info('淘宝商品url错误, 非正规的url, 请参照格式(https://item.taobao.com/item.htm)开头的...')

    return tmp_wait_to_save_data_goods_id_list

def _get_taobao_right_data(data):
    '''
    得到规范格式的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

    tmp['shop_name'] = data_list['shop_name']  # 公司名称
    tmp['title'] = data_list['title']  # 商品名称
    tmp['sub_title'] = data_list['sub_title']  # 商品子标题
    tmp['link_name'] = ''  # 卖家姓名
    tmp['account'] = data_list['account']  # 掌柜名称
    tmp['all_sell_count'] = data_list['sell_count']  # 月销量

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
    tmp['site_id'] = 1  # 采集来源地(淘宝)
    tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1

    return tmp

def _get_db_taobao_insert_params(item):
    '''
    得到db待插入的数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],

        item['site_id'],
        item['is_delete'],
    )

    return params

def _get_m_taobao_goods_id(goods_link):
    '''
    获取m站的goods_id
    :param goods_link:
    :return:
    '''
    try:
        return re.compile(r'id=(\d+)').findall(goods_link)[0]
    except IndexError:
        return ''

def _deal_with_taobao_goods(goods_link):
    '''
    处理淘宝商品
    :param goods_link:
    :return: dict
    '''
    goods_id = _get_m_taobao_goods_id(goods_link)
    if goods_id == '':
        return {'goods_id': ''}

    taobao = TaoBaoLoginAndParse(logger=my_lg)
    wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id  # 构造成标准干净的淘宝商品地址
    tmp_result = taobao.get_goods_data(goods_id=goods_id)
    data = taobao.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象
    # time.sleep(TAOBAO_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
    if tmp_result == {} or data == {}:
        del taobao
        gc.collect()
        return {
            'goods_id': goods_id,
            'data': {},
        }

    data.update({
        'goods_id': goods_id,
        'spider_url': wait_to_deal_with_url,
        'username': '18698570079',
    })

    data = _get_taobao_right_data(data)
    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    my_lg.info('------>>>| 正在存储的数据为: ' + data.get('goods_id', ''))

    params = _get_db_taobao_insert_params(item=data)
    sql_str = r'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    is_insert_into = my_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=my_lg)
    if is_insert_into:  # 如果返回值为True
        pass
    else:
        pass

    '''返回给APP时, 避免json.dumps转换失败...'''
    data['price'] = float(data['price'])
    data['taobao_price'] = float(data['taobao_price'])

    return data

######################################################
# 天猫
@app.route('/tmall_data', methods=['POST'])
def get_tmall_data():
    if is_login(request=request):
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')

                return _null_goods_link()

            login_tmall = TmallParse(logger=my_lg)
            goods_id = login_tmall.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del login_tmall       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
            #####################################################
            if goods_id[0] == 0:        # [0, '1111']
                wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]   # 构造成标准干净的天猫商品地址
            elif goods_id[0] == 1:      # [1, '1111']
                wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
            elif goods_id[0] == 2:      # [2, '1111', 'https://xxxxx']
                wait_to_deal_with_url = str(goods_id[2]) + '?id=' + goods_id[1]
            tmp_result = login_tmall.get_goods_data(goods_id=goods_id)
            time.sleep(TMALL_SLEEP_TIME)     # 这个在服务器里面可以注释掉为.5s
            if tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del login_tmall
                gc.collect()

                return _null_goods_data()

            data = login_tmall.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {}:
                my_lg.info('获取到的data为空!')
                del login_tmall
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id[1]
            )

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果

            result_json = json.dumps(result, ensure_ascii=False).encode()
            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(result_json.decode()))
            my_lg.info('-------------------------------')

            del login_tmall       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            gc.collect()        # 手动回收即可立即释放需要删除的资源
            return result_json.decode()
        else:       # 直接把空值给pass，不打印信息
            # my_lg.info('goodsLink为空值...')
            return _null_goods_link()
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
    '''
    ## 此处注意保存的类型是天猫(3)，还是天猫超市(4)，还是天猫国际(6)
    :return:
    '''
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]   # 过滤'\n'
            # my_lg.info('缓存中待存储url的list为: %s' % str(tmp_wait_to_save_data_list))
            my_lg.info('获取到的待存取的url的list为: %s' % str(wait_to_save_data_url_list))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='tmall',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='tmall',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg=msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(msg=save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_tmall_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

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
                        goods_id = \
                        re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?id=(\d+)').findall(tmall_url)[0]
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
                    else:  # 非正确的天猫商品url
                        my_lg.info('天猫商品url错误, 非正规的url, 请参照格式(https://detail.tmall.com/item.htm)开头的...')
                        pass

    return tmp_wait_to_save_data_goods_id_list

def _get_tmall_right_data(data):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

    tmp['shop_name'] = data_list['shop_name']  # 公司名称
    tmp['title'] = data_list['title']  # 商品名称
    tmp['sub_title'] = data_list['sub_title']  # 商品子标题
    tmp['link_name'] = ''  # 卖家姓名
    tmp['account'] = data_list['account']  # 掌柜名称
    tmp['all_sell_count'] = data_list['sell_count']  # 月销量

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
        tmp['site_id'] = 3  # 采集来源地(天猫)
    elif data_list.get('type') == 1:
        tmp['site_id'] = 4  # 采集来源地(天猫超市)
    elif data_list.get('type') == 2:
        tmp['site_id'] = 6  # 采集来源地(天猫国际)
    tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
    # my_lg.info('is_delete=%s' % str(tmp['is_delete']))

    return tmp

def _get_db_tmall_insert_params(item):
    '''
    得到tmall待存储数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 京东
@app.route('/jd_data', methods=['POST'])
def get_jd_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            print('发起获取请求的员工的username为: %s' % username)

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')

                return _null_goods_link()

            jd = JdParse()
            goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                del jd       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

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

                del jd
                gc.collect()
                return _null_goods_data()

            data = jd.deal_with_data(goods_id=goods_id)   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {}:
                print('获取到的data为空!')
                del jd
                gc.collect()
                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id[1]
            )

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
            return _null_goods_link()

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
    '''
    ## 此处注意保存的类型是京东(7)，还是京东超市(8)，还是京东全球购(9)，还是京东大药房(10)
    :return:
    '''
    global tmp_wait_to_save_data_list
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='jd',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='jd',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_jd_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

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

    return tmp_wait_to_save_data_goods_id_list

def _get_jd_right_data(data):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

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
        tmp['site_id'] = 10  # 采集来源地(京东大药房)

    tmp['is_delete'] = data_list.get('is_delete')  # 逻辑删除, 未删除为0, 删除为1
    # print('is_delete=', tmp['is_delete'])

    return tmp

def _get_db_jd_insert_params(item):
    '''
    得到db待插入数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 折800
@app.route('/zhe_800_data',  methods=['POST'])
def get_zhe_800_data():
    if is_login(request=request):
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

                return _null_goods_link()

            zhe_800 = Zhe800Parse()

            goods_id = zhe_800.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                del zhe_800       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'https://shop.zhe800.com/products/' + str(goods_id)

            tmp_result = zhe_800.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                del zhe_800
                gc.collect()

                return _null_goods_data()

            data = zhe_800.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                del zhe_800
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )

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
            return _null_goods_link()
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
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='zhe_800',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='zhe_800',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_zhe_800_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

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
                    pass  # 不处理
                else:
                    print('折800商品url错误, 非正规的url, 请参照格式(https://shop.zhe800.com/products/)开头的...')
                    pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_zhe_800_right_data(data):
    '''
    得到规范化数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

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

    return tmp

def _get_db_zhe_800_insert_params(item):
    '''
    得到db待插入的数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 卷皮
@app.route('/juanpi_data', methods=['POST'])
def get_juanpi_data():
    if is_login(request=request):
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

                return _null_goods_link()

            juanpi = JuanPiParse()

            goods_id = juanpi.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')

                del juanpi       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://shop.juanpi.com/deal/' + str(goods_id)

            tmp_result = juanpi.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')

                del juanpi
                gc.collect()

                return _null_goods_data()

            data = juanpi.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                my_lg.info('获取到的data为空!')
                del juanpi
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )

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
            return _null_goods_link()
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
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='juanpi',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='juanpi',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_juanpi_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

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
                pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_juanpi_right_data(data):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

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

    return tmp

def _get_db_juanpi_insert_params(item):
    '''
    得到db待插入数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 拼多多
@app.route('/pinduoduo_data', methods=['POST'])
def get_pinduoduo_data():
    if is_login(request=request):
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

                return _null_goods_link()

            pinduoduo = PinduoduoParse()
            goods_id = pinduoduo.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                del pinduoduo       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)
            tmp_result = pinduoduo.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                del pinduoduo
                gc.collect()

                return _null_goods_data()

            data = pinduoduo.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {}:
                print('获取到的data为空!')
                del pinduoduo
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )

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
            return _null_goods_link()

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
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='pinduoduo',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='pinduoduo',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_pinduoduo_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

    tmp_wait_to_save_data_goods_id_list = []
    for item in wait_to_save_data_url_list:
        if item == '':  # 除去传过来是空值
            pass
        else:
            is_pinduoduo_url = re.compile(r'http://mobile.yangkeduo.com/goods.html.*?').findall(item)
            if is_pinduoduo_url != []:
                if re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item) != []:
                    tmp_pinduoduo_url = \
                    re.compile(r'http://mobile.yangkeduo.com/goods.html\?.*?goods_id=(\d+).*?').findall(item)[0]
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
                pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_pinduoduo_right_data(data):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data

    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

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

    return tmp

def _get_db_pinduoduo_insert_params(item):
    '''
    得到db待插入的数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################
# 唯品会
@app.route('/vip_data', methods=['POST'])
def get_vip_data():
    if is_login(request=request):  # request.cookies -> return a dict
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
                return _null_goods_link()

            vip = VipParse()
            goods_id = vip.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                print('获取到的goods_id为空!')
                try:
                    del vip       # 每次都回收一下
                except Exception:
                    pass
                gc.collect()
                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'https://m.vip.com/product-0-' + str(goods_id[1]) + '.html'

            tmp_result = vip.get_goods_data(goods_id=goods_id)
            if tmp_result == {}:
                print('获取到的data为空!')
                try:
                    del vip
                except: pass
                gc.collect()
                return _null_goods_data()

            data = vip.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {}:
                print('获取到的data为空!')
                try: del vip
                except: pass
                gc.collect()

                return _null_goods_data()

            result = {
                'reason': 'success',
                'data': data,
                'error_code': 0,
            }

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id[1]
            )

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
            return _null_goods_link()

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
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # print('缓存中待存储url的list为: ', tmp_wait_to_save_data_list)
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='vip',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='vip',
                    tmp_list=tmp_list,
                    sql_str=sql_str,
                    goods_to_delete=goods_to_delete
                )

            else:
                msg = 'saveData为空!'
                my_lg.info(msg)
                return _error_msg(msg)
        else:
            my_lg.info(save_data_null_msg)
            return _error_msg(save_data_null_msg)

    else:
        return _error_msg(msg='')

def _get_vip_wait_to_save_data_goods_id_list(data):
    '''
    得到待存取的goods_id的list
    :param data:
    :return:
    '''
    wait_to_save_data_url_list = data

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
                        tmp_vip_url = \
                        re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(item)[0]
                        if tmp_vip_url != '':
                            goods_id = tmp_vip_url
                        else:  # 只是为了在pycharm运行时不跳到chrome，其实else完全可以不要的
                            vip_url = re.compile(r';').sub('', item)
                            goods_id = \
                            re.compile(r'https://m.vip.com/preheating-product-.*?-(\d+).html.*?').findall(vip_url)[0]
                        print('------>>>| 得到的唯品会 预售商品 的goods_id为:', goods_id)
                        tmp_goods_id = goods_id
                        tmp_wait_to_save_data_goods_id_list.append(tmp_goods_id)
                else:
                    print('唯品会商品url错误, 非正规的url, 请参照格式(https://m.vip.com/product-0-xxxxxxx.html) or (https://m.vip.com/preheating-product-xxxx-xxxx.html)开头的...')
                    pass  # 不处理

    return tmp_wait_to_save_data_goods_id_list

def _get_vip_right_data(data):
    '''
    得到规范化的数据
    :param data:
    :return:
    '''
    data_list = data
    tmp = {}
    tmp['goods_id'] = data_list['goods_id']  # 官方商品id
    tmp['goods_url'] = data_list['spider_url']  # 商品地址
    tmp['username'] = data_list['username']  # 操作人员username

    now_time = get_shanghai_time()
    tmp['create_time'] = now_time  # 操作时间
    tmp['modify_time'] = now_time  # 修改时间

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

    return tmp

def _get_db_vip_insert_params(item):
    '''
    得到db待插入数据
    :param item:
    :return:
    '''
    params = (
        item['goods_id'],
        item['goods_url'],
        item['username'],
        item['create_time'],
        item['modify_time'],
        item['shop_name'],
        item['account'],
        item['title'],
        item['sub_title'],
        item['link_name'],
        item['price'],
        item['taobao_price'],
        dumps(item['price_info'], ensure_ascii=False),
        dumps(item['detail_name_list'], ensure_ascii=False),  # 把list转换为json才能正常插入数据(并设置ensure_ascii=False)
        dumps(item['price_info_list'], ensure_ascii=False),
        dumps(item['all_img_url'], ensure_ascii=False),
        dumps(item['p_info'], ensure_ascii=False),  # 存入到PropertyInfo
        item['div_desc'],  # 存入到DetailInfo
        item['all_sell_count'],
        dumps(item['schedule'], ensure_ascii=False),

        item['site_id'],
        item['is_delete'],
    )

    return params

######################################################

@app.route('/basic_data', methods=['POST'])
def get_basic_data():
    '''
    返回一个商品地址的基本信息
    :return: 一个json
    '''
    if request.form.get('basic_app_key') is not None and request.form.get('basic_app_key') == BASIC_APP_KEY:  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            goodsLink = request.form.get('goodsLink')
            wait_to_deal_with_url = goodsLink

            if _is_taobao_url(wait_to_deal_with_url):
                basic_taobao = TaoBaoLoginAndParse(logger=my_lg)

                goods_id = basic_taobao.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id
                if goods_id == '':  # 如果得不到goods_id, 则return error
                    my_lg.info('获取到的goods_id为空!')
                    del basic_taobao  # 每次都回收一下
                    gc.collect()

                    return _null_goods_id()

                wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id  # 构造成标准干净的淘宝商品地址
                tmp_result = basic_taobao.get_goods_data(goods_id=goods_id)
                data = basic_taobao.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象
                time.sleep(TAOBAO_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
                if tmp_result == {} or data == {}:
                    my_lg.info('获取到的data为空!')
                    del basic_taobao
                    gc.collect()

                    return _null_goods_data()

                data = {
                    'title': data.get('title'),
                    'price': data.get('taobao_price'),
                    'month_sell_count': data.get('sell_count'),     # 月销量
                    'img_url': data.get('all_img_url'),
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

            elif _is_tmall_url(wait_to_deal_with_url):
                basic_tmall = TmallParse(logger=my_lg)

                goods_id = basic_tmall.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                if goods_id == []:  # 如果得不到goods_id, 则return error
                    my_lg.info('获取到的goods_id为空!')
                    del basic_tmall  # 每次都回收一下
                    gc.collect()

                    return _null_goods_id()

                # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
                #####################################################
                if goods_id[0] == 0:  # [0, '1111']
                    wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]  # 构造成标准干净的淘宝商品地址
                elif goods_id[0] == 1:  # [1, '1111']
                    wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
                elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
                    wait_to_deal_with_url = str(goods_id[2]) + '?id=' + goods_id[1]
                tmp_result = basic_tmall.get_goods_data(goods_id=goods_id)
                if tmp_result == {}:
                    my_lg.info('获取到的data为空!')
                    del basic_tmall
                    gc.collect()

                    return _null_goods_data()

                data = basic_tmall.deal_with_data()  # 如果成功获取的话, 返回的是一个data的dict对象
                if data == {}:
                    my_lg.info('获取到的data为空!')
                    del basic_tmall
                    gc.collect()

                    return _null_goods_data()

                data = {
                    'title': data.get('title'),
                    'price': data.get('taobao_price'),
                    'month_sell_count': data.get('sell_count'),     # 月销量
                    'img_url': data.get('all_img_url'),
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': goods_id[1],
                }

                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }

                result_json = json.dumps(result, ensure_ascii=False).encode()
                my_lg.info('------>>>| 下面是爬取到的页面信息: ')
                my_lg.info(str(result_json.decode()))
                my_lg.info('-------------------------------')

                del basic_tmall  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  # 手动回收即可立即释放需要删除的资源
                return result_json.decode()

            elif _is_jd_url(wait_to_deal_with_url):
                jd = JdParse()

                goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                if goods_id == []:  # 如果得不到goods_id, 则return error
                    my_lg.info('获取到的goods_id为空!')
                    del jd  # 每次都回收一下
                    gc.collect()

                    return _null_goods_id()

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
                    my_lg.info('获取到的data为空!')
                    del jd
                    gc.collect()

                    return _null_goods_data()

                data = jd.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象
                if data == {}:
                    my_lg.info('获取到的data为空!')
                    del jd
                    gc.collect()

                    return _null_goods_data()

                data = {
                    'title': data.get('title'),
                    'price': str(data.get('taobao_price')),
                    'all_sell_count': data.get('all_sell_count'),  # 月销量
                    'img_url': data.get('all_img_url'),
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

            else:
                # 直接把空值给pass，不打印信息
                # print('goodsLink为空值...')
                return _null_goods_link()

        else:
            my_lg.info('goodsLink为空值...')
            return _null_goods_link()

    else:
        return json.dumps({
            'reason': 'error',
            'data': '',
            'error_code': 0,
        })

@app.route('/basic_data_2', methods=['GET', 'POST'])
@Sign.signature_required
def _get_basic_data_2():
    # 正确请求将返回以下内容，否则将被signature_required拦截，返回请求验证信息： {"msg": "Invaild message", "success": False}
    return json.dumps({'ping':"pong"})

######################################################
'''
/api/goods
'''
@app.route('/api/goods', methods=['GET', 'POST'])
@Sign.signature_required
def _goods():
    # print(request.args)
    if request.method == 'GET':
        # print(dict(request.args))
        try:
            goods_link = dict(request.args).get('goods_link', [])[0]
        except IndexError:
            goods_link = None
    else:
        goods_link = request.form.get('goods_link')
    if goods_link:
        my_lg.info('正在获取相应数据中...')
        my_lg.info('获取到的goods_link：' + str(goods_link))

        if _is_m_taobao_url(goods_link):
            my_lg.info('该link为淘宝link...')
            result = _deal_with_taobao_goods(goods_link=goods_link)
            if result.get('goods_id', '') == '':
                my_lg.error('获取到的goods_id为空值!')
                return _null_goods_id()

            elif result.get('data', {}) == {}:
                my_lg.error('获取到的goods_data为空!')
                return _null_goods_data()

            else:
                my_lg.info('获取goods_data success!!')
                return _success_goods_data(result)

        elif _is_m_tmall_url(goods_link):
            pass

        elif _is_m_jd_url(goods_link):
            pass

        else:
            my_lg.info('无效的goods_link!')
            return _invalid_goods_link()

    else:
        my_lg.info('goods_link为空值!')

        return _null_goods_link()

######################################################
'''错误处理/成功处理'''

def _success_goods_data(data):
    # 获取数据成功时的操作
    return dumps({
        'reason': 'success',
        'msg': '成功!',
        'data': data,
        'error_code': '0000',
    }, ensure_ascii=False).encode().decode()

def _null_goods_link():
    # 空goods_link
    return dumps({
        'reason': 'error',
        'msg': 'goods_link为空值!',
        'data': '',
        'error_code': '0001',
    })

def _invalid_goods_link():
    # 无效goods_link
    return dumps({
        'reason': 'error',
        'msg': '无效的goods_link, 请检查!',
        'data': '',
        'error_code': '0002',
    })

def _null_goods_id():
    # 空goods_id
    return dumps({
        'reason': 'error',
        'msg': '获取到的goods_id为空str, 无效的goods_link, 请检查!',
        'data': '',
        'error_code': '0003',
    })

def _null_goods_data():
    # 获取到的goods_data为{}
    return dumps({
        'reason': 'error',
        'msg': '获取到的goods_data为空dict!',
        'data': '',
        'error_code': '0004',
    })

def _insert_into_db_result(**kwargs):
    '''
    抓取后数据储存处理结果, msg显示
    :param pipeline:
    :param is_inserted_and_goods_id_list: a list eg: [('db插入结果类型bool', '对应goods_id'), ...]
    :return:
    '''
    pipeline = kwargs.get('pipeline')
    is_inserted_and_goods_id_list = kwargs.get('is_inserted_and_goods_id_list', [])

    msg = ''
    goods_id_list = [item[1] for item in is_inserted_and_goods_id_list if not item[0]]
    error_goods_id_msg_list = []  # 早期已被存入db的 [('goods_id', 'msg'), ...]

    if goods_id_list != []:     # 处理早期被存入的goods_id
        _e = error_insert_sql_str
        _e += ' or GoodsID=%s ' * (len(goods_id_list)-1)
        _ = pipeline._select_table(sql_str=_e, params=tuple(goods_id_list))
        if _ is None or _ == []:        # 查询失败处理!
            msg = r'执行搜索对应商品语句时出错! 可能已被入录! 请在公司后台对应查询!<br/><br/>'
            for _u in goods_id_list:
                msg += r'官方GoodsID: {0}<br/>'.format(_u)

            return dumps({
                'reason': 'error',
                'msg': msg,
                'data': '',
                'error_code': '0005',
            })

        for goods_id in goods_id_list:
            for _r in _:
                if goods_id == _r[2]:
                    tmp_msg = r'这个商品原先已被存入db中! 相关信息如下:<br/>操作人员: {0}<br/>创建时间: {1}<br/>官方GoodsID: {2}<br/>商品名称: {3}<br/>转换时间: {4}<br/>优秀商品ID: {5}<br/><br/>'.format(
                        _r[0], str(_r[1]), _r[2], _r[3], str(_r[4]) if _r[4] is not None else '未转换', _r[5] if _r[5] is not None else '未转换',
                    )
                    error_goods_id_msg_list.append((goods_id, tmp_msg))
    else:
        pass

    for _i in is_inserted_and_goods_id_list:
        goods_id = _i[1]
        if _i[0]:
            msg += r'新采集的商品[GoodsID={0}]已存入db中!<br/><br/>'.format(goods_id)
        else:
            for _m in error_goods_id_msg_list:
                if goods_id == _m[0]:
                    msg += _m[1]
    my_lg.info(msg)

    return dumps({
        'reason': 'success',
        'msg': msg,
        'data': '',
        'error_code': '0006',
    })

def _error_msg(msg):
    '''
    错误的msg, json返回
    :param msg:
    :return:
    '''
    return dumps({
        'reason': 'error',
        'msg': str(msg),
        'data': '',
        'error_code': '0007',
    })

######################################################
# wechat

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    echo_str = dict(request.args).get('echostr', '')
    
    return echo_str

######################################################

def _is_taobao_url(wait_to_deal_with_url):
    '''
    判断是否为淘宝的链接
    :param wait_to_deal_with_url:
    :return: bool
    '''
    _ = False
    if re.compile(r'https://item.taobao.com/item.htm.*?').findall(wait_to_deal_with_url) != []:
        _ = True

    return _

def _is_m_taobao_url(goods_link):
    '''
    淘宝m站
    :param goods_link:
    :return:
    '''
    if re.compile(r'https://h5.m.taobao.com/awp/core/detail.htm.*?').findall(goods_link) != []:
        return True

    return False

def _is_tmall_url(wait_to_deal_with_url):
    '''
    判断是否为tmall的url
    :param wait_to_deal_with_url:
    :return: bool
    '''
    _ = False
    if re.compile(r'https://detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://chaoshi.detail.tmall.com/item.htm.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://detail.tmall.hk/.*?item.htm.*?').findall(wait_to_deal_with_url) != []:
        _ = True

    return _

def _is_m_tmall_url(goods_link):
    '''
    天猫m站
    :param goods_link:
    :return:
    '''
    pass

def _is_jd_url(wait_to_deal_with_url):
    '''
    判断是否为jd的url
    :param wait_to_deal_with_url:
    :return: bool
    '''
    _ = False
    if re.compile(r'https://item.jd.com/.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://item.jd.hk/.*?').findall(wait_to_deal_with_url) != [] \
         or re.compile(r'https://item.yiyaojd.com/.*?').findall(wait_to_deal_with_url) != []:
        _ = True

    return _

def _is_m_jd_url(goods_link):
    '''
    京东m站
    :param goods_link:
    :return:
    '''
    pass

######################################################
# 从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]

def get_who_wait_to_save_data_goods_id_list(**kwargs):
    '''
    对应得到wait_to_save_data_goods_id_list
    :param kwargs:
    :return: a list
    '''
    type = kwargs.get('type')
    data = kwargs.get('wait_to_save_data_url_list')

    if type == 'ali':
        return _get_ali_wait_to_save_data_goods_id_list(data=data)

    elif type == 'taobao':
        return _get_taobao_wait_to_save_data_goods_id_list(data=data)

    elif type == 'tmall':
        return _get_tmall_wait_to_save_data_goods_id_list(data=data)

    elif type == 'jd':
        return _get_jd_wait_to_save_data_goods_id_list(data=data)

    elif type == 'zhe_800':
        return _get_zhe_800_wait_to_save_data_goods_id_list(data=data)

    elif type == 'juanpi':
        return _get_juanpi_wait_to_save_data_goods_id_list(data=data)

    elif type == 'pinduoduo':
        return _get_pinduoduo_wait_to_save_data_goods_id_list(data=data)

    elif type == 'vip':
        return _get_vip_wait_to_save_data_goods_id_list(data=data)

    else:
        return []

def get_who_right_data(**kwargs):
    '''
    对应得到right_data
    :param kwargs:
    :return:
    '''
    type = kwargs.get('type')
    data = kwargs.get('data_list')

    if type == 'ali':
        return _get_ali_right_data(data=data)

    elif type == 'taobao':
        return _get_taobao_right_data(data=data)

    elif type == 'tmall':
        return _get_tmall_right_data(data=data)

    elif type == 'jd':
        return _get_jd_right_data(data=data)

    elif type == 'zhe_800':
        return _get_zhe_800_right_data(data=data)

    elif type == 'juanpi':
        return _get_juanpi_right_data(data=data)

    elif type == 'pinduoduo':
        return _get_pinduoduo_right_data(data=data)

    elif type == 'vip':
        return _get_vip_right_data(data=data)

    else:
        return {}

def get_tmp_list_and_goods_2_delete_list(**kwargs):
    '''
    从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]
    :param kwargs:
    :return:
    '''
    global tmp_wait_to_save_data_list

    type = kwargs.get('type')   # 三方商品类型
    wait_to_save_data_url_list = kwargs.get('wait_to_save_data_url_list')   # client发来的待存储的url_list

    tmp_wait_to_save_data_goods_id_list = get_who_wait_to_save_data_goods_id_list(
        type=type,
        wait_to_save_data_url_list=wait_to_save_data_url_list
    )

    wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
    my_lg.info('获取到的待存取的goods_id的list为: {0}'.format(str(wait_to_save_data_goods_id_list)))

    # list里面的dict去重
    ll_list = []
    [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
    tmp_wait_to_save_data_list = ll_list
    # print('所有待存储的数据: ', tmp_wait_to_save_data_list)

    goods_to_delete = []
    tmp_list = []  # 用来存放筛选出来的数据, eg: [{}, ...]
    for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
        for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
            if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                my_lg.info('匹配到该goods_id, 其值为: {0}'.format(wait_to_save_data_goods_id))
                data_list = tmp_wait_to_save_data_list[index]

                tmp = get_who_right_data(
                    type=type,
                    data_list=data_list
                )

                # my_lg.info('------>>>| 待存储的数据信息为: {0}'.format(str(tmp)))
                my_lg.info('------>>>| 待存储的数据信息为: {0}'.format(tmp.get('goods_id')))

                tmp_list.append(tmp)
                try:
                    goods_to_delete.append(tmp_wait_to_save_data_list[index])  # 避免在遍历时进行删除，会报错，所以建临时数组
                except IndexError:
                    my_lg.info('索引越界, 此处我设置为跳过')
                # tmp_wait_to_save_data_list.pop(index)
                finally:
                    pass
            else:
                pass

    return tmp_list, goods_to_delete

######################################################
# save every url's right data

def get_db_who_insert_params(type, item):
    '''
    返回用哪个get_db_who_insert_params处理数据
    :param type:
    :return: params
    '''
    if type == 'ali':
        params = _get_db_ali_insert_params(item=item)

    elif type == 'taobao':
        params = _get_db_taobao_insert_params(item=item)

    elif type == 'tmall':
        params = _get_db_tmall_insert_params(item=item)

    elif type == 'jd':
        params = _get_db_jd_insert_params(item=item)

    elif type == 'zhe_800':
        params = _get_db_zhe_800_insert_params(item=item)

    elif type == 'juanpi':
        params = _get_db_juanpi_insert_params(item=item)

    elif type == 'pinduoduo':
        params = _get_db_pinduoduo_insert_params(item=item)

    elif type == 'vip':
        params = _get_db_vip_insert_params(item=item)

    else:
        params = {}

    return params

def save_every_url_right_data(**kwargs):
    '''
    存储处理后的每一个url的数据
    :param kwargs:
    :return: a json msg
    '''
    global tmp_wait_to_save_data_list

    tmp_list = kwargs.get('tmp_list')
    type = kwargs.get('type')
    sql_str = kwargs.get('sql_str')
    goods_to_delete = kwargs.get('goods_to_delete')

    my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    # 存储['db插入结果类型bool', '对应goods_id']
    is_inserted_and_goods_id_list = []
    for item in tmp_list:
        # my_lg.info('------>>> | 正在存储的数据为: %s|', str(item))
        my_lg.info('------>>>| 正在存储的数据为: {0}'.format(str(item.get('goods_id'))))

        params = get_db_who_insert_params(type=type, item=item)
        is_insert_into = my_page_info_save_item_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=my_lg)

        is_inserted_and_goods_id_list.append((is_insert_into, str(item.get('goods_id'))))

    tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
    my_lg.info('存入完毕'.center(100, '*'))
    # del my_page_info_save_item_pipeline
    gc.collect()

    return _insert_into_db_result(
        pipeline=my_page_info_save_item_pipeline,
        is_inserted_and_goods_id_list=is_inserted_and_goods_id_list
    )

######################################################
# high reuse(高复用code)

def add_base_info_2_processed_data(**kwargs):
    '''
    给采集后的data增加基础信息
    :param kwargs:
    :return:
    '''
    data = kwargs.get('data')
    spider_url = kwargs.get('spider_url')
    username = kwargs.get('username')
    goods_id = str(kwargs.get('goods_id'))

    wait_to_save_data = data
    wait_to_save_data['spider_url'] = spider_url
    wait_to_save_data['username'] = username
    wait_to_save_data['goods_id'] = goods_id

    return wait_to_save_data

def is_login(**kwargs):
    '''
    判断是否合法登录
    :param kwargs:
    :return: bool
    '''
    request = kwargs.get('request')

    if request.cookies.get('username') is not None \
            and request.cookies.get('passwd') is not None:   # request.cookies -> return a dict
        return True
    else:
        return False

######################################################

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

def just_fuck_run():
    my_lg.info('服务器已经启动...等待接入中...')
    my_lg.info('http://0.0.0.0:{0}'.format(str(SERVER_PORT), ))

    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

    # 简单的多线程
    # app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == "__main__":
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
