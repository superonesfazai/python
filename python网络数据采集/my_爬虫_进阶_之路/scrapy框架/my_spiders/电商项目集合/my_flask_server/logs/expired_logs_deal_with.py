# coding:utf-8

'''
@author = super_fazai
@File    : expired_logs_deal_with.py
@Time    : 2018/3/31 11:22
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from settings import (
    MY_SPIDER_LOGS_PATH,
    IS_BACKGROUND_RUNNING,)
import glob, gc
import asyncio
from time import sleep
import os
import datetime

from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import (
    restart_program,
    daemon_init,)

async def get_now_time_from_pytz():
    '''
    得到log文件的时间名字
    :return: 格式: 2016-03-25 类型datetime
    '''
    _ = str(get_shanghai_time())[0:10].split('-')
    _ = datetime.datetime(year=int(_[0]), month=int(_[1]), day=int(_[2]))

    return _

async def deal_with_logs():
    file_re_path = MY_SPIDER_LOGS_PATH + '/*/*/*.txt'
    for item in glob.iglob(pathname=file_re_path):  # iglob() 获取一个可编历对象，使用它可以逐个获取匹配的文件路径名。
        # print(item)
        file_name_contain_extension_name = os.path.basename(item)   # 2016-02-01.txt
        try:
            file_name = os.path.splitext(file_name_contain_extension_name)[0]   # 2016-03-30
            # print(file_name)
        except IndexError:
            continue

        file_name_list = file_name.split('-')
        file_name_date = datetime.datetime(year=int(file_name_list[0]), month=int(file_name_list[1]), day=int(file_name_list[2]))
        now_date = await get_now_time_from_pytz()
        if file_name_date == now_date:
            print('当天日志, 跳过!')
            continue
        try: result = int(str(now_date - file_name_date).split(' ')[0])     # 当前日期 - 文件名的日期 的相差的day
        except IndexError: continue

        if result > 6:
            os.remove(item)
            print('删除过期日志文件 [%s] 成功!' % item)
        else:
            print('未过期跳过!')

    return True

def just_fuck_run():
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(deal_with_logs())
        try: loop.close()
        except: pass
        gc.collect()
        sleep(60*60)

        restart_program()       # 通过这个重启环境, 避免log重复打印

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()

