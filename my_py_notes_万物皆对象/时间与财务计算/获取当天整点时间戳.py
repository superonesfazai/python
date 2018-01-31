# coding:utf-8

'''
@author = super_fazai
@File    : 获取当天整点时间戳.py
@Time    : 2018/1/31 10:45
@connect : superonesfazai@gmail.com
'''

from datetime import datetime
import time

def gettime():
    for x in range(24):        # 循环24 x依次为 0-23
        # datetime.datetime.now()获得当前时间，strftime格式化,%2d以2位的固定位宽获取int型的数值，由此获得整点字符串
        a = datetime.now().strftime("%Y-%m-%d")+" %2d:00:00" % x
        # 函数根据指定的格式把一个时间字符串解析为时间元组，返回struct_time对象。
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        # 它接收struct_time对象作为参数，返回用秒数来表示时间的浮点数。int()强制转换 取整
        timeStamp = int(time.mktime(timeArray))
        print(timeStamp)


gettime()