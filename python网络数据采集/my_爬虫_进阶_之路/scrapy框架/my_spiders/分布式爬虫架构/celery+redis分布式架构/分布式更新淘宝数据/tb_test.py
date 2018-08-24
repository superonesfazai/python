# coding:utf-8

'''
@author = super_fazai
@File    : tb_test.py
@Time    : 2018/7/1 19:26
@connect : superonesfazai@gmail.com
'''

from taobao_tasks import TaoBaoLoginAndParse
from celery.utils.log import get_task_logger
import redis

from fzutils.data.pickle_utils import deserializate_pickle_object

logger = get_task_logger('tb')
# print(type(logger))
tb = TaoBaoLoginAndParse(logger=logger)

def get_tb_process_data(tb_object, url):
    goods_id = tb_object.get_goods_id_from_url(url)
    _ = tb_object.get_goods_data.apply_async(args=(tb_object, goods_id,),).get(timeout=2)
    if _ != {}:
        _ = tb_object.deal_with_data.apply_async(args=(tb_object, goods_id, _),)

    else:
        logger.error('get_goods_data得到的data为空dict!')
        return None

    return _

if __name__ == '__main__':
    url = 'https://item.taobao.com/item.htm?id=534498954634'

    _r = get_tb_process_data(tb_object=tb, url=url)

    # logger.info(_r.get(timeout=2))
    _r.get(timeout=2)
    print('tasks的id: {0}, status: {1}'.format(_r.id, _r.status))

    # 从redis获取结果
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis_cli = redis.StrictRedis(connection_pool=pool)
    _k = 'celery-task-meta-' + str(_r)

    # 将redis里面的序列化python对象进行反序列化
    result = deserializate_pickle_object(redis_cli.get(_k))
    if result.get('status', '') == 'SUCCESS':
        result = result.get('result', '{}')
        print(result)

    else:
        print('获取失败!')


