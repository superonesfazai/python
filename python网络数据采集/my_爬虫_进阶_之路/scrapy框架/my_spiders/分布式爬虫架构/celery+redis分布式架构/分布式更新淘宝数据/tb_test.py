# coding:utf-8

'''
@author = super_fazai
@File    : tb_test.py
@Time    : 2018/7/1 19:26
@connect : superonesfazai@gmail.com
'''

from .taobao_tasks import TaoBaoLoginAndParse
from celery.utils.log import get_task_logger

logger = get_task_logger('tb')

def get_tb_result(url):
    result = TaoBaoLoginAndParse(logger=logger).__call__(url=url).delay()

    return result

if __name__ == '__main__':
    url = 'https://item.taobao.com/item.htm?id=534498954634'
    _r = get_tb_result(url)

    print(_r.id)
    print(_r.status)
    print(_r.get(timeout=1))

    # 从redis获取结果
    import redis

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis_cli = redis.StrictRedis(connection_pool=pool)
    _k = 'celery-task-meta-' + str(_r)

    print(redis_cli.get(_k).decode('utf-8'))
