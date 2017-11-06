# coding:utf-8

'''
@author = super_fazai
@File    : tmall_real-time_update.py
@Time    : 2017/11/6 16:45
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse import TmallParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep

if __name__ == '__main__':
    while True:
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server.select_tmall_all_goods_id_url())
        except TypeError as e:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            for item in result:  # 实时更新数据
                data = {}
                # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                tmall = TmallParse()
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
                    print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[1], index))
                    tmp_item = []
                    if item[0] == 3:        # 从数据库中取出时，先转换为对应的类型
                        tmp_item.append(0)
                    elif item[0] == 4:
                        tmp_item.append(1)
                    elif item[0] == 6:
                        tmp_item.append(2)
                    tmp_item.append(item[1])
                    tmall.get_goods_data(goods_id=tmp_item)
                    data = tmall.deal_with_data()
                    if data != {}:
                        data['goods_id'] = item[1]
                        # print('------>>>| 爬取到的数据为: ', data)
                        tmall.to_right_and_update_data(data, pipeline=tmp_sql_server)
                    else:  # 表示返回的data值为空值
                        pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                try:
                    del tmall
                except:
                    pass
                gc.collect()
                # sleep(1)
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        sleep(5)
        # del ali_1688
        gc.collect()



