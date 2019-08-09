# coding:utf-8

"""
@author = super_fazai
@File    : my_server.py
@Time    : 2017/10/13 09:30
@connect : superonesfazai@gmail.com
"""

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
from tmall_parse_2 import TmallParse
from jd_parse import JdParse
from zhe_800_parse import Zhe800Parse
from juanpi_parse import JuanPiParse
from pinduoduo_parse import PinduoduoParse
from vip_parse import VipParse

from settings import *
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,)
from my_signature import Signature
# from apps.search import PostDocument
from apps.admin import *
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
    get_one_1688_data,
    judge_begin_greater_than_1,)
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
from apps.mi import (
    get_one_mia_data,)
from apps.save import (
    get_who_wait_to_save_data_goods_id_list,
    get_who_right_data,
    get_db_who_insert_params,)

import time
import datetime
from logging import (
    INFO,
    ERROR,
)
from base64 import b64decode
from threading import Lock as ThreadingLock
from threading import Thread
from queue import Queue

try:
    # 高并发部署
    from gevent.wsgi import WSGIServer
except Exception as e:
    from gevent.pywsgi import WSGIServer

from sql_str_controller import (
    fz_al_insert_str,
    fz_tb_insert_str,
    fz_tm_insert_str,
    fz_jd_insert_str,
    fz_z8_insert_str,
    fz_jp_insert_str,
    fz_pd_insert_str,
    fz_vi_insert_str,
    fz_kl_insert_str,
    fz_yx_insert_str,
    fz_yp_insert_str,
    fz_mi_insert_str,
    tm_select_str_3,
    tb_select_str_3,
)

from article_spider import ArticleParser
from buyiju_spider import BuYiJuSpider

from fzutils.log_utils import set_logger
from fzutils.exceptions import catch_exceptions
from fzutils.data.json_utils import get_new_list_by_handle_list_2_json_error
from fzutils.spider.async_always import *

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
    logger_name=get_uuid1(),
    log_file_name=MY_SPIDER_LOGS_PATH + '/my_spiders_server/day_by_day/' + str(get_shanghai_time())[0:10] + '.txt',
    console_log_level=INFO,
    file_log_level=INFO,)
Sign = Signature(logger=my_lg)

# saveData[]为空的msg
save_data_null_msg = 'saveData为空! <br/><br/>可能是抓取后, 重复点存入数据按钮导致!<br/><br/>** 请按正常流程操作:<br/>先抓取，后存入，才有相应抓取后存储信息的展示!<br/><br/>^_^!!!  感谢使用!!!'

######################################################
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        passwd = request.form.get('passwd', '')
        super_name = request.form.get('superUser', '')
        super_passwd = request.form.get('superPass', '')
        my_lg.info('{}: {}'.format(username, passwd))
        # my_lg.info('super_name:{0} super_passwd:{1}'.format(super_name, super_passwd)

        if super_name == ADMIN_NAME and super_passwd == ADMIN_PASSWD:
            # 先判断是否为admin，如果是转向管理员管理界面
            my_lg.info('超级管理员密码匹配正确')
            # 重定向到新的页面
            response = make_response(redirect('admin'))

            # 加密
            has_super_name = encrypt(key, super_name)
            has_super_passwd = encrypt(key, super_passwd)

            outdate = datetime.datetime.today() + datetime.timedelta(days=1)
            # 延长过期时间(1天)
            response.set_cookie('super_name', value=has_super_name, max_age=60 * 60 * 5, expires=outdate)
            response.set_cookie('super_passwd', value=has_super_passwd, max_age=60 * 60 * 5, expires=outdate)

            return response

        else:
            # 普通用户
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
                    # session['islogin'] = '1'        # 设置session的话会有访问的时间限制, 故我不设置
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
            my_lg.info(ajax_request)
            if ajax_request == 'ali_login':
                return make_response(redirect('show_ali'))

            elif ajax_request == 'taob_login':
                return make_response(redirect('show_taobao'))

            elif ajax_request == 'tianm_login':
                return make_response(redirect('show_tmall'))

            elif ajax_request == 'jd_login':
                return make_response(redirect('show_jd'))

            elif ajax_request == 'zhe_800_login':
                return make_response(redirect('show_zhe_800'))

            elif ajax_request == 'juanpi_login':
                return make_response(redirect('show_juanpi'))

            elif ajax_request == 'pinduoduo_login':
                return make_response(redirect('show_pinduoduo'))

            elif ajax_request == 'vip_login':
                return make_response(redirect('show_vip'))

            elif ajax_request == 'kaola_login':
                return make_response(redirect('show_kaola'))

            elif ajax_request == 'yanxuan_login':
                return make_response(redirect('show_yanxuan'))

            elif ajax_request == 'youpin_login':
                return make_response(redirect('show_youpin'))

            elif ajax_request == 'mia_login':
                return make_response(redirect('show_mia'))

            else:
                return ERROR_HTML_CODE
        else:
            return render_template(SELECT_HTML_NAME)

    else:   # 非法登录显示错误网页
        return ERROR_HTML_CODE

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    管理员页面
    :return:
    """
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
    """
    注册新用户页面
    :return:
    """
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
def handle_someone_show_page_res(short_name: str, request):
    """
    处理路由'/show_xxx'的结果
    :param short_name:
    :param request:
    :return:
    """
    if short_name == 'al':
        show_path = ALi_SPIDER_TO_SHOW_PATH
    elif short_name == 'tb':
        show_path = TAOBAO_SPIDER_TO_SHWO_PATH
    elif short_name == 'tm':
        show_path = TMALL_SPIDER_TO_SHOW_PATH
    elif short_name == 'jd':
        show_path = JD_SPIDER_TO_SHOW_PATH
    elif short_name == 'z8':
        show_path = ZHE_800_SPIDER_TO_SHOW_PATH
    elif short_name == 'jp':
        show_path = JUANPI_SPIDER_TO_SHOW_PATH
    elif short_name == 'pd':
        show_path = PINDUODUO_SPIDER_TO_SHOW_PATH
    elif short_name == 'vip':
        show_path = VIP_SPIDER_TO_SHOW_PATH
    elif short_name == 'kl':
        show_path = KAOLA_SPIDER_2_SHOW_PATH
    elif short_name == 'yx':
        show_path = YANXUAN_SPIDER_2_SHOW_PATH
    elif short_name == 'yp':
        show_path = YOUPIN_SPIDER_2_SHOW_PATH
    elif short_name == 'mia':
        show_path = MIA_SPIDER_2_SHOW_PATH
    else:
        raise ValueError('short_name value 异常!')

    if not is_login(request=request):
        return ERROR_HTML_CODE
    else:
        my_lg.info('正在获取{}爬取页面...'.format(short_name))
        if request.method == 'POST':
            # 让前端发个post请求, 重置页面
            pass
        else:
            return send_file(show_path)

@app.route('/show_ali', methods=['GET', 'POST'])
def show_al_info():
    return handle_someone_show_page_res(
        short_name='al',
        request=request,)

@app.route('/show_taobao', methods=['GET', 'POST'])
def show_tb_info():
    return handle_someone_show_page_res(
        short_name='tb',
        request=request, )

@app.route('/show_tmall', methods=['GET', 'POST'])
def show_tm_info():
    return handle_someone_show_page_res(
        short_name='tm',
        request=request, )

@app.route('/show_jd', methods=['GET', 'POST'])
def show_jd_info():
    return handle_someone_show_page_res(
        short_name='jd',
        request=request, )

@app.route('/show_zhe_800', methods=['GET', 'POST'])
def show_z8_info():
    return handle_someone_show_page_res(
        short_name='z8',
        request=request, )

@app.route('/show_juanpi', methods=['GET', 'POST'])
def show_jp_info():
    return handle_someone_show_page_res(
        short_name='jp',
        request=request, )

@app.route('/show_pinduoduo', methods=['GET', 'POST'])
def show_pd_info():
    return handle_someone_show_page_res(
        short_name='pd',
        request=request, )

@app.route('/show_vip', methods=['GET', 'POST'])
def show_vip_info():
    return handle_someone_show_page_res(
        short_name='vip',
        request=request, )

@app.route('/show_kaola', methods=['GET', 'POST'])
def show_kl_info():
    return handle_someone_show_page_res(
        short_name='kl',
        request=request, )

@app.route('/show_yanxuan', methods=['GET', 'POST'])
def show_yx_info():
    return handle_someone_show_page_res(
        short_name='yx',
        request=request, )

@app.route('/show_youpin', methods=['GET', 'POST'])
def show_yp_info():
    return handle_someone_show_page_res(
        short_name='yp',
        request=request, )

@app.route('/show_mia', methods=['GET', 'POST'])
def show_mia_info():
    return handle_someone_show_page_res(
        short_name='mia',
        request=request, )

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
                my_lg=my_lg)
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()

            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()

            else:
                pass

            begin_greater_than_1 = judge_begin_greater_than_1(price_info=wait_to_save_data.get('price_info', []), logger=my_lg)
            if begin_greater_than_1:
                return _error_msg(msg='采集的1688商品的最小起批量, 不能大于1!!')

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            collect()  
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
        result = dumps(result)
        return result

@app.route('/to_save_data', methods=['POST'])
def to_save_data():
    """
    存储请求存入的每个url对应的信息
    :return:
    """
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

                return save_every_url_right_data(
                    type='ali',
                    tmp_list=tmp_list,
                    sql_str=fz_al_insert_str,
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

            wait_to_save_data = get_one_tb_data(
                username=username,
                tb_url=wait_to_deal_with_url,
                my_lg=my_lg)
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()
            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()
            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            collect()  

            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '淘宝抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

        else:
            # 直接把空值给pass，不打印信息
            # my_lg.info('goodsLink为空值...')
            return _null_goods_link()
    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='taobao',
                    tmp_list=tmp_list,
                    sql_str=fz_tb_insert_str,
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
            collect()  

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
        result = dumps(result)
        return result

@app.route('/tmall_to_save_data', methods=['POST'])
def tmall_to_save_data():
    """
    ## 此处注意保存的类型是天猫(3)，还是天猫超市(4)，还是天猫国际(6)
    :return:
    """
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

                return save_every_url_right_data(
                    type='tmall',
                    tmp_list=tmp_list,
                    sql_str=fz_tm_insert_str,
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
                my_lg=my_lg,)
            # pprint(wait_to_save_data)
            if wait_to_save_data.get('goods_id', '') == '':
                return _null_goods_id()
            elif wait_to_save_data.get('msg', '') == 'data为空!':
                return _null_goods_data()
            else:
                pass

            tmp_wait_to_save_data_list.append(wait_to_save_data)    # 用于存放所有url爬到的结果
            collect()  

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
        result = dumps(result)

        return result

@app.route('/jd_to_save_data', methods=['POST'])
def jd_to_save_data():
    """
    ## 此处注意保存的类型是京东(7)，还是京东超市(8)，还是京东全球购(9)，还是京东大药房(10)
    :return:
    """
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

                return save_every_url_right_data(
                    type='jd',
                    tmp_list=tmp_list,
                    sql_str=fz_jd_insert_str,
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
                collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'https://shop.zhe800.com/products/' + str(goods_id)

            tmp_result = zhe_800.get_goods_data(goods_id=goods_id)
            data = zhe_800.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del zhe_800
                collect()

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
            collect()  

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='zhe_800',
                    tmp_list=tmp_list,
                    sql_str=fz_z8_insert_str,
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
                collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://shop.juanpi.com/deal/' + str(goods_id)
            tmp_result = juanpi.get_goods_data(goods_id=goods_id)
            data = juanpi.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象

            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del juanpi
                collect()

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
            collect()  

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='juanpi',
                    tmp_list=tmp_list,
                    sql_str=fz_jp_insert_str,
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
                collect()

                return _null_goods_id()

            #####################################################
            wait_to_deal_with_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + str(goods_id)
            tmp_result = pinduoduo.get_goods_data(goods_id=goods_id)
            data = pinduoduo.deal_with_data()   # 如果成功获取的话, 返回的是一个data的dict对象
            if data == {} or tmp_result == {}:
                my_lg.info('获取到的data为空!')
                del pinduoduo
                collect()

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
            collect()  

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='pinduoduo',
                    tmp_list=tmp_list,
                    sql_str=fz_pd_insert_str,
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
                collect()
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
                collect()
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
            collect()        

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='vip',
                    tmp_list=tmp_list,
                    sql_str=fz_vi_insert_str,
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
            collect()

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='kaola',
                    tmp_list=tmp_list,
                    sql_str=fz_kl_insert_str,
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
            collect()

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='yanxuan',
                    tmp_list=tmp_list,
                    sql_str=fz_yx_insert_str,
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
            collect()

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
        result = dumps(result)
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

                return save_every_url_right_data(
                    type='youpin',
                    tmp_list=tmp_list,
                    sql_str=fz_yp_insert_str,
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
# 蜜芽
@app.route('/mia_data', methods=['POST'])
def get_mia_data():
    if is_login(request=request):  # request.cookies -> return a dict
        if request.form.get('goodsLink'):
            my_lg.info('正在获取mia相应数据中...')

            username = decrypt(key, request.cookies.get('username'))
            my_lg.info('发起获取请求的员工的username为: {0}'.format(username))

            goodsLink = request.form.get('goodsLink')
            if goodsLink:
                wait_to_deal_with_url = goodsLink
            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            wait_to_save_data = get_one_mia_data(
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
            collect()

            my_lg.info('------>>>| 下面是爬取到的蜜芽页面信息: ')
            my_lg.info(str(wait_to_save_data))
            my_lg.info('-------------------------------')
            msg = '蜜芽抓取成功!'

            return _success_data(data=wait_to_save_data, msg=msg)

        else:       # 直接把空值给pass，不打印信息
            return _null_goods_link()

    else:
        result = {
            'reason': 'error',
            'data': '',
            'error_code': 0,
        }
        result = dumps(result)
        return result

@app.route('/mia_to_save_data', methods=['POST'])
def mia_to_save_data():
    # 蜜芽 site_id=32
    global tmp_wait_to_save_data_list
    if is_login(request=request):
        if request.form.getlist('saveData[]'):  # 切记：从客户端获取list数据的方式
            wait_to_save_data_url_list = list(request.form.getlist('saveData[]'))  # 一个待存取的url的list

            wait_to_save_data_url_list = [re.compile(r'\n').sub('', item) for item in wait_to_save_data_url_list]
            # my_lg.info('缓存中待存储url的list为: {0}'.format(str(tmp_wait_to_save_data_list)))
            my_lg.info('获取到的待存取的url的list为: {0}'.format(str(wait_to_save_data_url_list)))
            if wait_to_save_data_url_list != []:
                tmp_list, goods_to_delete = get_tmp_list_and_goods_2_delete_list(
                    type='mia',
                    wait_to_save_data_url_list=wait_to_save_data_url_list
                )

                return save_every_url_right_data(
                    type='mia',
                    tmp_list=tmp_list,
                    sql_str=fz_mi_insert_str,
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
"""
/basic_data
"""
@app.route('/basic_data', methods=['POST'])
def get_basic_data():
    """
    返回一个商品地址的基本信息
    :return: 一个json
    """
    if request.form.get('basic_app_key') is not None \
            and request.form.get('basic_app_key') == BASIC_APP_KEY:
        if request.form.get('goodsLink'):
            my_lg.info('正在获取相应数据中...')
            wait_to_deal_with_url = request.form.get('goodsLink',)

            if _is_taobao_url_plus(wait_to_deal_with_url):
                tb = TaoBaoLoginAndParse(logger=my_lg)
                try:
                    goods_id = tb.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id
                    assert goods_id != '', '获取到的goods_id为空!'
                except AssertionError:
                    my_lg.error('遇到错误:', exc_info=True)
                    try:
                        del tb
                    except:
                        pass
                    return _null_goods_id()
                    
                wait_to_deal_with_url = 'https://item.taobao.com/item.htm?id=' + goods_id  # 构造成标准干净的淘宝商品地址
                try:
                    tmp_result = tb.get_goods_data(goods_id=goods_id)
                    assert tmp_result != {}, '获取到的data为空!'
                    data = tb.deal_with_data(goods_id=goods_id)  # 如果成功获取的话, 返回的是一个data的dict对象
                    assert data != {}, '获取到的data为空!'
                    time.sleep(TAOBAO_SLEEP_TIME)  # 这个在服务器里面可以注释掉为.5s
                except AssertionError:
                    my_lg.error('遇到错误:', exc_info=True)
                    try:
                        del tb
                    except:
                        pass
                    return _null_goods_data()

                _goods_id = goods_id
                data = {
                    'title': data.get('title', ''),
                    'price': data.get('taobao_price',),
                    'month_sell_count': data.get('sell_count',),     # 月销量
                    'img_url': data.get('all_img_url'),
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': _goods_id,
                }
                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }
                try:
                    del tb  # 释放login_ali的资源(python在使用del后不一定马上回收垃圾资源, 因此我们需要手动进行回收)
                except:
                    pass

            elif _is_tmall_url(wait_to_deal_with_url):
                tm = TmallParse(logger=my_lg)
                goods_id = tm.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                try:
                    assert goods_id != [], '获取到的goods_id为空!'
                except AssertionError:
                    my_lg.error('遇到错误', exc_info=True)
                    try:
                        del tm  # 每次都回收一下
                    except:
                        pass
                    return _null_goods_id()

                # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
                #####################################################
                _type, _goods_id = goods_id[0], goods_id[1]
                if _type == 0:  # [0, '1111']
                    wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + _goods_id
                elif _type == 1:  # [1, '1111']
                    wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + _goods_id
                elif _type == 2:  # [2, '1111', 'https://xxxxx']
                    wait_to_deal_with_url = str(goods_id[2]) + '?id=' + _goods_id
                try:
                    tmp_result = tm.get_goods_data(goods_id=goods_id)
                    assert tmp_result != {}, '获取到的data为空!'
                    data = tm.deal_with_data()
                    assert data != {}, '获取到的data为空!'
                except AssertionError:
                    my_lg.error('遇到错误', exc_info=True)
                    try:
                        del tm
                    except:
                        pass
                    return _null_goods_data()

                data = {
                    'title': data.get('title'),
                    'price': data.get('taobao_price'),
                    'month_sell_count': data.get('sell_count'),     # 月销量
                    'img_url': data.get('all_img_url'),
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': _goods_id,
                }
                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }
                try:
                    del tm
                except:
                    pass

            elif _is_jd_url(wait_to_deal_with_url):
                jd = JdParse(logger=my_lg)

                goods_id = jd.get_goods_id_from_url(wait_to_deal_with_url)  # 获取goods_id, 这里返回的是一个list
                try:
                    assert goods_id != [], '获取到的goods_id为空!'
                except AssertionError:
                    my_lg.error('遇到错误', exc_info=True)
                    try:
                        del jd
                    except:
                        pass
                    return _null_goods_id()

                # 改进判断，根据传入数据判断是京东(京东超市属于其中)，还是京东全球购，还是京东大药房
                #####################################################
                _type, _goods_id = goods_id
                if _type == 0:  # [0, '1111']
                    wait_to_deal_with_url = 'https://item.jd.com/' + _goods_id + '.html'  # 构造成标准干净的淘宝商品地址
                elif _type == 1:  # [1, '1111']
                    wait_to_deal_with_url = 'https://item.jd.hk/' + _goods_id + '.html'
                elif _type == 2:  # [2, '1111', 'https://xxxxx']
                    wait_to_deal_with_url = 'https://item.yiyaojd.com/' + _goods_id + '.html'

                try:
                    tmp_result = jd.get_goods_data(goods_id=goods_id)
                    assert tmp_result != {}, '获取到的data为空!'
                    data = jd.deal_with_data(goods_id=goods_id)
                    assert data != {}, '获取到的data为空!'
                except AssertionError:
                    my_lg.error('遇到错误', exc_info=True)
                    try:
                        del jd
                    except:
                        pass
                    return _null_goods_data()

                data = {
                    'title': data.get('title'),
                    'price': str(data.get('taobao_price')),
                    'all_sell_count': data.get('all_sell_count'),  # 月销量
                    'img_url': data.get('all_img_url'),
                    'spider_url': wait_to_deal_with_url,
                    'goods_id': _goods_id,
                }
                result = {
                    'reason': 'success',
                    'data': data,
                    'error_code': 0,
                }
                try:
                    del jd
                except:
                    pass

            else:
                my_lg.info('goodsLink为空值...')
                return _null_goods_link()

            result_json = dumps(
                obj=result,
                ensure_ascii=False).encode()
            my_lg.info('------>>>| 下面是爬取到的页面信息: ')
            my_lg.info(str(result_json.decode()))
            my_lg.info('-------------------------------')

            return result_json.decode()

        else:
            my_lg.info('goodsLink为空值...')
            return _null_goods_link()

    else:
        return dumps({
            'reason': 'error',
            'data': '',
            'error_code': 0,
        })

@app.route('/basic_data_2', methods=['GET', 'POST'])
@Sign.signature_required
def _get_basic_data_2():
    # 正确请求将返回以下内容，否则将被signature_required拦截，返回请求验证信息： {"msg": "Invaild message", "success": False}
    return dumps({
        'ping':"pong"
    })

######################################################
"""
/api/goods
"""
@app.route('/api/goods', methods=['GET'])
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
    """
    从cli得到goods_link(只支持get, post)
    :param kwargs:
    :return:
    """
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
"""
/api/article
"""
@app.route('/api/article_spiders_intro', methods=['GET'])
def article_spiders_intro() -> str:
    """
    获取article spiders intro
    :return:
    """
    article_parser = ArticleParser(logger=my_lg)
    loop = get_event_loop()
    res = ''
    try:
        res = loop.run_until_complete(
            article_parser.get_article_spiders_intro())
    except Exception:
        my_lg.error('遇到错误:', exc_info=True)

    try:
        del article_parser
    except:
        pass
    collect()

    return res

@app.route('/api/article', methods=['GET'])
# @Sign.signature_required
def _article():
    """
    文章接口
    :return: json
    """
    _ = get_article_link(request=request)
    article_url = b64decode(s=_.encode('utf-8')).decode('utf-8')     # _ 传来的起初是str, 先str->byte, 再b64decode解码
    my_lg.info('获取到的article_url: {}'.format(str(article_url)))

    article_parser = ArticleParser(logger=my_lg)
    loop = get_event_loop()
    article_res = {}
    try:
        article_res = loop.run_until_complete(article_parser._parse_article(article_url=article_url))
    except Exception:
        my_lg.error('遇到错误:', exc_info=True)

    try:
        del article_parser
    except:
        pass
    collect()
    if article_res == {}:
        return _error_msg(msg='文章抓取失败!')

    return _success_data(msg='文章抓取成功!', data=article_res)

def get_article_link(**kwargs):
    """
    从cli得到article_link
    :param kwargs:
    :return:
    """
    request = kwargs.get('request')

    _ = ''
    if request.method == 'GET':
        try:
            _ = dict(request.args).get('article_link', '')[0]
        except IndexError:
            my_lg.error('获取article_link时IndexError!')

    else:
        _ = request.form.get('article_link', '')

    return _

######################################################
"""
/api/fortune_telling
"""
@app.route('/api/fortune_telling', methods=['GET'])
# @Sign.signature_required
def fortune_telling():
    """
    算命接口
    :return: json
    """
    @catch_exceptions(logger=my_lg, default_res={})
    def _get_fortune_telling_res(req_args_dict: dict) -> dict:
        """
        获取接口请求res
        :param req_args_dict:
        :return:
        """
        fortune_telling_type = int(req_args_dict.get('type', '0'))
        byj_spider = BuYiJuSpider(logger=my_lg)
        loop = get_event_loop()

        if fortune_telling_type == 0:
            # 姓名打分
            res = loop.run_until_complete(byj_spider.name_scoring(
                surname=req_args_dict.get('surname', '吕'),
                name=req_args_dict.get('name', '布'),))

        elif fortune_telling_type == 1:
            # 测字算命
            res = loop.run_until_complete(byj_spider.word_and_fortune_telling(
                two_words=req_args_dict.get('two_words', '你好')))

        elif fortune_telling_type == 2:
            # 生日算命
            res = loop.run_until_complete(byj_spider.birthday_fortune_telling(
                month=int(req_args_dict.get('month', 1)),
                day=int(req_args_dict.get('day', 1)),))

        elif fortune_telling_type == 3:
            # 手机号码测吉凶
            res = loop.run_until_complete(byj_spider.phone_number_for_good_or_bad_luck(
                phone_num=int(req_args_dict.get('phone_num', '18796571279')),))

        elif fortune_telling_type == 4:
            # 车牌号码测吉凶
            res = loop.run_until_complete(byj_spider.license_plate_num_for_good_or_bad(
                province=req_args_dict.get('province', '京'),
                city_num=req_args_dict.get('city_num', 'A'),
                num=req_args_dict.get('num', '66666'),))

        elif fortune_telling_type == 5:
            # 姓名缘分配对
            res = loop.run_until_complete(byj_spider.distribution_pairs_of_names(
                name1=req_args_dict.get('name1', '吕布'),
                name2=req_args_dict.get('name2', '貂蝉'),))

        elif fortune_telling_type == 6:
            # 星座配对
            res = loop.run_until_complete(byj_spider.constellation_pairing(
                name1=req_args_dict.get('name1', '处女座'),
                name2=req_args_dict.get('name2', '摩羯座'),))

        elif fortune_telling_type == 7:
            # 抽签算命
            TIPS = {
                '观音灵签': 'gy',
                '佛祖灵签': 'fz',
                '月老灵签': 'yl',
                '关帝灵签': 'gd',
                '黄大仙灵签': 'hdx',
                '吕祖灵签': 'lv',
                '天后妈祖灵签': 'mz',
                '财神灵签': 'cs',
                '地藏王灵签': 'dzw',
                '易经64卦灵签': 'yj',
                '太上老君灵签': 'tslj',
            }
            res = loop.run_until_complete(byj_spider.fortune_telling_by_lot(
                lot_type=req_args_dict.get('lot_type', 'gy'),))

        else:
            raise NotImplemented('未实现fortune_telling_type值!')

        try:
            del loop
            del byj_spider
        except:
            pass

        return res

    req_args_dict = request.args
    my_lg.info(str(req_args_dict))

    try:
        res = _get_fortune_telling_res(req_args_dict=req_args_dict)
        assert res != {}
    except Exception:
        my_lg.error('遇到错误:', exc_info=True)
        return _error_msg(msg='抓取失败')

    return _success_data(
        msg='抓取成功',
        data=res,
    )

######################################################
"""
/spider/dcs
"""
# 避免与asyncio的Queue冲突
tm_real_time_update_queue = Queue()
tm_real_time_update_lock = ThreadingLock()
tb_real_time_update_queue = Queue()
tb_real_time_update_lock = ThreadingLock()

@app.route('/spider/dcs', methods=['GET'])
def spider_dcs():
    """
    待更新数据获取接口
    :return:
    """
    @catch_exceptions(logger=my_lg, default_res=[])
    def get_dcs_res(req_args_dict: dict) -> list:
        """
        :param req_args_dict:
        :return:
        """
        def add_2_update_queue(queue_name, sql_str, target_queue, target_queue_thread_lock) -> None:
            """
            target_queue为空队列时, 从db新增数据进target_queue
            :param queue_name:
            :param sql_str:
            :param target_queue: eg: tm_real_time_update_queue
            :param target_queue_thread_lock: eg: tm_real_time_update_lock
            :return:
            """
            # todo 可注释, 闭包中全局变量若已在上层父包导入, 即可直接在闭包中取值or修改
            # global tm_real_time_update_queue

            if target_queue.empty():
                sql_cli = SqlServerMyPageInfoSaveItemPipeline()
                my_lg.info('{} is null queue, 从db赋值ing...'.format(queue_name))
                res = list(sql_cli._select_table(
                    sql_str=sql_str,
                    logger=my_lg, ))
                for item in res:
                    target_queue_thread_lock.acquire()
                    new_item = get_new_list_by_handle_list_2_json_error(
                        target_list=item)
                    try:
                        target_queue.put(new_item)
                    except Exception:
                        pass
                    finally:
                        target_queue_thread_lock.release()
                try:
                    del sql_cli
                except:
                    pass
                my_lg.info('{} 赋值完毕!'.format(queue_name))
            else:
                my_lg.info('{} is not null queue, 直接取值中ing...'.format(queue_name))

            return

        global tm_real_time_update_queue, tb_real_time_update_queue

        res = []
        # 待获取的type, eg: 'tm', 'tb'
        dcs_type = req_args_dict.get('type', '')
        assert dcs_type != ''
        dcs_child_type = int(req_args_dict.get('child_type', '0'))
        # 单次请求获取数据量个数
        max_one_get_num = 100

        if dcs_type == 'tm':
            if dcs_child_type == 0:
                # 实时更新
                queue_name = '{}_{}_queue'.format(dcs_type, 'real_time_update')
                sql_str = tm_select_str_3
                t1 = Thread(
                    target=add_2_update_queue,
                    args=(
                        queue_name,
                        sql_str,
                        tm_real_time_update_queue,
                        tm_real_time_update_lock,
                    ),)
                t1.start()
                t1.join(timeout=20)
                target_queue = tm_real_time_update_queue
            else:
                raise ValueError('dcs_child_type: {} 值异常!'.format(dcs_child_type))

        elif dcs_type == 'tb':
            if dcs_child_type == 0:
                # 实时更新
                queue_name = '{}_{}_queue'.format(dcs_type, 'real_time_update')
                sql_str = tb_select_str_3
                t1 = Thread(
                    target=add_2_update_queue,
                    args=(
                        queue_name,
                        sql_str,
                        tb_real_time_update_queue,
                        tb_real_time_update_lock,
                    ),)
                t1.start()
                t1.join(timeout=20)
                target_queue = tb_real_time_update_queue
            else:
                raise ValueError('dcs_child_type: {} 值异常!'.format(dcs_child_type))

        else:
            raise ValueError('dcs_type: {} 值异常!'.format(dcs_type))

        try:
            del t1
        except:
            pass
        while not target_queue.empty() \
                and max_one_get_num > 0:
            res.append(target_queue.get())
            max_one_get_num -= 1

        return res

    global tm_real_time_update_queue, tb_real_time_update_queue

    req_args_dict = request.args
    my_lg.info(str(req_args_dict))

    try:
        res = get_dcs_res(req_args_dict=req_args_dict)
    except Exception:
        my_lg.error('遇到错误:', exc_info=True)
        return _error_msg(msg='抓取失败', default_res=[])

    return _success_data(
        msg='获取db数据成功!',
        data=res,)

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
# error page handler
@app.errorhandler(404)
def page_not_found(error):
    """
    404页面
    :param error:
    :return:
    """
    return send_file('templates/404.html'), 404

######################################################
# 从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]
def get_tmp_list_and_goods_2_delete_list(**kwargs):
    """
    从tmp_wait_to_save_data_list对应筛选出待存储的缓存数据[tmp_list]和待删除的goods缓存[goods_to_delete]
    :param kwargs:
    :return:
    """
    global tmp_wait_to_save_data_list

    # 三方商品类型
    type = kwargs.get('type')
    # client发来的待存储的url_list
    wait_to_save_data_url_list = kwargs.get('wait_to_save_data_url_list')

    tmp_wait_to_save_data_goods_id_list = get_who_wait_to_save_data_goods_id_list(
        type=type,
        wait_to_save_data_url_list=wait_to_save_data_url_list,
        my_lg=my_lg,)

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
    """
    存储处理后的每一个url的数据
    :param kwargs:
    :return: a json msg
    """
    global tmp_wait_to_save_data_list

    tmp_list = kwargs.get('tmp_list')
    type = kwargs.get('type')
    sql_str = kwargs.get('sql_str')
    goods_to_delete = kwargs.get('goods_to_delete')

    my_page_info_save_item_pipeline = SqlServerMyPageInfoSaveItemPipeline()
    # 存储['db插入结果类型bool', '对应goods_id']
    is_inserted_and_goods_id_list = []
    for item in tmp_list:
        my_lg.info('------>>>| 正在存储的数据为: {0}'.format(str(item.get('goods_id', ''))))
        params = get_db_who_insert_params(type=type, item=item)
        is_insert_into = my_page_info_save_item_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=my_lg)
        is_inserted_and_goods_id_list.append((is_insert_into, str(item.get('goods_id', ''))))

    tmp_wait_to_save_data_list = [i for i in tmp_wait_to_save_data_list if i not in goods_to_delete]  # 删除已被插入
    my_lg.info('存入完毕'.center(100, '*'))
    # del my_page_info_save_item_pipeline
    collect()

    return _insert_into_db_result(
        pipeline=my_page_info_save_item_pipeline,
        is_inserted_and_goods_id_list=is_inserted_and_goods_id_list
    )

######################################################
def just_fuck_run():
    my_lg.info('服务器已经启动...等待接入中...')
    my_lg.info('http://0.0.0.0:{0}'.format(str(SERVER_PORT), ))

    # app.debug = True

    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

    # 简单的多线程
    # app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

def main():
    my_lg.info('========主函数开始========')
    daemon_init()
    my_lg.info('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == "__main__":
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
