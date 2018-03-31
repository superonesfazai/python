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
from my_utils import get_shanghai_time, daemon_init

import gc
from time import sleep
import datetime
import json
from settings import IS_BACKGROUND_RUNNING

def run_forever():
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
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            tmall = TmallParse()
            for item in result:  # 实时更新数据
                data = {}
                if index % 5 == 0:
                    tmall = TmallParse()
                    gc.collect()

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
                    data = tmall.get_goods_data(goods_id=tmp_item)
                    if isinstance(data, int):       # 单独处理return 4041
                        continue

                    if data.get('is_delete') == 1:  # 单独处理下架商品
                        data['goods_id'] = item[1]

                        data['my_shelf_and_down_time'], data['delete_time'] = get_my_shelf_and_down_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[2],
                            MyShelfAndDownTime=item[3]
                        )

                        # print('------>>>| 爬取到的数据为: ', data)
                        tmall.to_right_and_update_data(data, pipeline=tmp_sql_server)

                        sleep(1.5)
                        index += 1
                        gc.collect()
                        continue

                    data = tmall.deal_with_data()
                    if data != {}:
                        data['goods_id'] = item[1]

                        data['my_shelf_and_down_time'], data['delete_time'] = get_my_shelf_and_down_time_and_delete_time(
                            tmp_data=data,
                            is_delete=item[2],
                            MyShelfAndDownTime=item[3]
                        )

                        # print('------>>>| 爬取到的数据为: ', data)
                        tmall.to_right_and_update_data(data, pipeline=tmp_sql_server)
                    else:  # 表示返回的data值为空值
                        pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                # try:
                #     del tmall
                # except:
                #     pass
                gc.collect()
                sleep(2)
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
        # del ali_1688
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
    if tmp_data['is_delete'] != is_delete:
        if tmp_data['is_delete'] == 0 and is_delete == 1:
            # is_delete由0->1 表示商品状态上架变为下架
            my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
        else:
            # is_delete由1->0 表示商品状态下架变为上架
            my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
        delete_time = str(get_shanghai_time())  # 记录下状态变化的时间点
    else:
        if MyShelfAndDownTime is None or MyShelfAndDownTime == '{"shelf_time": "", "down_time": ""}' or len(MyShelfAndDownTime) == 35:  # 35就是那串初始str
            if tmp_data['is_delete'] == 0:  # 上架的状态
                my_shelf_and_down_time['shelf_time'] = str(get_shanghai_time())
            else:  # 下架的状态
                my_shelf_and_down_time['down_time'] = str(get_shanghai_time())
            delete_time = str(get_shanghai_time())  # 记录下状态变化的时间点
        else:
            # 否则保存原始值不变
            tmp_shelf_and_down_time = MyShelfAndDownTime
            my_shelf_and_down_time = json.loads(tmp_shelf_and_down_time)  # 先转换为dict
            delete_time = set_delete_time_from_orginal_time(my_shelf_and_down_time=my_shelf_and_down_time)

    # print(my_shelf_and_down_time)
    # print(delete_time)

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