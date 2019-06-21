# coding:utf-8

'''
@author = super_fazai
@File    : yanxuan_real-times_update.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from yanxuan_parse import YanXuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

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
    yx_select_str_1,
    yx_update_str_2,)
from multiplex_code import (
    _block_get_new_db_conn,
    _block_print_db_old_data,
    get_goods_info_change_data,
    BaseDbCommomGoodsInfoParamsObj,
)

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init

def run_forever():
    while True:
        # ** 不能写成全局变量并放在循环中, 否则会一直记录到同一文件中
        my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/网易严选/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR,)

        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(sql_cli._select_table(sql_str=yx_select_str_1))
        except TypeError:
            my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result, logger=my_lg)
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
                    collect()

                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, logger=my_lg, remainder=10)
                if sql_cli.is_connect_success:
                    my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (str(item[1]), str(index)))
                    yanxuan._get_goods_data(goods_id=item[1])

                    data = yanxuan._deal_with_data()
                    db_goods_info_obj = YXDbGoodsInfoObj(
                        item=item,
                        logger=my_lg)
                    if data != {}:
                        if data.get('is_delete') == 1:
                            # 单独处理下架商品
                            my_lg.info('@@@ 该商品已下架...')
                            sql_cli._update_table_2(
                                sql_str=yx_update_str_2,
                                params=(db_goods_info_obj.goods_id,),
                                logger=my_lg,)
                            sleep(TMALL_REAL_TIMES_SLEEP_TIME)
                            continue

                        else:
                            data = get_goods_info_change_data(
                                target_short_name='yx',
                                logger=my_lg,
                                data=data,
                                db_goods_info_obj=db_goods_info_obj,)

                        yanxuan.to_right_and_update_data(data, pipeline=sql_cli)
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

            my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)

        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(60)
        collect()

class YXDbGoodsInfoObj(BaseDbCommomGoodsInfoParamsObj):
    def __init__(self, item: list, logger=None):
        BaseDbCommomGoodsInfoParamsObj.__init__(
            self,
            item=item,
            logger=logger,
        )

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