# coding:utf-8

'''
@author = super_fazai
@File    : test_redis.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    RedisCli,)
from pprint import pprint

def test():
    """
    查看指定keys的更新时间点
    :return:
    """
    redis_cli = RedisCli()
    base_pattern = 'fzhook:tm0:'
    res = list(redis_cli.keys(pattern='fzhook:tm0:*'))
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    sql_str = 'select GoodsID, ModfiyTime from dbo.GoodsInfoAutoGet where GoodsID=%s'

    tmp_list = []
    for item in res:
        goods_id = item.replace(base_pattern, '')
        print('look goods_id: {} ...'.format(goods_id))
        tmp = sql_cli._select_table(
            sql_str=sql_str,
            params=(goods_id,))
        if tmp_list is not None:
            tmp_list.append({
                'goods_id': goods_id,
                'modify_time': tmp[0][1],
            })

    new_tmp_list = sorted(
        tmp_list,
        key=lambda item: item.get('modify_time', ''))
    pprint(new_tmp_list[0:200])

    try:
        del sql_cli
        del redis_cli
    except:
        pass

    return

test()
