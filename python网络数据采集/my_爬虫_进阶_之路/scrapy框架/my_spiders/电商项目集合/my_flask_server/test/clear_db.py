# coding:utf-8

'''
@author = super_fazai
@File    : clear_db.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from time import sleep
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

def clear_db():
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    # 清理mia_pintuan
    who_is = 'mia_pintuan'
    print('获取 {} 目标数据中...'.format(who_is))
    mia_db_target_goods_id_list = sql_cli._select_table(
        sql_str='''
        select goods_id
        from.dbo.mia_pintuan
        where 
        (MainGoodsID is null and miaosha_begin_time < GETDATE()-60)
        -- 清掉已下架的且被后台转换的data
        or (MainGoodsID is not null and is_delete=1 and ConvertTime > modfiy_time)
        ''')
    _len = len(mia_db_target_goods_id_list)
    print('Got {} target_data len: {}'.format(who_is, _len))
    for item in mia_db_target_goods_id_list:
        goods_id = item[0]
        res = sql_cli._delete_table(
            sql_str='delete from dbo.mia_pintuan where goods_id=%s',
            params=(goods_id,))
        print('[{}] [{}, rest_num: {}] deleting row where goods_id: {} ...'.format(
            '+' if res else '-',
            who_is,
            _len,
            goods_id,))
        _len -= 1
    print('clear {} over!'.format(who_is))
    sleep(2.)

    try:
        del sql_cli
        del mia_db_target_goods_id_list
    except:
        pass
    collect()

if __name__ == '__main__':
    clear_db()