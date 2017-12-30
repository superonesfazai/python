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

spike_file_name_list = [
    'zhe_800_spike',
    'zhe_800_miaosha_real-times_update',
    'juanpi_spike',
    'juanpi_miaosha_real-times_update',
    'pinduoduo_spike',
    'pinduoduo_miaosha_real-times_update',
]

pintuan_file_name_list = [
    'zhe_800_pintuan',
    'zhe_800_pintuan_real-times_update',
    'juanpi_pintuan',
    'juanpi_pintuan_real-times_update',
]

real_file_name_list = [
    'zhe_800_real-times_update',
    'juanpi_real-times_update',
]

def auto_run(*params):
    print('开始执行秒杀脚本'.center(60, '*'))

    for item in spike_file_name_list:
        os.system('cd {0} && python3 {1}.py'.format(params[0], item))
        sleep(2.5)      # 避免同时先后启动先sleep下

    for item in pintuan_file_name_list:
        os.system('cd {0} && python3 {1}.py'.format(params[1], item))
        sleep(2.5)      # 避免同时先后启动先sleep下

    for item in real_file_name_list:
        os.system('cd {0} && python3 {1}.py'.format(params[2], item))
        sleep(2.5)  # 避免同时先后启动先sleep下

    print('脚本执行完毕'.center(60, '*'))

def main():
    spike_path = '~/myFiles/python/my_flask_server/spike_everything'
    pintuan_path = '~/myFiles/python/my_flask_server/pintuan_script'
    real_path = '~/myFiles/python/my_flask_server/real-times_update'

    auto_run(spike_path, pintuan_path, real_path)
    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()