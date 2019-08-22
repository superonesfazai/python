# coding:utf-8

'''
@author = super_fazai
@File    : just_fck_run_local.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')
from os import system
from fzutils.spider.async_always import *

logs_file_name_list = [
    # 'expired_logs_deal_with',
]

real_file_name_list = [
    # server上不进行更新，放在本地更新
    'tmall_real-times_update',
    # 'taobao_real-times_update',
]

# 只在晚上run
night_run_file_name_list = []
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
                system('cd {0} && python3 {1}.py'.format(path, item))
                sleep(2.5)  # 避免同时先后启动先sleep下
            else:
                print(process_name + '脚本已存在!')

def auto_run(*params):
    print('开始执行脚本'.center(60, '*'))

    run_one_file_name_list(path=params[0], file_name_list=logs_file_name_list)
    run_one_file_name_list(path=params[1], file_name_list=real_file_name_list)

    if str(get_shanghai_time())[11:13] not in night_run_time:
        # kill冲突process
        [kill_process_by_name(process_name) for process_name in night_run_file_name_list]

    print('脚本执行完毕'.center(60, '*'))

def main_2():
    while True:
        logs_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server/logs'
        real_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server/real-times_update'

        auto_run(logs_path, real_path)
        print(' Money is on the way! '.center(100, '*'))
        sleep(30)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    main_2()

if __name__ == '__main__':
    main()