# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_migrate.py
@Time    : 2018/3/13 19:21
@connect : superonesfazai@gmail.com
'''

"""
将老表中的goods更新到新表中进行上下架监控
"""

import sys
sys.path.append('..')

from ali_1688_parse import ALi1688LoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
from settings import IS_BACKGROUND_RUNNING

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init

def run_forever():
    while True:
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = 'select GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where SiteID=2 order by ID desc'
        sql_str_2 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
            result_2 = list(tmp_sql_server._select_table(sql_str=sql_str_2))
            # print(result_2)
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result_2)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            ali_1688 = ALi1688LoginAndParse()
            # 新表 GoodsInfoAutoGet
            new_table_ali_1688_all_goods_id_list = list(set([item[0] for item in result]))      # 新表里面的goods_id
            print(new_table_ali_1688_all_goods_id_list)
            sleep(2)

            # 老表
            old_table_ali_1688_all_goods_list = []
            for item in result_2:
                tmp_goods_id = ali_1688.get_goods_id_from_url(item[0])
                if tmp_goods_id != '' and tmp_goods_id not in new_table_ali_1688_all_goods_id_list:
                    old_table_ali_1688_all_goods_list.append([
                        'https://detail.1688.com/offer/' + tmp_goods_id + '.html',
                        item[1],
                        tmp_goods_id,
                    ])
                else:
                    print('@@@ 原地址为: ', item[0])
            # print(old_table_ali_1688_all_goods_list)
            print('老表待转数据个数为: ', len(old_table_ali_1688_all_goods_list))
            sleep(2)

            for item in old_table_ali_1688_all_goods_list:  # 实时更新数据
                if index % 10 == 0:
                    ali_1688 = ALi1688LoginAndParse()

                if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    # try:
                    #     del tmp_sql_server
                    # except:
                    #     pass
                    # gc.collect()
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    goods_id = str(item[2])
                    # print(goods_id)
                    if goods_id in new_table_ali_1688_all_goods_id_list:
                        print('该goods_id已经存在于数据库中, 此处跳过!')
                        index += 1
                        gc.collect()
                        continue        # 跳过sleep

                    else:
                        sql_str = 'select GoodsID from dbo.GoodsInfoAutoGet where SiteID=2 and GoodsID=%s'
                        try:    # 老是有重复的，索性单独检查
                            is_in_db = list(tmp_sql_server._select_table(sql_str=sql_str, params=(goods_id)))
                        except:
                            is_in_db = []
                            pass
                        if is_in_db != []:
                            print('该goods_id已经存在于数据库中, 此处跳过!')
                            index += 1
                            gc.collect()
                            continue

                        print('------>>>| 正在插入的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                        tt = ali_1688.get_ali_1688_data(goods_id)
                        if tt.get('is_delete') == 1 and tt.get('before') is False:    # 处理已下架的但是还是要插入的
                            tt['goods_id'] = goods_id
                            tt['goods_url'] = 'https://detail.1688.com/offer/' + goods_id + '.html'
                            tt['username'] = '18698570079'
                            tt['main_goods_id'] = item[1]

                            ali_1688.old_ali_1688_goods_insert_into_new_table(data=tt, pipeline=tmp_sql_server)

                            index += 1
                            gc.collect()
                            sleep(1.2)
                            continue
                        else:
                            pass

                        data = ali_1688.deal_with_data()
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://detail.1688.com/offer/' + goods_id + '.html'
                            data['username'] = '18698570079'
                            data['main_goods_id'] = item[1]

                            ali_1688.old_ali_1688_goods_insert_into_new_table(data=data, pipeline=tmp_sql_server)

                        else:   # 表示返回的data为空值
                            pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                # try:
                #     del ali_1688
                # except:
                #     pass
                gc.collect()
                sleep(2)
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        # del ali_1688
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