# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/16 18:53
@connect : superonesfazai@gmail.com
'''

from ray import init as ray_init
from ray import remote as ray_remote
from ray import get as ray_get
from ray import wait as ray_wait
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_requests import PROXY_TYPE_HTTPS
from fzutils.spider.async_always import *

# # 通过ray实现分布式并发执行f函数
# @ray_remote
# def f():
#     print('sleep 1s ...')
#     sleep(1)
#     return 1

# ray_init()
# _ = ray_get([f.remote() for item in range(100)])

ray_init()

@ray_remote
def get_url_body(url,
                 use_proxy=False,
                 proxy_type=PROXY_TYPE_HTTPS,
                 num_retries=6,):
    print('url: {}'.format(url))
    body = Requests.get_url_body(
        url=url,
        headers=get_random_headers(),
        use_proxy=use_proxy,
        ip_pool_type=tri_ip_pool,
        proxy_type=proxy_type,
        num_retries=num_retries,)
    # print(body)

    return body

@func_time
def main():
    target_url = 'http://0.0.0.0:8001/get_all'
    tasks = []
    for index in range(200):
        task = get_url_body.remote(url=target_url)
        # print(task)
        tasks.append(task)

    # ready_ids, remaining_ids = ray_wait(object_ids=tasks)
    # pprint(ready_ids)
    # pprint(remaining_ids)

    # 等待所有执行完毕并获取结果
    one_res = ray_get(object_ids=tasks)
    pprint(one_res)

if __name__ == '__main__':
    main()