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

def get_shanghai_time():
    '''
    时区处理，时间处理到上海时间
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
    except Exception as e:
        print(e)
        return {}

    return _

