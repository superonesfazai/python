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
    # 'pinduoduo_spike',                        # 不维护
    # 'pinduoduo_miaosha_real-times_update',
    'mia_spike',
    'mia_miaosha_real-times_update',
    # 'mogujie_spike',                          # 不维护
    # 'mogujie_miaosha_real-times_update',
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
    # 'mogujie_pintuan',                        # 不维护
    # 'mogujie_pintuan_real-times_update',
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
    'youpin_real-times_update',
    'mia_real-times_update',
]

other_file_name_list = [
    # 'sina_head_img_and_nick_name',
    # 'bilibili_user',
]

logs_file_name_list = [
    'expired_logs_deal_with'
]

zwm_file_name_list = [
    # 'zwm_spider',
    # 'new_my_server',
]

# 只在晚上run
night_run_file_name_list = [
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
    run_one_file_name_list(path=params[5], file_name_list=zwm_file_name_list)

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
        zwm_path = '~/myFiles/python/my_flask_server'

        auto_run(spike_path, pintuan_path, real_path, other_path, logs_path, zwm_path)
        print(' Money is on the way! '.center(100, '*'))

        sleep(60*1)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    main_2()

if __name__ == '__main__':
    main()