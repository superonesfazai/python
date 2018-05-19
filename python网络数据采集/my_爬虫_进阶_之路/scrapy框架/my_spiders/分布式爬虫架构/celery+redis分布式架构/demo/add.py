# coding:utf-8

'''
@author = super_fazai
@File    : add.py
@Time    : 2018/5/19 15:07
@connect : superonesfazai@gmail.com
'''

from tasks import add

def notify(a, b):
    result = add.delay(a, b)

    # add.apply_async(args=(a, b))  # 上面等价于下面

    return result

if __name__ == '__main__':
    _r = notify(6, 7)
    print(_r.id)    # eg: a8eeb34e-01ef-4719-8fc4-a6e4d80e5cd5
    print(_r.status)
    print(_r.get(timeout=1))

    # 从redis获取结果
    import redis

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis_cli = redis.StrictRedis(connection_pool=pool)
    _k = 'celery-task-meta-' + str(_r)

    print(redis_cli.get(_k))