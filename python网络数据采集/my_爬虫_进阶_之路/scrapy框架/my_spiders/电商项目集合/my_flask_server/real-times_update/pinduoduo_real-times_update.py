# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_real-times_update.py
@Time    : 2017/11/30 09:46
@connect : superonesfazai@gmail.com
'''

"""
pdd 退款过多, 不再维护
"""

import sys
sys.path.append('..')

from pinduoduo_parse import PinduoduoParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
from settings import IS_BACKGROUND_RUNNING

from sql_str_controller import pd_select_str_1
from multiplex_code import (
    _get_sku_price_trans_record,
    _get_spec_trans_record,
    _get_stock_trans_record,
    _block_print_db_old_data,
    _block_get_new_db_conn,
    _get_price_change_info,
    format_price_info_list,
)

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import (
    get_shelf_time_and_delete_time,
)
from fzutils.common_utils import json_2_dict

def run_forever():
    while True:
        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(sql_cli._select_table(sql_str=pd_select_str_1))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result,)
            index = 1
            for item in result:  # 实时更新数据
                # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                pinduoduo = PinduoduoParse()
                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50)
                if sql_cli.is_connect_success:
                    print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                    pinduoduo.get_goods_data(goods_id=item[0])
                    data = pinduoduo.deal_with_data()
                    if data != {}:
                        data['goods_id'] = item[0]
                        data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[1],
                            shelf_time=item[4],
                            delete_time=item[5])
                        price_info_list = old_sku_info = json_2_dict(item[6], default_res=[])
                        try:
                            old_sku_info = format_price_info_list(price_info_list=price_info_list, site_id=13)
                        except AttributeError:  # 处理已被格式化过的
                            pass
                        new_sku_info = format_price_info_list(data['price_info_list'], site_id=13)
                        data['_is_price_change'], data['sku_info_trans_time'], price_change_info = _get_sku_price_trans_record(
                            old_sku_info=old_sku_info,
                            new_sku_info=new_sku_info,
                            is_price_change=item[7] if item[7] is not None else 0,
                            db_price_change_info=json_2_dict(item[9], default_res=[]),
                            old_price_trans_time=item[12])
                        data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                            old_price=item[2],
                            old_taobao_price=item[3],
                            new_price=data['price'],
                            new_taobao_price=data['taobao_price'],
                            is_price_change=data['_is_price_change'],
                            price_change_info=price_change_info)
                        # 监控纯规格变动
                        data['is_spec_change'], data['spec_trans_time'] = _get_spec_trans_record(
                            old_sku_info=old_sku_info,
                            new_sku_info=new_sku_info,
                            is_spec_change=item[8] if item[8] is not None else 0,
                            old_spec_trans_time=item[13])

                        # 监控纯库存变动
                        data['is_stock_change'], data['stock_trans_time'], data['stock_change_info'] = _get_stock_trans_record(
                            old_sku_info=old_sku_info,
                            new_sku_info=new_sku_info,
                            is_stock_change=item[10] if item[10] is not None else 0,
                            db_stock_change_info=json_2_dict(item[11], default_res=[]),
                            old_stock_trans_time=item[14])

                        pinduoduo.to_right_and_update_data(data, pipeline=sql_cli)
                    else:  # 表示返回的data值为空值
                        pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
        gc.collect()

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    run_forever()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        run_forever()
