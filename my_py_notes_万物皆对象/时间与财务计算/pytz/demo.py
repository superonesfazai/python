# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/11/6 07:21
@connect : superonesfazai@gmail.com
'''

import pytz
import datetime
import re

'''
时区处理，时间处理到上海时间
'''
# pytz查询某个国家时区
country_timezones_list = pytz.country_timezones('cn')
# print(country_timezones_list)

tz = pytz.timezone('Asia/Shanghai')     # 创建时区对象
now_time = datetime.datetime.now(tz)
# print(type(now_time))

# 处理为精确到秒位，删除时区信息
now_time = re.compile(r'\..*').sub('', str(now_time))
# 将字符串类型转换为datetime类型
now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
print(now_time)
# print(str(now_time)[0:10])