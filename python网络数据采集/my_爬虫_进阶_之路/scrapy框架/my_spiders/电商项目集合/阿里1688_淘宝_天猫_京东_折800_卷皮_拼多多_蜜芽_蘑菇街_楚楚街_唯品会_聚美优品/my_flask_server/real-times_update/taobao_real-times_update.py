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
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline, SqlPools
from my_utils import get_shanghai_time, daemon_init

from settings import TAOBAO_REAL_TIMES_SLEEP_TIME
import gc
from time import sleep
import os, re, pytz, datetime
import json
from settings import IS_BACKGROUND_RUNNING

def run_forever():
    #### 实时更新数据
    while True:
        # tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        tmp_sql_server = SqlPools()  # 使用sqlalchemy管理数据库连接池
        try:
            # result = list(tmp_sql_server.select_taobao_all_goods_id())
            result = tmp_sql_server.select_taobao_all_goods_id()

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
                taobao = TaoBaoLoginAndParse()
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    # try:
                    #     del tmp_sql_server
                    # except:
                    #     pass
                    # gc.collect()
                    # tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    tmp_sql_server = SqlPools()

                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                    data = taobao.get_goods_data(item[0])

                    if data.get('is_delete') == 1:        # 单独处理【原先插入】就是 下架状态的商品
                        data['goods_id'] = item[0]
                        data['my_shelf_and_down_time'], data['delete_time'] = get_my_shelf_and_down_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[1],
                            MyShelfAndDownTime=item[2]
                        )

                        # print('------>>>| 爬取到的数据为: ', data)
                        taobao.to_right_and_update_data(data, pipeline=tmp_sql_server)

                        sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 避免服务器更新太频繁
                        index += 1
                        gc.collect()
                        continue

                    data = taobao.deal_with_data(goods_id=item[0])
                    if data != {}:
                        data['goods_id'] = item[0]
                        data['my_shelf_and_down_time'], data['delete_time'] = get_my_shelf_and_down_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[1],
                            MyShelfAndDownTime=item[2]
                        )

                        # print('------>>>| 爬取到的数据为: ', data)
                        taobao.to_right_and_update_data(data, pipeline=tmp_sql_server)
                    else:
                        pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                # try:
                #     del taobao
                # except:
                #     pass
                gc.collect()
                # 国外服务器上可以缩短时间, 可以设置为0s
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 不能太频繁，与用户请求错开尽量
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
        gc.collect()

def set_delete_time_from_orginal_time(my_shelf_and_down_time):
    '''
    返回原先商品状态变换被记录下的时间点
    :param my_shelf_and_down_time: 一个dict
    :return: detele_time    datetime类型
    '''
    shelf_time = my_shelf_and_down_time.get('shelf_time', '')
    if shelf_time != '':
        # 将字符串类型的时间转换为datetime类型
        shelf_time = datetime.datetime.strptime(shelf_time, '%Y-%m-%d %H:%M:%S')
    down_time = my_shelf_and_down_time.get('down_time', '')
    if down_time != '':
        down_time = datetime.datetime.strptime(down_time, '%Y-%m-%d %H:%M:%S')

    if shelf_time == '':
        delete_time = down_time
    elif down_time == '':
        delete_time = shelf_time
    else:  # shelf_time和down_time都不为''
        if shelf_time > down_time:  # 取最近的那个
            delete_time = shelf_time
        else:
            delete_time = down_time

    return delete_time

def get_my_shelf_and_down_time_and_delete_time(tmp_data, is_delete, MyShelfAndDownTime):
    '''
    得到my_shelf_and_down_time和delete_time
    :param tmp_data:
    :param is_delete:
    :param MyShelfAndDownTime:
    :return:
    '''
    '''
    设置最后刷新的商品状态上下架时间
    '''
    # 1.is_delete由0->1 为下架时间down_time  2. is_delete由1->0 为上架时间shelf_time
    my_shelf_and_down_time = {
        'shelf_time': '',
        'down_time': '',
    }
    if tmp_data['is_delete'] != is_delete:  # 表示状态改变
        if tmp_data['is_delete'] == 0 and is_delete == 1:
            # is_delete由0->1 表示商品状态上架变为下架
            my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
        else:
            # is_delete由1->0 表示商品状态下架变为上架
            my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
        delete_time = str(get_shanghai_time())  # 记录下状态变化的时间点
    else:  # 表示状态不变
        if MyShelfAndDownTime is None or MyShelfAndDownTime == '{"shelf_time": "", "down_time": ""}' or len(MyShelfAndDownTime) == 35:  # 35就是那串初始str
            if tmp_data['is_delete'] == 0:  # 上架的状态
                my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
            else:  # 下架的状态
                my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
            delete_time = str(get_shanghai_time())
        else:
            # 否则保存原始值不变
            tmp_shelf_and_down_time = MyShelfAndDownTime
            my_shelf_and_down_time = json.loads(tmp_shelf_and_down_time)  # 先转换为dict
            # print(my_shelf_and_down_time)
            delete_time = set_delete_time_from_orginal_time(my_shelf_and_down_time=my_shelf_and_down_time)

    return (my_shelf_and_down_time, delete_time)

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