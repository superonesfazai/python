# coding:utf-8

'''
@author = super_fazai
@File    : test_jd.py
@Time    : 2017/11/10 13:36
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import requests
from time import sleep
from pprint import pprint
import pytz
import datetime
import re

'''
时区处理，时间处理到上海时间
'''
tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
now_time = datetime.datetime.now(tz)

# 处理为精确到秒位，删除时区信息
now_time = re.compile(r'\..*').sub('', str(now_time))
# 将字符串类型转换为datetime类型
now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

print(type(now_time.hour))

