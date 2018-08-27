# coding:utf-8

'''
@author = super_fazai
@File    : jd_real-times_update.py
@Time    : 2017/11/11 17:49
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from jd_parse import JdParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
from logging import INFO, ERROR
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import jd_select_str_1
from multiplex_code import get_sku_info_trans_record

from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import (
    _get_price_change_info,
    get_shelf_time_and_delete_time,
)
from fzutils.cp_utils import format_price_info_list
from fzutils.common_utils import json_2_dict
from fzutils.log_utils import set_logger

def run_forever():
    while True:
        my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/jd/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR)
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        # and GETDATE()-ModfiyTime>1 and IsDelete=0
        try:
            result = list(tmp_sql_server._select_table(sql_str=jd_select_str_1))
        except TypeError:
            my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            continue

        my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
        my_lg.info(str(result))
        my_lg.info('--------------------------------------------------------')
        my_lg.info('总计待更新个数:{}'.format(len(result)))

        my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
        index = 1

        # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
        jd = JdParse(logger=my_lg)
        for item in result:  # 实时更新数据
            # # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            # jd = JdParse()
            if index % 10 == 0:
                try: del jd
                except: pass
                gc.collect()
                jd = JdParse(logger=my_lg)

            if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                my_lg.info('正在重置，并与数据库建立新连接中...')
                tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                my_lg.info('与数据库的新连接成功建立...')

            if tmp_sql_server.is_connect_success:
                my_lg.info('------>>>| 正在更新的goods_id为({}) | --------->>>@ 索引值为({})'.format(item[1], index))
                tmp_item = []
                if item[0] == 7 or item[0] == 8:        # 从数据库中取出时，先转换为对应的类型
                    tmp_item.append(0)
                elif item[0] == 9:
                    tmp_item.append(1)
                elif item[0] == 10:
                    tmp_item.append(2)

                tmp_item.append(item[1])
                jd.get_goods_data(goods_id=tmp_item)
                data = jd.deal_with_data(goods_id=tmp_item)
                if data != {}:
                    data['goods_id'] = item[1]

                    data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                        tmp_data=data,
                        is_delete=item[2],
                        shelf_time=item[5],
                        delete_time=item[6])
                    my_lg.info('上架时间: {0}, 下架时间: {1}'.format(data['shelf_time'], data['delete_time']))

                    data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                        old_price=item[3],
                        old_taobao_price=item[4],
                        new_price=data['price'],
                        new_taobao_price=data['taobao_price'])

                    site_id = jd._from_jd_type_get_site_id_value(jd_type=data['jd_type'])
                    try:
                        old_sku_info = format_price_info_list(
                            price_info_list=json_2_dict(item[7]),
                            site_id=site_id)
                    except AttributeError:  # 处理已被格式化过的
                        old_sku_info = item[7]
                    data['_is_price_change'], data['sku_info_trans_time'] = get_sku_info_trans_record(
                        old_sku_info=old_sku_info,
                        new_sku_info=format_price_info_list(data['price_info_list'], site_id=site_id),
                        is_price_change=item[8] if item[8] is not None else 0
                    )

                    jd.to_right_and_update_data(data, pipeline=tmp_sql_server)
                else:  # 表示返回的data值为空值
                    pass
            else:  # 表示返回的data值为空值
                my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
                pass
            index += 1
            gc.collect()
            sleep(1.2)
        my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        try: del jd
        except: pass
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
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