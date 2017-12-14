# coding:utf-8

'''
@author = super_fazai
@File    : just_fuck_run.py
@Time    : 2017/11/29 13:46
@connect : superonesfazai@gmail.com
'''

import os
from time import sleep
import datetime
import re

file_name_list = [
    'zhe_800_spike',
    'zhe_800_miaosha_real-times_update',
    'juanpi_spike',
    'juanpi_miaosha_real-times_update',
    'pinduoduo_spike',
    'pinduoduo_miaosha_real-times_update',
]

def auto_run(path):
    print('开始执行秒杀脚本'.center(60, '*'))

    for item in file_name_list:
        os.system('cd {0} && python3 {1}.py'.format(path, item))
        sleep(2.5)      # 避免同时先后启动先sleep下
    print('脚本执行完毕'.center(60, '*'))

def main():
    python_path = '~/myFiles/python/my_flask_server/spike_everything'

    auto_run(python_path)
    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()