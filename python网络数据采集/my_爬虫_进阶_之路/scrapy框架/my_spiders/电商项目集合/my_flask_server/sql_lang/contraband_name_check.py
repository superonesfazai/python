# coding:utf-8

'''
@author = super_fazai
@File    : contraband_name_check.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from multiplex_code import (
    CONTRABAND_GOODS_KEY_TUPLE,
)
from pprint import pprint
from fzutils.time_utils import get_shanghai_time

def goods_name_check_and_do_something():
    """
    违禁物品检测下架
    :return:
    """
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    sql_str0 = '''
    -- select count(*)
    select GoodsID, GoodsName, ConvertTime, IsDelete, delete_time, MainGoodsID
    from dbo.GoodsInfoAutoGet
    where '''
    sql_str1 = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s, delete_time=%s where GoodsID=%s'
    goods_name_like_str = ' or '.join(['GoodsName like %s' for index in range(0, len(CONTRABAND_GOODS_KEY_TUPLE))])
    sql_str0 += goods_name_like_str
    print(sql_str0)
    params = ['%{}%'.format(item) for item in CONTRABAND_GOODS_KEY_TUPLE]
    pprint(params)
    res = sql_cli._select_table(
        sql_str=sql_str0,
        params=params, )
    pprint(res)

    # 下架
    assert res is not None
    now_time = get_shanghai_time()
    for item in res:
        goods_id = item[0]
        print('goods_id: {}'.format(goods_id))
        sql_cli._update_table(
            sql_str=sql_str1,
            params=(now_time, now_time, goods_id)
        )

    try:
        del sql_cli
    except:
        pass

goods_name_check_and_do_something()