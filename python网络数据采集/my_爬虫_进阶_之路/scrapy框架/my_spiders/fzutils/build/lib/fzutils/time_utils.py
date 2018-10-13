# coding:utf-8

'''
@author = super_fazai
@File    : time_utils.py
@Time    : 2016/7/13 18:02
@connect : superonesfazai@gmail.com
'''

import time
from pytz import (
    timezone,
    country_timezones,)
from datetime import datetime
import re
import functools
from threading import Thread

__all__ = [
    'get_shanghai_time',                            # 时区处理，得到上海时间
    'timestamp_to_regulartime',                     # 时间戳转规范的时间字符串
    'string_to_datetime',                           # 将字符串转换成时间
    'datetime_to_timestamp',                        # datetime转timestamp
    'date_parse',                                   # 不规范日期解析为datetime类型

    'fz_timer',                                     # 一个装饰器或者上下文管理器, 用于计算某函数耗时
    'fz_set_timeout',                               # 可以给任意可能会hang住的函数添加超时功能[这个功能在编写外部API调用, 网络爬虫, 数据库查询的时候特别有用]
]

def get_shanghai_time(retries=10):
    '''
    时区处理，得到上海时间
    :return: datetime类型
    '''
    # TODO 时区处理，时间处理到上海时间
    # pytz查询某个国家时区
    # country_timezones_list = country_timezones('cn')
    # print(country_timezones_list)

    tz = timezone('Asia/Shanghai')                                      # 创建时区对象
    now_time = datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    try:
        now_time = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')     # 将字符串类型转换为datetime类型
    except ValueError as e:                                             # 捕获 ValueError: unconverted data remains: +08:00 异常!
        if retries > 0:
            return get_shanghai_time(retries=retries-1)
        else:
            raise e

    return now_time

def timestamp_to_regulartime(timestamp):
    '''
    将时间戳转换成时间
    '''
    # 利用localtime()函数将时间戳转化成localtime的格式
    # 利用strftime()函数重新格式化时间

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

def string_to_datetime(string):
    '''
    将字符串转换成datetime
    :param string:
    :return:
    '''
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def datetime_to_timestamp(_dateTime):
    '''
    把datetime类型转外时间戳形式
    :param _dateTime:
    :return: int
    '''
    return int(time.mktime(_dateTime.timetuple()))

class fz_timer(object):
    """
    A timer can time how long does calling take as 上下文管理器 or 装饰器.
    If assign ``print_func`` with ``sys.stdout.write``, ``logger.info`` and so on,
    timer will print the spent time.
        用法: eg:
            import sys

            @fz_timer(print_func=sys.stdout.write)
            def tmp():
                get_shanghai_time()

            tmp()
    """
    def __init__(self, print_func=None):
        '''
        :param print_func: sys.stdout.write | logger.info
        '''
        self.elapsed = None
        self.print_func = print_func

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *_):
        self.elapsed = time.time() - self.start
        if self.print_func:
            self.print_func(self.__str__())

    def __call__(self, fun):
        def wrapper(*args, **kwargs):
            with self:
                return fun(*args, **kwargs)
        return wrapper

    def __str__(self):
        return 'Spent time: {}s'.format(self.elapsed)

class TimeoutError(Exception):
    pass

def fz_set_timeout(seconds, error_message='函数执行超时!'):
    '''
    可以给任意可能会hang住的函数添加超时功能[这个功能在编写外部API调用, 爬虫, 数据库查询的时候特别有用]
        用法: eg:
            from time import sleep

            @fz_set_timeout(seconds=2)
            def tmp():
                sleep(3)

            tmp()
    :param seconds: 设置超时时间
    :param error_message: 显示的错误信息
    :return: None | Exception: 自定义的超时异常TimeoutError
    '''
    def decorated(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            share = [TimeoutError(error_message)]
            def func_with_except():
                try:
                    share[0] = func(*args, **kwargs)
                except Exception as e:
                    share[0] = e

            t = Thread(target=func_with_except)
            t.daemon = True
            try:
                t.start()
                t.join(seconds)
            except Exception as e:
                raise e

            result = share[0]
            if isinstance(result, BaseException):
                raise result

            return result

        return wrapper

    return decorated

def date_parse(target_date_str) -> datetime:
    '''
    不规范日期解析为datetime类型
        eg:
            In [5]: parse('2018-10-11T07:46:19Z')
            Out[5]: datetime.datetime(2018, 10, 11, 7, 46, 19, tzinfo=tzutc())

            In [6]: parse('Sun, 25 Nov 2018 14:46:19 +0800')
            Out[6]: datetime.datetime(2018, 11, 25, 14, 46, 19, tzinfo=tzoffset(None, 28800))
    :param target_date_str:
    :return:
    '''
    from dateutil.parser import parse

    return parse(target_date_str)