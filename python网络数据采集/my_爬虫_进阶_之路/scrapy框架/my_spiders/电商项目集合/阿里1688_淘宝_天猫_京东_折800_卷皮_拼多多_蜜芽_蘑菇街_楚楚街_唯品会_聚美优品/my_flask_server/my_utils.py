# coding:utf-8

'''
@author = super_fazai
@File    : my_utils.py
@Time    : 2017/3/31 14:16
@connect : superonesfazai@gmail.com
'''

import pytz, datetime, re
import sys, os, time, json
from pprint import pprint
from json import JSONDecodeError
import asyncio
import execjs
from random import randint
from my_ip_pools import MyIpPools
import requests

__all__ = [
    'get_shanghai_time',                                # 时区处理，得到上海时间
    'daemon_init',                                      # 守护进程
    'timestamp_to_regulartime',                         # 时间戳转规范的时间字符串
    'string_to_datetime',                               # 将字符串转换成时间
    'datetime_to_timestamp',                            # datetime转timestamp
    'restart_program',                                  # 初始化避免异步导致log重复打印
    'process_exit',                                     # 判断进程是否存在
    '_get_url_contain_params',                          # 根据params组合得到包含params的url
    'str_cookies_2_dict',                               # cookies字符串转dict
    'tuple_or_list_params_2_dict_params',               # tuple和list类型的params转dict类型的params
    '_json_str_to_dict',                                # json转dict
    '_green',                                           # 将字体变成绿色
    'delete_list_null_str',                             # 删除list中的空str
    'kill_process_by_name',                             # 根据进程名杀掉对应进程

    '_get_price_change_info',                           # 公司用来记录价格改变信息
    'set_delete_time_from_orginal_time',                # 公司返回原先商品状态变换被记录下的时间点
    'get_my_shelf_and_down_time_and_delete_time',       # 公司得到my_shelf_and_down_time和delete_time
    'get_miaosha_begin_time_and_miaosha_end_time',      # 公司返回秒杀开始和结束时间

    'calculate_right_sign',                             # 获取淘宝sign
    'get_taobao_sign_and_body',                         # 得到淘宝带签名sign的接口数据
]

def get_shanghai_time():
    '''
    时区处理，得到上海时间
    :return: datetime类型
    '''
    # 时区处理，时间处理到上海时间
    # pytz查询某个国家时区
    country_timezones_list = pytz.country_timezones('cn')
    # print(country_timezones_list)

    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time

def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    '''
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:     # 父进程
            os._exit(0)
    except OSError as e:
        sys.stderr.write("first fork failed!!" + e.strerror)
        os._exit(1)

    # 子进程， 由于父进程已经退出，所以子进程变为孤儿进程，由init收养
    '''setsid使子进程成为新的会话首进程，和进程组的组长，与原来的进程组、控制终端和登录会话脱离。'''
    os.setsid()
    '''防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下'''
    os.chdir("/")
    '''设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的'''
    os.umask(0)

    try:
        pid = os.fork()  # 第二次进行fork,为了防止会话首进程意外获得控制终端
        if pid > 0:
            os._exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("second fork failed!!" + e.strerror)
        os._exit(1)

    # 孙进程
    #   for i in range(3, 64):  # 关闭所有可能打开的不需要的文件，UNP中这样处理，但是发现在python中实现不需要。
    #       os.close(i)
    sys.stdout.write("Daemon has been created! with pid: %d\n" % os.getpid())
    sys.stdout.flush()  # 由于这里我们使用的是标准IO，这里应该是行缓冲或全缓冲，因此要调用flush，从内存中刷入日志文件。

def timestamp_to_regulartime(timestamp):
    '''
    将时间戳转换成时间
    '''
    # 利用localtime()函数将时间戳转化成localtime的格式
    # 利用strftime()函数重新格式化时间

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

# 把字符串转成datetime
def string_to_datetime(string):
    '''
    将字符串转换成datetime
    :param string:
    :return:
    '''
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def datetime_to_timestamp(_dateTime):
    '''
    把datetime类型转外时间戳形式
    :param _dateTime:
    :return: int
    '''
    return int(time.mktime(_dateTime.timetuple()))

def restart_program():
    '''
    初始化避免异步导致log重复打印
    :return:
    '''
    import sys
    import os
    python = sys.executable
    os.execl(python, python, * sys.argv)

def process_exit(process_name):
    '''
    判断进程是否存在
    :param process_name:
    :return: 0 不存在 | >= 1 存在
    '''
    # Linux
    process_check_response = os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines()
    return len(process_check_response)

def _get_url_contain_params(url, params):
    '''
    根据params组合得到包含params的url
    :param url:
    :param params:
    :return: url
    '''
    return url + '?' + '&'.join([item[0] + '=' + item[1] for item in params])

def str_cookies_2_dict(str_cookies):
    '''
    cookies字符串转dict
    :param str_cookies:
    :return:
    '''
    _ = [(i.split('=')[0], i.split('=')[1]) for i in str_cookies.replace(' ', '').split(';')]

    cookies_dict = {}
    for item in _:
        cookies_dict.update({item[0]: item[1]})

    return cookies_dict

def tuple_or_list_params_2_dict_params(params):
    '''
    tuple和list类型的params转dict类型的params
    :param params:
    :return:
    '''
    _ = {}
    for item in params:
        _.update({
            item[0]: item[1]
        })

    return _

def _json_str_to_dict(json_str):
    '''
    json字符串转dict
    :param json_str:
    :return:
    '''
    try:
        _ = json.loads(json_str)
    except JSONDecodeError as e:
        print(e)
        return {}

    return _

def _green(string):
    '''
    将字体转变为绿色
    :param string:
    :return:
    '''
    return '\033[32m{}\033[0m'.format(string)

def set_delete_time_from_orginal_time(my_shelf_and_down_time):
    '''
    公司返回原先商品状态变换被记录下的时间点
    :param my_shelf_and_down_time: 一个dict
    :return: detele_time    datetime类型
    '''
    shelf_time = my_shelf_and_down_time.get('shelf_time', '')
    if shelf_time != '':
        # 将字符串类型的时间转换为datetime类型
        shelf_time = datetime.datetime.strptime(shelf_time, '%Y-%m-%d %H:%M:%S')
    down_time = my_shelf_and_down_time.get('down_time', '')
    if down_time != '':
        down_time = datetime.datetime.strptime(down_time, '%Y-%m-%d %H:%M:%S')

    if shelf_time == '':
        delete_time = down_time
    elif down_time == '':
        delete_time = shelf_time
    else:  # shelf_time和down_time都不为''
        if shelf_time > down_time:  # 取最近的那个
            delete_time = shelf_time
        else:
            delete_time = down_time

    return delete_time

def get_my_shelf_and_down_time_and_delete_time(tmp_data, is_delete, MyShelfAndDownTime):
    '''
    公司得到my_shelf_and_down_time和delete_time
    :param tmp_data:
    :param is_delete:
    :param MyShelfAndDownTime:
    :return:
    '''
    # 设置最后刷新的商品状态上下架时间
    # 1.is_delete由0->1 为下架时间down_time  2. is_delete由1->0 为上架时间shelf_time
    my_shelf_and_down_time = {
        'shelf_time': '',
        'down_time': '',
    }
    if tmp_data['is_delete'] != is_delete:  # 表示状态改变
        if tmp_data['is_delete'] == 0 and is_delete == 1:
            # is_delete由0->1 表示商品状态上架变为下架
            my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
        else:
            # is_delete由1->0 表示商品状态下架变为上架
            my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
        delete_time = str(get_shanghai_time())  # 记录下状态变化的时间点
    else:  # 表示状态不变
        if MyShelfAndDownTime is None or MyShelfAndDownTime == '{"shelf_time": "", "down_time": ""}' or len(MyShelfAndDownTime) == 35:  # 35就是那串初始str
            if tmp_data['is_delete'] == 0:  # 上架的状态
                my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
            else:  # 下架的状态
                my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
            delete_time = str(get_shanghai_time())
        else:
            # 否则保存原始值不变
            tmp_shelf_and_down_time = MyShelfAndDownTime
            my_shelf_and_down_time = json.loads(tmp_shelf_and_down_time)  # 先转换为dict
            # print(my_shelf_and_down_time)
            delete_time = set_delete_time_from_orginal_time(my_shelf_and_down_time=my_shelf_and_down_time)

    return (my_shelf_and_down_time, delete_time)

def _get_price_change_info(old_price, old_taobao_price, new_price, new_taobao_price):
    '''
    公司用来记录价格改变信息
    :param old_price: 原始最高价 type Decimal
    :param old_taobao_price: 原始最低价 type Decimal
    :param new_price: 新的最高价
    :param new_taobao_price: 新的最低价
    :return: _is_price_change 0 or 1 | _
    '''
    # print(old_price)
    # print(type(old_price))
    # print(new_price)
    # print(type(new_price))
    _is_price_change = 0
    if float(old_price) != float(new_price) or float(old_taobao_price) != float(new_taobao_price):
        _is_price_change = 1

    _ = {
        'old_price': str(old_price),
        'old_taobao_price': str(old_taobao_price),
        'new_price': str(new_price),
        'new_taobao_price': str(new_taobao_price),
    }

    return _is_price_change, _

async def calculate_right_sign(_m_h5_tk: str, data: json):
    '''
    根据给的json对象 data 和 _m_h5_tk计算出正确的sign
    :param _m_h5_tk:
    :param data:
    :return: sign 类型str, t 类型str
    '''
    with open('../static/js/get_h_func.js', 'r') as f:  # 打开js源文件
        js = f.read()

    js_parser = execjs.compile(js)  # 编译js得到python解析对象
    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

    # 构造参数e
    appKey = '12574478'
    # e = 'undefine' + '&' + t + '&' + appKey + '&' + '{"optStr":"{\"displayCount\":4,\"topItemIds\":[]}","bizCode":"tejia_003","currentPage":"1","pageSize":"4"}'
    e = _m_h5_tk + '&' + t + '&' + appKey + '&' + data

    sign = js_parser.call('h', e)

    return sign, t

async def get_taobao_sign_and_body(base_url, headers:dict, params:dict, data:json, timeout=13, _m_h5_tk='undefine', session=None, logger=None):
    '''
    得到淘宝带签名sign接口数据
    :param base_url:
    :param headers:
    :param params:
    :param data:
    :param timeout:
    :param _m_h5_tk:
    :param session:
    :return: (_m_h5_tk, session, body)
    '''
    sign, t = await calculate_right_sign(data=data, _m_h5_tk=_m_h5_tk)
    headers['Host'] = re.compile(r'://(.*?)/').findall(base_url)[0]
    params.update({  # 添加下面几个query string
        't': t,
        'sign': sign,
        'data': data,
    })

    # 设置代理ip
    ip_object = MyIpPools()
    proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
    proxy = proxies['http'][randint(0, len(proxies) - 1)]

    tmp_proxies = {
        'http': proxy,
    }

    if session is None:
        session = requests.session()
    else:
        session = session
    try:
        response = session.get(url=base_url, headers=headers, params=params, proxies=tmp_proxies, timeout=timeout)
        _m_h5_tk = response.cookies.get('_m_h5_tk', '')
        _m_h5_tk = _m_h5_tk.split('_')[0]
        # print(s.cookies.items())
        # print(_m_h5_tk)

        body = response.content.decode('utf-8')
        # print(body)

    except Exception as e:
        logger.exception(e)
        _m_h5_tk = ''
        body = ''

    return (_m_h5_tk, session, body)

def get_miaosha_begin_time_and_miaosha_end_time(miaosha_time):
    '''
    返回秒杀开始和结束时间
    :param miaosha_time: 里面的miaosha_begin_time的类型为字符串类型
    :return: tuple  miaosha_begin_time, miaosha_end_time
    '''
    miaosha_begin_time = miaosha_time.get('miaosha_begin_time')
    miaosha_end_time = miaosha_time.get('miaosha_end_time')

    if miaosha_begin_time is None or miaosha_end_time is None:
        miaosha_begin_time = miaosha_time.get('begin_time')
        miaosha_end_time = miaosha_time.get('end_time')

    # 将字符串转换为datetime类型
    miaosha_begin_time = datetime.datetime.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')
    miaosha_end_time = datetime.datetime.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')

    return miaosha_begin_time, miaosha_end_time

def delete_list_null_str(_list):
    '''
    删除list中的所有空str
    :param _list:
    :return:
    '''
    while '' in _list:
        _list.remove('')

    return _list

def kill_process_by_name(process_name):
    '''
    根据进程名杀掉对应进程
    :param process_name: str
    :return:
    '''
    if process_exit(process_name) > 0:
        try:
            process_check_response = delete_list_null_str(os.popen('ps aux | grep ' + process_name).readlines()[0].split(' '))[1]
            os.system('kill -9 %s' % process_check_response)
            print('该进程名%s, pid = %s, 进程kill完毕!!' % (process_name, process_check_response))

        except Exception as e:
            print(e)
    else:
        print('进程[%s]不存在' % process_name)
