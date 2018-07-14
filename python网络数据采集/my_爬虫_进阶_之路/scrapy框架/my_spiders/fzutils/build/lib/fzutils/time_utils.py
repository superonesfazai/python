# coding:utf-8

'''
@author = super_fazai
@File    : time_utils.py
@Time    : 2018/7/13 18:02
@connect : superonesfazai@gmail.com
'''

__all__ = [
    'get_shanghai_time',                            # 时区处理，得到上海时间
    'timestamp_to_regulartime',                     # 时间戳转规范的时间字符串
    'string_to_datetime',                           # 将字符串转换成时间
    'datetime_to_timestamp',                        # datetime转timestamp

]

def get_shanghai_time():
    '''
    时区处理，得到上海时间
    :return: datetime类型
    '''
    import pytz
    import datetime
    import re

    # TODO 时区处理，时间处理到上海时间
    # pytz查询某个国家时区
    # country_timezones_list = pytz.country_timezones('cn')
    # print(country_timezones_list)

    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time

def timestamp_to_regulartime(timestamp):
    '''
    将时间戳转换成时间
    '''
    import time
    # 利用localtime()函数将时间戳转化成localtime的格式
    # 利用strftime()函数重新格式化时间

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

def string_to_datetime(string):
    '''
    将字符串转换成datetime
    :param string:
    :return:
    '''
    import datetime

    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def datetime_to_timestamp(_dateTime):
    '''
    把datetime类型转外时间戳形式
    :param _dateTime:
    :return: int
    '''
    import time

    return int(time.mktime(_dateTime.timetuple()))
