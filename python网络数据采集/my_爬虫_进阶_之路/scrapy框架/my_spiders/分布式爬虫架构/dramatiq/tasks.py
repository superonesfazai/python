# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
运行方式:
$ dramatiq tasks --watch .
"""

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results as DramatiqResults
from dramatiq.actor import Actor
from dramatiq import actor as dramatiq_actor
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_requests import PROXY_TYPE_HTTPS
from fzutils.spider.async_always import *

redis_broker = RedisBroker(
    url='redis://127.0.0.1:6379/0',)
result_backend = RedisBackend(
    url='redis://127.0.0.1:6379/1',
)
dramatiq.set_broker(redis_broker)
redis_broker.add_middleware(
    middleware=DramatiqResults(
        backend=result_backend))

@dramatiq_actor(
    broker=redis_broker,
    time_limit=1000 * 60,
    max_retries=None,
    max_age=1000 * 60 * 6,
    priority=0,                 # 默认值
    store_results=True,)
def get_url_body(url,
                 use_proxy=False,
                 proxy_type=PROXY_TYPE_HTTPS,
                 num_retries=6,):
    body = Requests.get_url_body(
        url=url,
        headers=get_random_headers(),
        use_proxy=use_proxy,
        ip_pool_type=tri_ip_pool,
        proxy_type=proxy_type,
        num_retries=num_retries,)
    # print(body)

    return body