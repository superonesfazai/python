# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_real-times_update.py
@Time    : 2017/10/28 07:24
@connect : superonesfazai@gmail.com
'''

"""
我们需要两台服务器一台拿来专门更新数据，一台拿来专门处理客服入信息
"""

import sys
sys.path.append('..')

from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools,
)

from settings import TAOBAO_REAL_TIMES_SLEEP_TIME
import gc
from time import sleep
from logging import INFO, ERROR
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
)

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import (
    daemon_init,
    restart_program,
)
from fzutils.cp_utils import (
    _get_price_change_info,
    get_shelf_time_and_delete_time,
)

def run_forever():
    #### 实时更新数据
    while True:
        # ** 不能写成全局变量并放在循环中, 否则会一直记录到同一文件中
        my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )

        sql_str = '''
        select GoodsID, IsDelete, Price, TaoBaoPrice, shelf_time, delete_time 
        from dbo.GoodsInfoAutoGet 
        where SiteID=1 and MainGoodsID is not null
        order by ID desc'''

        # tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        tmp_sql_server = SqlPools()  # 使用sqlalchemy管理数据库连接池
        try:
            # result = list(tmp_sql_server.select_taobao_all_goods_id())
            result = tmp_sql_server._select_table(sql_str=sql_str,)
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
            for item in result:  # 实时更新数据
                taobao = TaoBaoLoginAndParse(logger=my_lg)
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    my_lg.info('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlPools()

                    my_lg.info('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (item[0], str(index)))
                    data = taobao.get_goods_data(item[0])

                    if data.get('is_delete') == 1:        # 单独处理【原先插入】就是 下架状态的商品
                        data['goods_id'] = item[0]
                        data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[1],
                            shelf_time=item[4],
                            delete_time=item[5]
                        )

                        # my_lg.info('------>>>| 爬取到的数据为: ' + str(data))
                        taobao.to_right_and_update_data(data, pipeline=tmp_sql_server)

                        sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 避免服务器更新太频繁
                        index += 1
                        gc.collect()
                        continue

                    data = taobao.deal_with_data(goods_id=item[0])
                    if data != {}:
                        data['goods_id'] = item[0]
                        data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[1],
                            shelf_time=item[4],
                            delete_time=item[5]
                        )
                        data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                            old_price=item[2],
                            old_taobao_price=item[3],
                            new_price=data['price'],
                            new_taobao_price=data['taobao_price']
                        )

                        # my_lg.info('------>>>| 爬取到的数据为: ' + str(data))
                        taobao.to_right_and_update_data(data, pipeline=tmp_sql_server)
                    else:
                        my_lg.info('------>>>| 休眠5s中...')
                        sleep(5)

                else:  # 表示返回的data值为空值
                    my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
                    sleep(10)
                    pass

                index += 1
                # try:
                #     del taobao
                # except:
                #     pass
                gc.collect()
                # 国外服务器上可以缩短时间, 可以设置为0s
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 不能太频繁，与用户请求错开尽量
            my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
        gc.collect()
        restart_program()

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