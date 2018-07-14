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
    # 'taobao_tiantiantejia',
    'taobao_tiantiantejia_real-times_update',
]

logs_file_name_list = [
    'expired_logs_deal_with',
]

def run_one_file_name_list(path, file_name_list):
    for item in file_name_list:
        process_name = item + '.py'
        if process_exit(process_name) == 0:
            # 如果对应的脚本没有在运行, 则运行之
            os.system('cd {0} && python3 {1}.py'.format(path, item))
            sleep(2.5)  # 避免同时先后启动先sleep下
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
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    main_2()


if __name__ == '__main__':
    main()