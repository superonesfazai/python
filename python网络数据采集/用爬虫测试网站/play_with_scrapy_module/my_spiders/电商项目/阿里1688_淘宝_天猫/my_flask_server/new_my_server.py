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

from ali_1688_login_and_parse_idea2 import ALi1688LoginAndParse
from taobao_login_and_parse_idea2 import TaoBaoLoginAndParse
from my_pipeline import UserItemPipeline
from settings import ALi_SPIDER_TO_SHOW_PATH, TAOBAO_SPIDER_TO_SHWO_PATH
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import hashlib
import json
import time
from time import sleep
import datetime
import re
from decimal import Decimal

from gevent.wsgi import WSGIServer      # 高并发部署
import gc

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
                pass
            else:
                return '''
                <html><header></header><body>非法操作!请返回登录页面登录后继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
                '''
        else:
            return render_template('select.html')
    else:   # 非法登录显示错误网页
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''

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
                print('用户 %s 注册成功!' % username)
                return redirect('/')
            else:
                return "用户注册失败!"

        else:       # 输入员工口令错误
            return "内部员工口令错误, 请返回重新注册!"

    else:
        #request.args['username']
        return render_template('Reg.html')

@app.route('/show_ali', methods=['GET', 'POST'])
def show_ali_info():
    '''
    点击后成功后显示的爬取页面
    :return:
    '''
    if request.cookies.get('username') is None or request.cookies.get('passwd') is None:     # request.cookies -> return a dict
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后, 再继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''
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
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后, 再继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''
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
    if request.cookies.get('username') is None or request.cookies.get(
            'passwd') is None:  # request.cookies -> return a dict
        return '''
        <html><header></header><body>非法操作!请返回登录页面登录后, 再继续相关操作<a href="/"></br></br>返回登录页面</a></body></html>
        '''
    else:
        print('正在获取爬取页面...')
        if request.method == 'POST':
            pass
        else:
            # return send_file('templates/spider_to_show.html')       # 切记：有些js模板可能跑不起来, 但是自己可以直接发送静态文件
            return send_file(ALi_SPIDER_TO_SHOW_PATH)

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
                print('所有待存储的数据: ', tmp_wait_to_save_data_list)

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
                            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            tmp['deal_with_time'] = now_time                                        # 操作时间

                            tmp['modfiy_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 修改时间

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

                            print('------>>> | 待存储的数据信息为: |', tmp)
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
                    print('------>>> | 正在存储的数据为: |', item)
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
            time.sleep(2)
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
            print('------>>> 下面是爬取到的页面信息: ')
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
                print('所有待存储的数据: ', tmp_wait_to_save_data_list)

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
                            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            tmp['deal_with_time'] = now_time                    # 操作时间

                            tmp['modfiy_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 修改时间

                            tmp['shop_name'] = data_list['shop_name']           # 公司名称
                            tmp['title'] = data_list['title']                   # 商品名称
                            tmp['sub_title'] = data_list['sub_title']           # 商品子标题
                            tmp['link_name'] = ''                               # 卖家姓名
                            tmp['account'] = data_list['account']               # 掌柜名称

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

                            print('------>>> | 待存储的数据信息为: |', tmp)
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
                    print('------>>> | 正在存储的数据为: |', item)
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
    pass

@app.route('/tmall_to_save_data', methods=['POST'])
def tmall_to_save_data():
    ## 此处注意保存的类型是天猫(3)，还是天猫超市(4)，还是天猫国际(6)
    pass

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

if __name__ == "__main__":
    print('服务器已经启动...等待接入中...')
    print('http://0.0.0.0:5000')

    WSGIServer(listener=('0.0.0.0', 5000), application=app).serve_forever()      # 采用高并发部署
    # app.run(host= '0.0.0.0', debug=False, port=5000)

    # 简单的多线程
    # app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
