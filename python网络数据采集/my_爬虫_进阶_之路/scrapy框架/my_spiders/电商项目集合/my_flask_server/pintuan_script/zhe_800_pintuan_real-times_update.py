# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_pintuan_real-times_update.py
@Time    : 2017/12/19 11:10
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from zhe_800_pintuan_parse import Zhe800PintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from gc import collect
from time import sleep
import re
from settings import (
    IS_BACKGROUND_RUNNING,
    ZHE_800_PINTUAN_SLEEP_TIME,)

from sql_str_controller import (
    z8_delete_str_1,
    z8_select_str_2,
    z8_update_str_4,)
from multiplex_code import (
    _block_print_db_old_data,
    _block_get_new_db_conn,
    _handle_goods_shelves_in_auto_goods_table,
)

from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import daemon_init

def run_forever():
    while True:
        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            sql_cli._delete_table(sql_str=z8_delete_str_1)
            result = list(sql_cli._select_table(sql_str=z8_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            for item in result:  # 实时更新数据
                goods_id = item[0]
                db_is_delete = item[1]
                # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                zhe_800_pintuan = Zhe800PintuanParse()
                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50,)
                if index % 300 == 0:    # 每更新300个，休眠3分钟
                    sleep_time = 3 * 60
                    sleep(sleep_time)
                    print('休眠{}s中...'.format(sleep_time))

                if sql_cli.is_connect_success:
                    tmp_tmp = zhe_800_pintuan.get_goods_data(goods_id=goods_id)
                    # 不用这个了因为会影响到正常情况的商品
                    try:        # 单独处理商品页面不存在的情况
                        if isinstance(tmp_tmp, str) and re.compile(r'^ze').findall(tmp_tmp) != []:
                            _handle_goods_shelves_in_auto_goods_table(
                                goods_id=goods_id,
                                update_sql_str=z8_update_str_4,
                                sql_cli=sql_cli,
                            )
                            sleep(ZHE_800_PINTUAN_SLEEP_TIME)
                            continue
                        else:
                            pass
                    except:
                        pass

                    data = zhe_800_pintuan.deal_with_data()
                    if data != {}:
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                        data['goods_id'] = goods_id

                        if db_is_delete == 1:
                            print('该goods_id[{0}]已过期!'.format(goods_id))
                            _handle_goods_shelves_in_auto_goods_table(
                                goods_id=goods_id,
                                update_sql_str=z8_update_str_4,
                                sql_cli=sql_cli,
                            )
                        else:
                            zhe_800_pintuan.to_right_and_update_data(data=data, pipeline=sql_cli)
                    else:  # 表示返回的data值为空值
                        pass

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                try:
                    del zhe_800_pintuan
                except:
                    pass
                collect()
                sleep(ZHE_800_PINTUAN_SLEEP_TIME)
            print('全部数据更新完毕'.center(100, '#'))

        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(10 * 60)
        collect()

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
