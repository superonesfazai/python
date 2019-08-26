# coding:utf-8

'''
@author = super_fazai
@File    : just_fuck_run_tmall.py
@Time    : 2018/4/17 14:01
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import os
from fzutils.spider.async_always import *

tejia_file_name_list = [
    # 'taobao_tiantiantejia',
    # 'taobao_tiantiantejia_real-times_update',
]

spike_file_name_list = [
    'taobao_qianggou_spike',
    'taobao_qianggou_miaosha_real-times_update',
]

logs_file_name_list = [
    'expired_logs_deal_with',
]

server_file_name_list = [
    'new_my_server',
]

real_file_name_list = [
    # server上不进行更新，放在本地更新
    # 'tmall_real-times_update',
]

night_run_file_name_list = [    # 只在晚上run
    # server上不进行更新，放在本地更新
    # 'tmall_real-times_update',
]
# real-times脚本晚上运行时间
night_run_time = ['21', '22', '23', '00', '01', '02', '03', '04', '05', '06',]

def run_one_file_name_list(path, file_name_list):
    for item in file_name_list:
        if item in night_run_file_name_list \
                and str(get_shanghai_time())[11:13] not in night_run_time:
            print('{0}.py不在运行时间点...此处跳过!'.format(item))
            pass
        else:
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
    run_one_file_name_list(path=params[3], file_name_list=server_file_name_list)

    [kill_process_by_name(process_name) for process_name in spike_file_name_list[1:]]   # 不杀spike
    # 运行tmall常规商品更新script
    run_one_file_name_list(path=params[2], file_name_list=real_file_name_list)

    if str(get_shanghai_time())[11:13] not in night_run_time:
        # kill冲突process
        [kill_process_by_name(process_name) for process_name in night_run_file_name_list]

    print('脚本执行完毕'.center(60, '*'))

def main_2():
    while True:
        tejia_path = '~/myFiles/python/my_flask_server/tejia'
        logs_path = '~/myFiles/python/my_flask_server/logs'
        real_path = '~/myFiles/python/my_flask_server/real-times_update'
        server_path = '~/myFiles/python/my_flask_server'
        spike_path = '~/myFiles/python/my_flask_server/spike_everything'

        auto_run(tejia_path, logs_path, real_path, server_path, spike_path)
        print(' Money is on the way! '.center(100, '*'))

        sleep(1*60)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    main_2()

if __name__ == '__main__':
    main()