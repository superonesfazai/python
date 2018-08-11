# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_miaosha_real-times_update.py
@Time    : 2018/2/1 09:29
@connect : superonesfazai@gmail.com
'''

'''
蘑菇街秒杀商品实时更新脚本
'''

import sys
sys.path.append('..')

from mogujie_miaosha_parse import MoGuJieMiaoShaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import os, re, pytz, datetime
import json
from pprint import pprint
import time
from random import randint
from settings import IS_BACKGROUND_RUNNING, MOGUJIE_SLEEP_TIME
import requests
from decimal import Decimal

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class MoGuJieMiaoShaRealTimeUpdate(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = r'delete from dbo.mogujie_xianshimiaosha where goods_id=%s'

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mogujie.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = r'select goods_id, miaosha_time, event_time, goods_url from dbo.mogujie_xianshimiaosha where site_id=22'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
        except TypeError:
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
                miaosha_end_time = json.loads(item[1]).get('miaosha_end_time')
                miaosha_end_time = int(str(time.mktime(time.strptime(miaosha_end_time,'%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                data = {}
                # 释放内存, 在外面声明就会占用很大的, 所以此处优化内存的方法是声明后再删除释放
                mogujie_miaosha = MoGuJieMiaoShaParse()
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(miaosha_end_time) == 0:
                        tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))

                    elif self.is_recent_time(miaosha_end_time) == 2:
                        # break       # 跳出循环
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:   # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        data['goods_id'] = item[0]

                        item_list = self.get_item_list(event_time=str(item[2]))
                        if item_list == '':
                            # 可能网络状况导致, 先跳过
                            pass

                        elif item_list == []:
                            print('该商品已被下架限时秒杀活动，此处将其删除')
                            tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                            print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                            pass

                        else:
                            # 该event_time中现有的所有goods_id的list
                            miaosha_goods_all_goods_id = [item_1.get('iid', '') for item_1 in item_list]

                            if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                                print('该商品已被下架限时秒杀活动，此处将其删除')
                                tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                pass

                            else:  # 未下架的
                                for item_2 in item_list:
                                    if item_2.get('iid', '') == item[0]:
                                        spider_url = item[3]
                                        mogujie_miaosha.get_goods_data(goods_id=spider_url)
                                        goods_data = mogujie_miaosha.deal_with_data()

                                        if goods_data == {}:    # 返回的data为空则跳过
                                            pass
                                        else:
                                            goods_data['goods_id'] = str(item[0])

                                            # price设置为原价
                                            try:
                                                tmp_price_list = sorted([round(float(item_4.get('normal_price', '')), 2) for item_4 in goods_data['price_info_list']])
                                                price = Decimal(tmp_price_list[-1]).__round__(2)  # 商品原价
                                                goods_data['price'] = price
                                            except:
                                                print('设置price为原价时出错!请检查')
                                                continue

                                            goods_data['miaosha_time'] = {
                                                'miaosha_begin_time': timestamp_to_regulartime(int(item_2.get('startTime', 0))),
                                                'miaosha_end_time': timestamp_to_regulartime(int(item_2.get('endTime', 0))),
                                            }
                                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])

                                            # pprint(goods_data)
                                            # print(goods_data)
                                            mogujie_miaosha.update_mogujie_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                                            sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度
                                    else:
                                        pass

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        gc.collect()

    def get_miaosha_begin_time_and_miaosha_end_time(self, miaosha_time):
        '''
        返回秒杀开始和结束时间
        :param miaosha_time:
        :return: tuple  miaosha_begin_time, miaosha_end_time
        '''
        miaosha_begin_time = miaosha_time.get('miaosha_begin_time')
        miaosha_end_time = miaosha_time.get('miaosha_end_time')
        # 将字符串转换为datetime类型
        miaosha_begin_time = datetime.datetime.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')
        miaosha_end_time = datetime.datetime.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')

        return miaosha_begin_time, miaosha_end_time

    def get_item_list(self, event_time):
        '''
        得到event_time中所有的商品信息
        :param event_time:
        :return: item_list 类型 list
        '''
        tmp_url = 'https://qiang.mogujie.com//jsonp/fastBuyListActionLet/1?eventTime={0}&bizKey=rush_main'.format(str(event_time))
        body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
        # print(body)

        if body == '':
            print('获取到的body为空值! 此处跳过')
            item_list = ''

        else:
            try:
                body = re.compile('null\((.*)\)').findall(body)[0]
            except Exception:
                print('re匹配body中的数据时出错!')
                body = '{}'

            try:
                tmp_data = json.loads(body)
            except:
                tmp_data = {}
                print('json.loads转换body时出错, 此处跳过!')

            if tmp_data == {}:
                print('tmp_data为空{}!')
                item_list = []

            else:
                # pprint(tmp_data)
                # print(tmp_data)

                item_list = tmp_data.get('data', {}).get('list', [])
        sleep(.5)

        return item_list

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -86400:     # (为了后台能同步下架)所以设置为 24个小时
        # if diff_time < 0:     # (原先的时间)结束时间 与当前时间差 <= 0
            return 0    # 已过期恢复原价的
        elif diff_time > 0:
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:           # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
            return 2

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = MoGuJieMiaoShaRealTimeUpdate()
        tmp.run_forever()
        try:
            del tmp
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()