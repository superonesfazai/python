# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_miaosha_real-times_update.py
@Time    : 2017/11/16 15:57
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from zhe_800_parse import Zhe800Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
import os, re, pytz, datetime
import json
from pprint import pprint
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from random import randint
from settings import HEADERS, IS_BACKGROUND_RUNNING
import requests
from my_phantomjs import MyPhantomjs
from my_utils import get_shanghai_time, daemon_init, timestamp_to_regulartime

class Zhe_800_Miaosha_Real_Time_Update(object):
    def __init__(self):
        self._set_headers()
        self.my_phantomjs = MyPhantomjs()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'zhe800.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

    def run_forever(self):
        '''
        这个实时更新的想法是只更新当天前天未来两小时的上架商品的信息，再未来信息价格(全为原价)暂不更新
        :return:
        '''
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server.select_zhe_800_xianshimiaosha_all_goods_id())
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
                miaosha_begin_time = json.loads(item[1]).get('miaosha_begin_time')
                miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time,'%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_begin_time)

                data = {}
                # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                zhe_800_miaosha = Zhe800Parse()
                if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(miaosha_begin_time) == 0:
                        tmp_sql_server.delete_zhe_800_expired_goods_id(goods_id=item[0])
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))

                    elif self.is_recent_time(miaosha_begin_time) == 2:
                        # break       # 跳出循环
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:   # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        data['goods_id'] = item[0]
                        # print('------>>>| 爬取到的数据为: ', data)

                        tmp_url = 'https://zapi.zhe800.com/zhe800_n_api/xsq/m/session_deals?session_id={0}&page=1&per_page=1000'.format(
                            str(item[2])
                        )

                        body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)
                        body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(body)

                        if body_1 != []:
                            tmp_data = body_1[0]
                            tmp_data = json.loads(tmp_data)
                            # pprint(tmp_data)

                            if tmp_data.get('data', {}).get('blocks', []) == []:  # session_id不存在
                                print('该session_id不存在，此处跳过')
                                pass

                            else:
                                tmp_data = [item_s.get('deal', {}) for item_s in tmp_data.get('data', {}).get('blocks', [])]
                                if tmp_data != []:  # 否则说明里面有数据
                                    miaosha_goods_list = self.get_miaoshao_goods_info_list(data=tmp_data)
                                    # pprint(miaosha_goods_list)

                                    # 该session_id中现有的所有zid的list
                                    miaosha_goods_all_goods_id = [i.get('zid') for i in miaosha_goods_list]

                                    if item[0] not in miaosha_goods_all_goods_id:   # 内部已经下架的
                                        print('该商品已被下架限时秒杀活动，此处将其删除')
                                        tmp_sql_server.delete_zhe_800_expired_goods_id(goods_id=item[0])
                                        print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                        pass

                                    else:   # 未下架的
                                        for item_1 in miaosha_goods_list:
                                            if item_1.get('zid', '') == item[0]:
                                                zhe_800_miaosha.get_goods_data(goods_id=item[0])
                                                goods_data = zhe_800_miaosha.deal_with_data()

                                                if goods_data == {}:  # 返回的data为空则跳过
                                                    pass
                                                else:  # 否则就解析并且插入
                                                    goods_data['stock_info'] = item_1.get('stock_info')
                                                    goods_data['goods_id'] = str(item_1.get('zid'))
                                                    # goods_data['username'] = '18698570079'
                                                    if item_1.get('stock_info').get('activity_stock') > 0:
                                                        goods_data['price'] = item_1.get('price')
                                                        goods_data['taobao_price'] = item_1.get('taobao_price')
                                                    else:
                                                        pass
                                                    goods_data['sub_title'] = item_1.get('sub_title')
                                                    goods_data['miaosha_time'] = item_1.get('miaosha_time')
                                                    goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item_1.get('miaosha_time'))

                                                    # print(goods_data['stock_info'])
                                                    # print(goods_data['miaosha_time'])
                                                    zhe_800_miaosha.to_update_zhe_800_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                                            else:
                                                pass

                                else:  # 说明这个sessionid没有数据, 就删除对应这个sessionid的限时秒杀商品
                                    print('该sessionid没有相关key为jsons的数据')
                                    # return {}
                                    tmp_sql_server.delete_zhe_800_expired_goods_id(goods_id=item[0])
                                    print('过期的goods_id为(%s)' % item[0], ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))
                                    pass
                        else:
                            print('获取到的data为空!')
                            # return {}
                            pass

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                # try:
                #     del tmall
                # except:
                #     pass
                # sleep(.8)
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(5)
        # del ali_1688
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

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -259200:     # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        # if diff_time < -172800:     # (原先的时间)48个小时, 只需要跟新过去48小时和对与当前时间的未来2小时的商品信息
            return 0    # 已过期恢复原价的
        elif diff_time > -172800 and diff_time < 7200:
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:
            return 2    # 未来时间的暂时不用更新

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            # pprint(item)
            tmp = {}
            # 秒杀开始时间和结束时间
            tmp['miaosha_time'] = {
                'miaosha_begin_time': timestamp_to_regulartime(int(str(item.get('begin_time'))[0:10])),
                'miaosha_end_time': timestamp_to_regulartime(int(str(item.get('end_time'))[0:10])),
            }

            # 折800商品地址
            tmp['zid'] = item.get('zid')
            # 是否包邮
            # tmp['is_baoyou'] = item.get('is_baoyou', 0)
            # 限时秒杀的库存信息
            tmp['stock_info'] = {
                'activity_stock': item.get('activity_stock', 0),  # activity_stock为限时抢的剩余数量
                'stock': item.get('stock', 0),  # stock为限时秒杀的总库存
            }
            # 原始价格
            tmp['price'] = float(item.get('list_price'))
            # 秒杀的价格, float类型
            tmp['taobao_price'] = float(item.get('price'))
            # 子标题
            tmp['sub_title'] = item.get('description', '')
            miaosha_goods_list.append(tmp)
            # pprint(miaosha_goods_list)

        return miaosha_goods_list

    def __del__(self):
        try:
            del self.my_phantomjs
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Zhe_800_Miaosha_Real_Time_Update()
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
