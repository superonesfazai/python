# coding:utf-8

'''
@author = super_fazai
@File    : yanxuan_real-times_update.py
@Time    : 2018/8/2 09:36
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from yanxuan_parse import YanXuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
from logging import (
    INFO,
    ERROR)
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TMALL_REAL_TIMES_SLEEP_TIME,)

from sql_str_controller import (
    yx_select_str_1,
    yx_update_str_2,)
from multiplex_code import (
    _get_sku_price_trans_record,
    _get_spec_trans_record,
    _get_stock_trans_record,)

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import (
    _get_price_change_info,
    get_shelf_time_and_delete_time,
    format_price_info_list,
)
from fzutils.common_utils import json_2_dict

def run_forever():
    while True:
        # ** 不能写成全局变量并放在循环中, 否则会一直记录到同一文件中
        my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/网易严选/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )

        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server._select_table(sql_str=yx_select_str_1))
        except TypeError:
            my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            my_lg.info(str(result))
            my_lg.info('--------------------------------------------------------')
            my_lg.info('总计待更新个数: {0}'.format(len(result)))

            my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            yanxuan = YanXuanParse(logger=my_lg)
            for item in result:  # 实时更新数据
                if index % 5 == 0:
                    try:
                        del yanxuan
                    except:
                        pass
                    yanxuan = YanXuanParse(logger=my_lg)
                    gc.collect()

                if index % 10 == 0:  # 每10次重连一次，避免单次长连无响应报错
                    my_lg.info('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    my_lg.info('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (str(item[1]), str(index)))
                    yanxuan._get_goods_data(goods_id=item[1])

                    data = yanxuan._deal_with_data()
                    if data != {}:
                        data['goods_id'] = item[1]
                        data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[2],
                            shelf_time=item[5],
                            delete_time=item[6])
                        if data.get('is_delete') == 1:  # 单独处理下架商品
                            my_lg.info('@@@ 该商品已下架...')
                            tmp_sql_server._update_table_2(sql_str=yx_update_str_2, params=(item[1],), logger=my_lg)
                            sleep(TMALL_REAL_TIMES_SLEEP_TIME)
                            continue

                        else:
                            price_info_list = old_sku_info = json_2_dict(item[7], default_res=[])
                            try:
                                old_sku_info = format_price_info_list(price_info_list=price_info_list, site_id=30)
                            except AttributeError:  # 处理已被格式化过的
                                pass
                            new_sku_info = format_price_info_list(data['price_info_list'], site_id=30)
                            data['_is_price_change'], data['sku_info_trans_time'], price_change_info = _get_sku_price_trans_record(
                                old_sku_info=old_sku_info,
                                new_sku_info=new_sku_info,
                                is_price_change=item[8] if item[8] is not None else 0,
                                db_price_change_info=json_2_dict(item[10], default_res=[]),
                                old_price_trans_time=item[13],
                            )
                            data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                                old_price=item[3],
                                old_taobao_price=item[4],
                                new_price=data['price'],
                                new_taobao_price=data['taobao_price'],
                                is_price_change=data['_is_price_change'],
                                price_change_info=price_change_info,
                            )
                            # 监控纯规格变动
                            data['is_spec_change'], data['spec_trans_time'] = _get_spec_trans_record(
                                old_sku_info=old_sku_info,
                                new_sku_info=new_sku_info,
                                is_spec_change=item[9] if item[9] is not None else 0,
                                old_spec_trans_time=item[14],)

                            # 监控纯库存变动
                            data['is_stock_change'], data['stock_trans_time'], data['stock_change_info'] = _get_stock_trans_record(
                                old_sku_info=old_sku_info,
                                new_sku_info=new_sku_info,
                                is_stock_change=item[11] if item[11] is not None else 0,
                                db_stock_change_info=json_2_dict(item[12], default_res=[]),
                                old_stock_trans_time=item[15],)

                        yanxuan.to_right_and_update_data(data, pipeline=tmp_sql_server)
                    else:  # 表示返回的data值为空值
                        my_lg.info('------>>>| 休眠8s中...')
                        sleep(8)

                else:  # 表示返回的data值为空值
                    my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
                    sleep(5)
                    pass
                index += 1
                gc.collect()
                sleep(TMALL_REAL_TIMES_SLEEP_TIME)

            my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)

        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(60)
        gc.collect()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    run_forever()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        run_forever()