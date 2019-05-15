# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

from tenacity import retry as tenacity_retry
from tenacity import (
    stop_after_delay,
    stop_after_attempt,)
from async_timeout import timeout as aio_timeout
from fzutils.spider.async_always import *
from fzutils.time_utils import fz_set_timeout
from asyncio import wait_for as async_wait_for

# 下面示例用于: 只一次成功退出 or 超时停止
@tenacity_retry(stop=(stop_after_delay(2) | stop_after_attempt(1)))
def stop_after_2_s_or_1_retries():
    print("Stopping after 2 seconds or 1 retries")
    sleep(3.)
    print('run over!')

    return True

# 函数超时退出
@fz_set_timeout(seconds=2)
def func_timeout_test():
    print('111')
    sleep(3)
    print('run over !')

    return True

async def async_stop_after_2_s_or_1_retries():
    async def run():
        print("Stopping after 2 seconds or 1 retries")
        await async_sleep(3)
        print('run over !')

        return 'success'

    for i in range(5):
        print('i: {}'.format(i))
        # 依赖async_timeout包的超时
        # async with aio_timeout(2) as cm:
        #     res = await run()
        # # bool, False表示超时
        # print(cm.expired)

        # 原生超时(推荐)
        res = []
        try:
            res = await async_wait_for(run(), timeout=2)
        except AsyncTimeoutError as e:
            print(e)

        print(res)

try:
    # 同步
    # res = stop_after_2_s_or_1_retries()
    # print(res)

    # 函数超时退出
    func_timeout_test()

    # 异步
    # loop = get_event_loop()
    # res = loop.run_until_complete(async_stop_after_2_s_or_1_retries(loop=loop))
except Exception as e:
    print('exception happen')
    print(e)

