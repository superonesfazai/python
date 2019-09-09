# coding:utf-8

'''
@author = super_fazai
@File    : just_fuck_run_2.py
@Time    : 2018/1/9 15:28
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from time import sleep
import re
import os

from fzutils.linux_utils import (
    daemon_init,
    process_exit,
)

tejia_file_name_list = [
    'taobao_tiantiantejia',
    # 'taobao_tiantiantejia_real-times_update',
]

logs_file_name_list = [
    'expired_logs_deal_with'
]

def run_one_file_name_list(path, file_name_list):
    for item in file_name_list:
        process_name = item + '.py'
        if process_exit(process_name) == 0:
            # 如果对应的脚本没有在运行, 则运行之
            os.system('cd {0} && python3 {1}.py'.format(path, item))
            sleep(2.5)      # 避免同时先后启动先sleep下
        else:
            print(process_name + '脚本已存在!')

def auto_run(*params):
    print('开始执行脚本'.center(60, '*'))

    run_one_file_name_list(path=params[0], file_name_list=tejia_file_name_list)
    run_one_file_name_list(path=params[1], file_name_list=logs_file_name_list)

    print('脚本执行完毕'.center(60, '*'))

def main_2():
    while True:
        tejia_path = '~/myFiles/python/my_flask_server/tejia'
        logs_path = '~/myFiles/python/my_flask_server/logs'

        auto_run(tejia_path, logs_path)
        print(' Money is on the way! '.center(100, '*'))

        sleep(2)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    main_2()

if __name__ == '__main__':
    main()