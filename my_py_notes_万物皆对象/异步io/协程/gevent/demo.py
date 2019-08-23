# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
notice: 当我们在受限于网络或IO的函数中使用gevent，这些函数会被协作式的调度, gevent的真正能力会得到发挥
Gevent处理了所有的细节， 来保证你的网络库会在可能的时候，隐式交出greenlet上下文的执行权。
"""

from gevent.pool import Pool as GeventPool
from gevent import monkey
from gevent import Greenlet
from gevent import spawn as gevent_spawn
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

# 猴子补丁
# eg: 在进行IO操作时，默认切换协程
monkey.patch_all()

@catch_exceptions(default_res={})
def get_url_body(index):
    url = 'https://httpbin.org/get'
    body = Requests.get_url_body(
        url=url,
        ip_pool_type=tri_ip_pool,
        proxy_type=PROXY_TYPE_HTTPS,
        timeout=15,)
    data = json_2_dict(json_str=body)
    print('[{}] index: {}'.format(
        '+' if data != {} else '-',
        index,
    ))

    return data

if __name__ == '__main__':
    # 假如你的url写在文件中 用第一个参数传进来
    tasks = []
    for index in range(1, 50):
        print('create task[where index: {}] ...'.format(index))
        tasks.append(gevent_spawn(
            get_url_body,
            index,
        ))

    one_res = wait_for_every_greenlet_obj_run_over_and_get_tasks_res(
        tasks=tasks,
    )
    # pprint(one_res)