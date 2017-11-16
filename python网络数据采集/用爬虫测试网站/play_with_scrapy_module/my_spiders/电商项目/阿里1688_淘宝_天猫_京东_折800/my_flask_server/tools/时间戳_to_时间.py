# coding:utf-8

'''
@author = super_fazai
@File    : 时间戳_to_时间.py
@Time    : 2017/11/15 17:13
@connect : superonesfazai@gmail.com
'''

import time

def timestamp_to_regulartime(timestamp):
    '''
    将时间戳转换成时间
    '''
    # 利用localtime()函数将时间戳转化成localtime的格式
    # 利用strftime()函数重新格式化时间

    # 转换成localtime
    time_local = time.localtime(timestamp)
    # print(time_local)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    return dt

timestamp = 1510826400
dt = timestamp_to_regulartime(timestamp)
print(dt)

def is_recent_time(timestamp):
    '''
    返回是否在指定的日期差内
    :param timestamp:
    :return:
    '''
    time_1 = int(timestamp)
    time_2 = time.time()            # 当前的时间戳
    time_1 = time.localtime(time_1)
    time_2 = time.localtime(time_2)
    if time_1.tm_year == time_2.tm_year:
        if time_1.tm_mon >= time_2.tm_mon:  # 如果目标时间的月份时间 >= 当前月份(月份合法, 表示是当前月份或者是今年其他月份)
            if time_1.tm_mday >= time_2.tm_mday:
                if time_1.tm_hour >= 8 and time_1.tm_hour <= 16:
                    print('合法时间')
                    # diff_days = abs(time_1.tm_mday - time_2.tm_mday)
                    return True
                else:
                    print('该小时在8点到16点以外，此处不处理跳过')
                    return False
            else:
                print('该日时间已过期, 此处跳过')
                return False
        else:                               # 月份过期
            print('该月份时间已过期，此处跳过')
            return False

    else:
        print('非本年度的限时秒杀时间，此处跳过')
        return False

while True:
    timestamp = input('请输入要判断的时间戳: ')
    print(is_recent_time(timestamp))