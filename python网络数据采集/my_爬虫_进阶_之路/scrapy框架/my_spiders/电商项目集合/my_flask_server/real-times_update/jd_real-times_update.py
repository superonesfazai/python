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
from settings import IS_BACKGROUND_RUNNING

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import (
    _get_price_change_info,
    get_shelf_time_and_delete_time,
)

def run_forever():
    while True:
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        # and GETDATE()-ModfiyTime>1 and IsDelete=0
        sql_str = '''
        select SiteID, GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time
        from dbo.GoodsInfoAutoGet 
        where (SiteID=7 or SiteID=8 or SiteID=9 or SiteID=10) and MainGoodsID is not null
        '''

        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
        except TypeError as e:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            continue

        print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
        print(result)
        print('--------------------------------------------------------')
        print('总计待更新个数:', len(result))

        print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
        index = 1

        # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
        jd = JdParse()

        for item in result:  # 实时更新数据
            # # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            # jd = JdParse()
            if index % 10 == 0:
                try: del jd
                except: pass
                gc.collect()
                jd = JdParse()

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
                    print('上架时间:', data['shelf_time'], '下架时间:', data['delete_time'])

                    data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                        old_price=item[3],
                        old_taobao_price=item[4],
                        new_price=data['price'],
                        new_taobao_price=data['taobao_price'])

                    # print('------>>>| 爬取到的数据为: ', data)
                    jd.to_right_and_update_data(data, pipeline=tmp_sql_server)
                else:  # 表示返回的data值为空值
                    pass
            else:  # 表示返回的data值为空值
                print('数据库连接失败，数据库可能关闭或者维护中')
                pass
            index += 1
            # try:
            #     del jd
            # except:
            #     pass
            gc.collect()
            sleep(1.2)
        print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        try: del jd
        except: pass
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
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