# coding:utf-8

'''
@author = super_fazai
@File    : mia_real-times_update.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from mia_parse import MiaParse

from gc import collect
from time import sleep
from logging import (
    INFO,
    ERROR)
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TMALL_REAL_TIMES_SLEEP_TIME,)

from sql_str_controller import (
    mia_select_str_5,
    mia_update_str_5,)
from multiplex_code import (
    _block_print_db_old_data,
    _block_get_new_db_conn,
    _handle_goods_shelves_in_auto_goods_table,
    get_goods_info_change_data,
    MIADbGoodsInfoObj,
)

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,)
from fzutils.linux_utils import daemon_init
from fzutils.common_utils import json_2_dict
from fzutils.safe_utils import get_uuid1

def run_forever():
    while True:
        # ** 不能写成全局变量并放在循环中, 否则会一直记录到同一文件中
        my_lg = set_logger(
            logger_name=get_uuid1(),
            log_file_name=MY_SPIDER_LOGS_PATH + '/蜜芽/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR,)

        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(sql_cli._select_table(sql_str=mia_select_str_5))
        except TypeError:
            my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result, logger=my_lg)
            index = 1
            mia = MiaParse()
            for item in result:
                goods_id = item[1]
                if index % 5 == 0:
                    try:
                        del mia
                    except: pass
                    mia = MiaParse()
                    collect()

                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, logger=my_lg, remainder=10)
                if sql_cli.is_connect_success:
                    my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (str(goods_id), str(index)))
                    mia.get_goods_data(goods_id=goods_id)
                    data = mia.deal_with_data()
                    db_goods_info_obj = MIADbGoodsInfoObj(item=item, logger=my_lg)
                    if data != {}:
                        if data.get('is_delete') == 1:  # 单独处理下架商品
                            my_lg.info('@@@ 该商品已下架...')
                            _handle_goods_shelves_in_auto_goods_table(
                                goods_id=goods_id,
                                logger=my_lg,
                                sql_cli=sql_cli,)
                            sleep(TMALL_REAL_TIMES_SLEEP_TIME)
                            continue

                        else:
                            data = get_goods_info_change_data(
                                target_short_name='mia',
                                logger=my_lg,
                                data=data,
                                db_goods_info_obj=db_goods_info_obj,)

                        mia._to_right_and_update_data(data, pipeline=sql_cli)
                    else:  # 表示返回的data值为空值
                        my_lg.info('------>>>| 休眠8s中...')
                        sleep(8)

                else:  # 表示返回的data值为空值
                    my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
                    sleep(5)
                    pass
                index += 1
                collect()
                sleep(TMALL_REAL_TIMES_SLEEP_TIME)

            my_lg.info('全部数据更新完毕'.center(100, '#'))

        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5 * 60)
        try:
            del my_lg
        except:
            pass
        collect()

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