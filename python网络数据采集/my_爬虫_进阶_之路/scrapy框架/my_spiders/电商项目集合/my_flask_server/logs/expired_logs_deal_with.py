# coding:utf-8

'''
@author = super_fazai
@File    : expired_logs_deal_with.py
@Time    : 2018/3/31 11:22
@connect : superonesfazai@gmail.com
'''

"""
清除日志文件夹中电商项目下的过期日志[本地/服务器]
"""

import sys
sys.path.append('..')

from settings import (
    MY_SPIDER_LOGS_PATH,
    IS_BACKGROUND_RUNNING,)
import glob
import os
import datetime
from fzutils.spider.async_always import *

async def get_now_time_from_pytz():
    '''
    得到log文件的时间名字
    :return: 格式: 2016-03-25 类型datetime
    '''
    _ = str(get_shanghai_time())[0:10].split('-')
    _ = datetime.datetime(
        year=int(_[0]),
        month=int(_[1]),
        day=int(_[2]))

    return _

async def deal_with_logs():
    # 为了类似mac中'2019-12-10.txt.3'也能匹配到
    file_re_path = MY_SPIDER_LOGS_PATH + '/*/*/*.txt*'
    for item in glob.iglob(pathname=file_re_path):
        # iglob() 获取一个可编历对象，使用它可以逐个获取匹配的文件路径名
        # print(item)
        file_name_contain_extension_name = os.path.basename(item)   # 2016-02-01.txt
        # print(file_name_contain_extension_name)
        try:
            file_name = os.path.splitext(file_name_contain_extension_name)[0]   # 2016-03-30
            # print('file_name: {}'.format(file_name))
            # 处理mac中类似'2019-12-10.txt.3', 经过上面划分为('2019-12-10.txt', '.3')
            file_name = file_name.replace('.txt', '')
        except IndexError:
            continue

        file_name_list = file_name.split('-')
        file_name_date = datetime.datetime(
            year=int(file_name_list[0]),
            month=int(file_name_list[1]),
            day=int(file_name_list[2]))
        # print(str(file_name_date))
        now_date = await get_now_time_from_pytz()
        if file_name_date == now_date:
            print('当天日志, 跳过!')
            continue
        try:
            # 当前日期 - 文件名的日期 的相差的day
            result = int(str(now_date - file_name_date).split(' ')[0])
        except IndexError:
            continue

        if result > 6:
            os.remove(item)
            print('删除过期日志文件 [%s] 成功!' % item)
        else:
            print('未过期跳过!')

    return True

def just_fuck_run():
    while True:
        loop = get_event_loop()
        loop.run_until_complete(deal_with_logs())
        try:
            loop.close()
        except:
            pass
        collect()
        sleep(60*60)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()

