# coding:utf-8

'''
@author = super_fazai
@File    : my_utils.py
@Time    : 2018/7/1 18:28
@connect : superonesfazai@gmail.com
'''
import pytz
import datetime
import re

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

