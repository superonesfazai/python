# coding:utf-8

'''
@author = super_fazai
@File    : requests阻塞异步导致同步问题.py
@connect : superonesfazai@gmail.com
'''

"""
类似问题:stackoverflow的解决方案
https://stackoverflow.com/questions/22190403/how-could-i-use-requests-in-asyncio
"""

from gc import collect
from fzutils.spider.async_always import *

async def test():
    loop = get_event_loop()
    print('项目start...')
    tasks = []
    for item in range(100):
        tasks.append(loop.create_task(task(item)))

    all_res = await async_wait_tasks_finished(tasks=tasks)

async def task(item):
    print('task {} start...'.format(item))
    body = await other_block_task()
    print('task {} over!! body: {}'.format(item, str(body)[:10]))

    return

async def other_block_task():
    """其他阻塞任务"""
    loop = get_event_loop()
    headers = {
        'authority': 'www.jianshu.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_pc_ua(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://www.jianshu.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'if-none-match': 'W/"4a9fde17dc47fa1c6e44b8952c88ecba"',
    }
    url = 'https://www.jianshu.com/p/63623c430e2b'
    # 即将会阻塞的函数, 开新的协程处理, 并异步等待直到返回结果
    body = await loop.run_in_executor(None, Requests.get_url_body, url, headers)
    try:
        del loop
    except:
        pass
    collect()

    return body

def main():
    loop = get_event_loop()
    loop.run_until_complete(test())

if __name__ == '__main__':
    main()