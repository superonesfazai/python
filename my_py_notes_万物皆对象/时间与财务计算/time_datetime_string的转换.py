# coding:utf-8

'''
@author = super_fazai
@File    : time_datetime_string的转换.py
@Time    : 2017/11/6 07:39
@connect : superonesfazai@gmail.com
'''

import datetime
import time

# 把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")


# 把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")


# 把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())


# 把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))


# 把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())

print(timestamp_toString(1510704000))
