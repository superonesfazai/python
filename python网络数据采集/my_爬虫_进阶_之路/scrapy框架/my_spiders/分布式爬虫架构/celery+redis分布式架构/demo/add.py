# coding:utf-8

'''
@author = super_fazai
@File    : add.py
@connect : superonesfazai@gmail.com
'''

import redis
from tasks import (
    add,
    test_async,)

def notify(a, b):
    res = add.delay(a, b)
    # res = add.apply_async(args=(a, b))  # 上面等价于下面

    return res

def test_notify():
    _r = notify(6, 7)
    print(_r.id)  # eg: a8eeb34e-01ef-4719-8fc4-a6e4d80e5cd5
    print(_r.status)
    print(_r.get(timeout=1))

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis_cli = redis.StrictRedis(connection_pool=pool)
    _k = 'celery-task-meta-' + str(_r)

    print(redis_cli.get(_k).decode('utf-8'))

def async_test():
    res = test_async.apply_async()
    print(res)

    return

if __name__ == '__main__':
    # test_notify()
    async_test()