# coding:utf-8

'''
@author = super_fazai
@File    : 获取当天整点时间戳.py
@Time    : 2018/1/31 10:45
@connect : superonesfazai@gmail.com
'''

import time, datetime
from pprint import pprint

def get_today_hour_timestamp():
    '''
    得到today的整点时间戳
    :return:today_hour_timestamp_list 类型 list
    '''
    today_hour_timestamp_list = []
    for hour in range(9, 17):        # 循环需求的整点时间
        # strftime格式化,%2d以2位的固定位宽获取int型的数值，由此获得整点字符串
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % hour
        # 把一个时间字符串解析为时间元组，返回struct_time对象。
        time_array = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        # 接收struct_time对象作为参数，返回用秒数来表示时间的浮点数
        timestamp = int(time.mktime(time_array))
        today_hour_timestamp_list.append(timestamp)

    return today_hour_timestamp_list

def timestamp_toString(timestamp):
    '''
    把时间戳转成字符串形式
    :param time_stamp: 时间戳
    :return:
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

hour_time_stamp = get_today_hour_timestamp()
pprint(hour_time_stamp)