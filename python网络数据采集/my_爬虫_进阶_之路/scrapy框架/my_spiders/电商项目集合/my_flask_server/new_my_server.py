# coding:utf-8

'''
@author = super_fazai
@File    : my_server.py
@Time    : 2017/10/13 09:30
@connect : superonesfazai@gmail.com
'''

import sys
import os
TOP_PATH = os.getcwd()
sys.path.append(TOP_PATH)

from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    make_response,
    session,
    Response,
    send_file,
    abort,
)
from flask_login import LoginManager

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
    KAOLA_SPIDER_2_SHOW_PATH,
    YANXUAN_SPIDER_2_SHOW_PATH,
    YOUPIN_SPIDER_2_SHOW_PATH,
    ADMIN_NAME,
    ADMIN_PASSWD,
    SERVER_PORT,
    MY_SPIDER_LOGS_PATH,
    ERROR_HTML_CODE,
    IS_BACKGROUND_RUNNING,
    BASIC_APP_KEY,
    TAOBAO_SLEEP_TIME,
    SELECT_HTML_NAME,
    key,
)

from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
)
from my_signature import Signature
# from apps.search import PostDocument
from apps.admin import (
    find_user_name,
    del_user,
    check_all_user,
    init_passwd,
    admin_add_new_user,)
from apps.msg import (
    _success_data,
    _null_goods_link,
    _invalid_goods_link,
    _null_goods_id,
    _null_goods_data,
    _insert_into_db_result,
    _error_msg,)
from apps.reuse import (
    add_base_info_2_processed_data,
    is_login,)
from apps.url_judge import (
    _is_taobao_url_plus,
    _is_tmall_url,
    _is_tmall_url_plus,
    _is_jd_url,
    _is_jd_url_plus,)
from apps.al import (
    get_one_1688_data,)
from apps.tb import (
    get_one_tb_data,
    _deal_with_tb_goods,)
from apps.tm import (
    _deal_with_tm_goods,
    get_one_tm_data,)
from apps.jd import (
    get_one_jd_data,
    _deal_with_jd_goods,)
from apps.kl import (
    get_one_kaola_data,)
from apps.yx import (
    get_one_yanxuan_data,)
from apps.yp import (
    get_one_youpin_data,)
from apps.save import (
    get_who_wait_to_save_data_goods_id_list,
    get_who_right_data,
    get_db_who_insert_params,)

import hashlib
import json
import time
from time import sleep
import datetime
import re
from logging import (
    INFO,
    ERROR,
)
from pprint import pprint
from base64 import b64decode

try:
    from gevent.wsgi import WSGIServer      # 高并发部署
except Exception as e:
    from gevent.pywsgi import WSGIServer

import gc

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,)
from fzutils.linux_utils import daemon_init
from fzutils.common_utils import json_2_dict
from fzutils.safe_utils import (
    encrypt,
    decrypt,)

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

tmp_wait_to_save_data_list = []

my_lg = set_logger(
    log_file_name=MY_SPIDER_LOGS_PATH + '/my_spiders_server/day_by_day/' + str(get_shanghai_time())[0:10] + '.txt',
    console_log_level=INFO,
    file_log_level=INFO
)

Sign = Signature(logger=my_lg)

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
            # my_lg.info('super_name:{0} super_passwd:{1}'.format(super_name, super_passwd)
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
                response = make_response(redirect('show_taobao'))
                return response

            elif ajax_request == 'tianm_login':
                response = make_response(redirect('show_tmall'))
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

            elif ajax_request == 'kaola_login':
                response = make_response(redirect('show_kaola'))
                return response

            elif ajax_request == 'yanxuan_login':
                response = make_response(redirect('show_yanxuan'))
                return response

            elif ajax_request == 'youpin_login':
                response = make_response(redirect('show_youpin'))
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
                return find_user_name(find_name=find_name, tmp_user=tmp_user, my_lg=my_lg)

            # 重置
            elif request.form.get('update', '') != '':
                update_name = request.form.get('update', '')
                return init_passwd(update_name=update_name, tmp_user=tmp_user, my_lg=my_lg)

            # 删除
            elif request.form.getlist('user_to_delete_list[]') != []:
                user_to_delete_list = list(request.form.getlist('user_to_delete_list[]'))
                return del_user(tmp_user=tmp_user, user_to_delete_list=user_to_delete_list, my_lg=my_lg)

            # 查看现有所有用户数据
            elif request.form.get('check_all_users', '') == 'True':
                my_lg.info('返回所有注册员工信息!')
                return check_all_user(tmp_user=tmp_user, my_lg=my_lg)

            # 注册新用户
            elif request.form.get('username', '') != '':
                admin_add_new_user(request=request, tmp_user=tmp_user, my_lg=my_lg)
                return send_file('templates/admin.html')

            else:
                my_lg.error('来自admin页面中的未知操作!')

        else:
            return send_file('templates/admin.html')       

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
            # return send_file('templates/spider_to_show.html')       
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
            # return send_file('templates/spider_to_show.html')       
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
            # return send_file('templates/spider_to_show.html')       
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

@app.route('/show_kaola', methods=['GET', 'POST'])
def show_kaola_info():
    if not is_login(request=request):
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取考拉页面...')
        if request.method == 'POST':
            pass
        else:
            return send_file(KAOLA_SPIDER_2_SHOW_PATH)

@app.route('/show_yanxuan', methods=['GET', 'POST'])
def show_yanxuan_info():
    if not is_login(request=request):
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取严选页面...')
        if request.method == 'POST':
            pass
        else:
            return send_file(YANXUAN_SPIDER_2_SHOW_PATH)

@app.route('/show_youpin', methods=['GET', 'POST'])
def show_youpin_info():
    if not is_login(request=request):
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取爬取小米有品页面...')
        if request.method == 'POST':
            pass
        else:
            return send_file(YOUPIN_SPIDER_2_SHOW_PATH)

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

            wait_to_save_data = get_one_1688_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()  
            msg = '阿里1688抓取数据成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

            wait_to_save_data = get_one_tb_data(username=username, tb_url=wait_to_deal_with_url, my_lg=my_lg)
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()
            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()
            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '淘宝抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

            wait_to_save_data = get_one_tm_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '天猫抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

######################################################
# 京东
@app.route('/jd_data', methods=['POST'])
def get_jd_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username', ''))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            wait_to_save_data = get_one_jd_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '京东抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list))
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

######################################################
# 折800
@app.route('/zhe_800_data',  methods=['POST'])
def get_zhe_800_data():
    if is_login(request=request):
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')

                return _null_goods_link()

            zhe_800 = Zhe800Parse()
            goods_id = zhe_800.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del zhe_800       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'https://shop.zhe800.com/products/' + str(goods_id)

            tmp_result = zhe_800.get_goods_data(goods_id=goods_id)
            data = zhe_800.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del zhe_800
                gc.collect()

                return _null_goods_data()

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            try: del zhe_800  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            except: pass
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '折800抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/zhe_800_to_save_data', methods=['POST'])
def zhe_800_to_save_data():
    ## 此处注意保存的类型是折800常规商品(11)
    global tmp_wait_to_save_data_list
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
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

######################################################
# 卷皮
@app.route('/juanpi_data', methods=['POST'])
def get_juanpi_data():
    if is_login(request=request):
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')

                return _null_goods_link()

            juanpi = JuanPiParse()

            goods_id = juanpi.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del juanpi       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://shop.juanpi.com/deal/' + str(goods_id)
            tmp_result = juanpi.get_goods_data(goods_id=goods_id)
            data = juanpi.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del juanpi
                gc.collect()

                return _null_goods_data()

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )
            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            try: del juanpi  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            except: pass
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '卷皮抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/juanpi_to_save_data', methods=['POST'])
def juanpi_to_save_data():
    ## 此处注意保存的类型是卷皮常规商品(12)
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
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

######################################################
# 拼多多
@app.route('/pinduoduo_data', methods=['POST'])
def get_pinduoduo_data():
    if is_login(request=request):
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')

            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')

                return _null_goods_link()

            pinduoduo = PinduoduoParse()
            goods_id = pinduoduo.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == '':      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                del pinduoduo       # 每次都回收一下
                gc.collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)
            tmp_result = pinduoduo.get_goods_data(goods_id=goods_id)
            data = pinduoduo.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del pinduoduo
                gc.collect()

                return _null_goods_data()

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id
            )
            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            try: del pinduoduo  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            except: pass
            gc.collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '拼多多抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/pinduoduo_to_save_data', methods=['POST'])
def pinduoduo_to_save_data():
    ## 此处注意保存的类型是拼多多常规商品(13)
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
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

######################################################
# 唯品会
@app.route('/vip_data', methods=['POST'])
def get_vip_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取vip相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            vip = VipParse()
            goods_id = vip.get_goods_id_from_url(wait_to_deal_with_url)   # 获取goods_id, 这里返回的是一个list
            if goods_id == []:      # 如果得不到goods_id, 则return error
                my_lg.info('获取到的goods_id为空!')
                try:
                    del vip       # 每次都回收一下
                except Exception:
                    pass
                gc.collect()
                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'https://m.vip.com/product-0-' + str(goods_id[1]) + '.html'

            tmp_result = vip.get_goods_data(goods_id=goods_id)
            data = vip.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                try:
                    del vip
                except: pass
                gc.collect()
                return _null_goods_data()

            wait_to_save_data = add_base_info_2_processed_data(
                data=data,
                spider_url=wait_to_deal_with_url,
                username=username,
                goods_id=goods_id[1]
            )
            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            try: del vip       # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
            except: pass
            gc.collect()        

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '唯品会抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/vip_to_save_data', methods=['POST'])
def vip_to_save_data():
    ## 此处注意保存的类型是唯品会常规商品(25)
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
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

######################################################
# 网易考拉海购
@app.route('/kaola_data', methods=['POST'])
def get_kaola_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取kaola相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            wait_to_save_data = get_one_kaola_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()

            my_lg.info('------>>>| 下面是爬取到的考拉页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '网易考拉抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/kaola_to_save_data', methods=['POST'])
def kaola_to_save_data():
    # 考拉site_id=29
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='kaola',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='kaola',
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
    
######################################################
# 网易严选
@app.route('/yanxuan_data', methods=['POST'])
def get_yanxuan_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取yanxuan相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            wait_to_save_data = get_one_yanxuan_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()

            my_lg.info('------>>>| 下面是爬取到的严选页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '网易严选抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/yanxuan_to_save_data', methods=['POST'])
def yanxuan_to_save_data():
    # 严选site_id=30
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='yanxuan',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='yanxuan',
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

######################################################
# 小米有品
@app.route('/youpin_data', methods=['POST'])
def get_youpin_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取youpin相应数据中...')

            # 解密
            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            wait_to_save_data = get_one_youpin_data(
                username=username,
                wait_to_deal_with_url=wait_to_deal_with_url,
                my_lg=my_lg
            )
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            gc.collect()

            my_lg.info('------>>>| 下面是爬取到的有品页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '小米有品抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

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

@app.route('/youpin_to_save_data', methods=['POST'])
def youpin_to_save_data():
    # 小米有品site_id=31
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='youpin',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )
                sql_str = 'insert into dbo.GoodsInfoAutoGet(GoodsID, GoodsUrl, UserName, CreateTime, ModfiyTime, ShopName, Account, GoodsName, SubTitle, LinkName, Price, TaoBaoPrice, PriceInfo, SKUName, SKUInfo, ImageUrl, PropertyInfo, DetailInfo, SellCount, Schedule, SiteID, IsDelete) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                return save_every_url_right_data(
                    type='youpin',
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

            if _is_taobao_url_plus(wait_to_deal_with_url):
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
                my_lg.info('------>>>| 下面是爬取到的页面信息: ')
                my_lg.info(str(result_json.decode()))
                my_lg.info('-------------------------------')

                del basic_taobao  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  

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
                gc.collect()  
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
                my_lg.info('------>>>| 下面是爬取到的页面信息: ')
                my_lg.info(str(result_json.decode()))
                my_lg.info('-------------------------------')

                del jd  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                gc.collect()  
                return result_json.decode()

            else:
                # 直接把空值给pass，不打印信息
                # my_lg.info('goodsLink为空值...')
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
    _ = get_goods_link(request=request)
    goods_link = b64decode(s=_.encode('utf-8')).decode('utf-8')     # _ 传来的起初是str, 先str->byte, 再b64decode解码

    if goods_link != '':
        my_lg.info('正在获取相应数据中...')
        my_lg.info('获取到的goods_link：' + str(goods_link))

        if _is_taobao_url_plus(goods_link):
            my_lg.info('该link为淘宝link...')

            return _deal_with_tb_goods(goods_link=goods_link, my_lg=my_lg)

        elif _is_tmall_url_plus(goods_link):
            my_lg.info('该link为天猫link...')

            return _deal_with_tm_goods(goods_link=goods_link, my_lg=my_lg)

        elif _is_jd_url_plus(goods_link):
            my_lg.info('该link为京东link...')

            return _deal_with_jd_goods(goods_link=goods_link, my_lg=my_lg)

        else:
            my_lg.info('无效的goods_link!')
            return _invalid_goods_link()

    else:
        my_lg.info('goods_link为空值!')

        return _null_goods_link()

def get_goods_link(**kwargs):
    '''
    从cli得到goods_link(只支持get, post)
    :param kwargs:
    :return:
    '''
    request = kwargs.get('request')

    # my_lg.info(dict(request.args))
    _ = ''
    if request.method == 'GET':
        try:
            _ = dict(request.args).get('goods_link', '')[0]
        except IndexError:
            my_lg.error('获取goods_link时IndexError!')

    else:
        _ = request.form.get('goods_link', '')

    return _

######################################################
# wechat
@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    echo_str = dict(request.args).get('echostr', '')
    
    return echo_str

######################################################
# search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if is_login(request=request):
        s = request.args.get('s')
        if s:
            posts = [{'id':1},]
        else:
            posts = ''

        return send_file('templates/search.html')
    else:
        return ERROR_HTML_CODE

######################################################
# 从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]
def get_tmp_list_and_goods_2_delete_list(**kwargs):
    '''
    从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]
    :param kwargs:
    :return:
    '''
    global tmp_wait_to_save_data_list

    type = kwargs.get('type')  # 三方商品类型
    wait_to_save_data_url_list = kwargs.get('wait_to_save_data_url_list')  # client发来的待存储的url_list

    tmp_wait_to_save_data_goods_id_list = get_who_wait_to_save_data_goods_id_list(
        type=type,
        wait_to_save_data_url_list=wait_to_save_data_url_list,
        my_lg=my_lg
    )

    wait_to_save_data_goods_id_list = list(set(tmp_wait_to_save_data_goods_id_list))  # 待保存的goods_id的list
    my_lg.info('获取到的待存取的goods_id的list为: {0}'.format(str(wait_to_save_data_goods_id_list)))

    # list里面的dict去重
    ll_list = []
    [ll_list.append(x) for x in tmp_wait_to_save_data_list if x not in ll_list]
    tmp_wait_to_save_data_list = ll_list
    # my_lg.info('所有待存储的数据: {0}'.format(str(tmp_wait_to_save_data_list)))

    goods_to_delete = []
    tmp_list = []  # 用来存放筛选出来的数据, eg: [{}, ...]
    for wait_to_save_data_goods_id in wait_to_save_data_goods_id_list:
        for index in range(0, len(tmp_wait_to_save_data_list)):  # 先用set去重, 再转为list
            if wait_to_save_data_goods_id == tmp_wait_to_save_data_list[index]['goods_id']:
                my_lg.info('匹配到该goods_id, 其值为: {0}'.format(wait_to_save_data_goods_id))
                data_list = tmp_wait_to_save_data_list[index]

                tmp = get_who_right_data(
                    type=type,
                    data_list=data_list,
                    my_lg=my_lg
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
    my_lg.info('========主函数开始========')
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    my_lg.info('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == "__main__":
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
