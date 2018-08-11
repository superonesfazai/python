# coding:utf-8

'''
@author = super_fazai
@File    : just_fuck_run.py
@Time    : 2017/11/29 13:46
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from time import sleep
import re
import os

from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import (
    daemon_init,
    process_exit,
    kill_process_by_name,
)

spike_file_name_list = [
    'zhe_800_spike',
    'zhe_800_miaosha_real-times_update',
    'juanpi_spike',
    'juanpi_miaosha_real-times_update',
    # 'pinduoduo_spike',
    # 'pinduoduo_miaosha_real-times_update',
    'mia_spike',
    'mia_miaosha_real-times_update',
    'mogujie_spike',
    'mogujie_miaosha_real-times_update',
    'chuchujie_spike',
    'chuchujie_miaosha_real-times_update',
    'jumeiyoupin_spike',
    'jumeiyoupin_miaosha_real-times_update',
]

pintuan_file_name_list = [
    'zhe_800_pintuan',
    'zhe_800_pintuan_real-times_update',
    'juanpi_pintuan',
    'juanpi_pintuan_real-times_update',
    'mia_pintuan',
    'mia_pintuan_real-times_update',
    'mogujie_pintuan',
    'mogujie_pintuan_real-times_update',
    'jumeiyoupin_pintuan',
    'jumeiyoupin_pintuan_real-times_update',
]

real_file_name_list = [
    'zhe_800_real-times_update',
    'juanpi_real-times_update',
    # 'tmall_real-times_update',
    # 'jd_real-times_update',
    'ali_1688_real-times_update',
    'vip_real-times_update',
    'kaola_real-times_update',
    'yanxuan_real-times_update',
]

other_file_name_list = [
    # 'sina_head_img_and_nick_name',
    # 'bilibili_user',
]

logs_file_name_list = [
    'expired_logs_deal_with'
]

night_run_file_name_list = [    # 只在晚上run
    'ali_1688_real-times_update',
]

# night 运行时间
night_run_time = ['21', '22', '23', '00', '01', '02', '03', '04', '05', '06', '07',]

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
    print('开始执行秒杀脚本'.center(60, '*'))

    run_one_file_name_list(path=params[0], file_name_list=spike_file_name_list)
    run_one_file_name_list(path=params[1], file_name_list=pintuan_file_name_list)
    run_one_file_name_list(path=params[2], file_name_list=real_file_name_list)
    run_one_file_name_list(path=params[3], file_name_list=other_file_name_list)
    run_one_file_name_list(path=params[4], file_name_list=logs_file_name_list)

    if str(get_shanghai_time())[11:13] not in night_run_time:
        # kill冲突process
        [kill_process_by_name(process_name) for process_name in night_run_file_name_list]

    print('脚本执行完毕'.center(60, '*'))

def main_2():
    while True:
        spike_path = '~/myFiles/python/my_flask_server/spike_everything'
        pintuan_path = '~/myFiles/python/my_flask_server/pintuan_script'
        real_path = '~/myFiles/python/my_flask_server/real-times_update'
        other_path = '~/myFiles/python/my_flask_server/other_scripts'
        logs_path = '~/myFiles/python/my_flask_server/logs'

        auto_run(spike_path, pintuan_path, real_path, other_path, logs_path)
        print(' Money is on the way! '.center(100, '*'))

        sleep(60*15)

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