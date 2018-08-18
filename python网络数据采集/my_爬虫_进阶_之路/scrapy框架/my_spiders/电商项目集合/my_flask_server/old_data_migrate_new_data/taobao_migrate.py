# coding:utf-8

'''
@author = super_fazai
@File    : taobao_migrate.py
@Time    : 2018/3/14 14:10
@connect : superonesfazai@gmail.com
'''

"""
将老表中的goods更新到新表中进行上下架监控
"""

import sys
sys.path.append('..')

from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline, SqlPools
from settings import TAOBAO_REAL_TIMES_SLEEP_TIME
import gc
from time import sleep
import re, pytz, datetime
from settings import IS_BACKGROUND_RUNNING

from sql_str_controller import (
    tb_select_str_1,
    tb_select_str_2,
)

from fzutils.linux_utils import daemon_init
from fzutils.time_utils import get_shanghai_time

def run_forever():
    #### 实时更新数据
    while True:
        # tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        tmp_sql_server = SqlPools()  # 使用sqlalchemy管理数据库连接池
        tmp_sql_server_2 = SqlServerMyPageInfoSaveItemPipeline()

        try:
            # result = list(tmp_sql_server.select_taobao_all_goods_id())
            result = tmp_sql_server._select_table(sql_str=tb_select_str_1, params=None)
            result_2 = list(tmp_sql_server_2._select_table(sql_str=tb_select_str_2, params=None))
            # print(result_2)
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
            result_2 = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result_2)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1

            new_table_ali_1688_all_goods_id_list = [item[0] for item in result]
            for item in result_2:  # 实时更新数据
                taobao = TaoBaoLoginAndParse()
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    # try:
                    #     del tmp_sql_server
                    # except:
                    #     pass
                    # gc.collect()
                    tmp_sql_server_2 = SqlServerMyPageInfoSaveItemPipeline()
                    tmp_sql_server = SqlPools()

                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    goods_id = taobao.get_goods_id_from_url(item[0])
                    if goods_id == '':
                        print('@@@ 原商品的地址为: ', item[0])
                        continue
                    else:
                        if goods_id in new_table_ali_1688_all_goods_id_list:
                            print('该goods_id已经存在于数据库中, 此处跳过!')
                            continue

                        else:
                            print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                            tt = taobao.get_goods_data(goods_id)
                            if tt.get('is_delete') == 1:    # 处理已下架的但是还是要插入的
                                tt['goods_id'] = goods_id
                                tt['goods_url'] = 'https://item.taobao.com/item.htm?id=' + str(goods_id)
                                tt['username'] = '18698570079'
                                tt['main_goods_id'] = item[1]

                                # print('------>>>| 爬取到的数据为: ', data)
                                taobao.old_taobao_goods_insert_into_new_table(data=tt, pipeline=tmp_sql_server_2)

                                index += 1
                                gc.collect()
                                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
                                continue
                            else:
                                pass

                            data = taobao.deal_with_data(goods_id=goods_id)
                            if data != {}:
                                data['goods_id'] = goods_id
                                data['goods_url'] = 'https://item.taobao.com/item.htm?id=' + str(goods_id)
                                data['username'] = '18698570079'
                                data['main_goods_id'] = item[1]

                                # print('------>>>| 爬取到的数据为: ', data)
                                taobao.old_taobao_goods_insert_into_new_table(data, pipeline=tmp_sql_server_2)
                            else:
                                pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
                # 国外服务器上可以缩短时间, 可以设置为0s
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 不能太频繁，与用户请求错开尽量
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        gc.collect()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    run_forever()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        run_forever()