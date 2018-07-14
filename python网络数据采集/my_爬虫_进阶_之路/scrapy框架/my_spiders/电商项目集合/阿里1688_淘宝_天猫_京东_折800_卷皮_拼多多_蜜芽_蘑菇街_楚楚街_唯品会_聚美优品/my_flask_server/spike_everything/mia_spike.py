# coding:utf-8

'''
@author = super_fazai
@File    : mia_spike.py
@Time    : 2018/1/16 11:03
@connect : superonesfazai@gmail.com
'''

'''
蜜芽秒杀抓取(秒杀时间为每日的10点，15点)
'''

from random import randint
import json
import re
import time
from pprint import pprint
import gc
import pytz
from time import sleep
import os

import sys
sys.path.append('..')

from settings import MIA_BASE_NUMBER, MIA_MAX_NUMBER, MIA_SPIKE_SLEEP_TIME
from mia_parse import MiaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import IS_BACKGROUND_RUNNING
import datetime

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class MiaSpike(object):
    def __init__(self):
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mia.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        mia_base_number = MIA_BASE_NUMBER
        while mia_base_number < MIA_MAX_NUMBER:
            tmp_url = 'https://m.mia.com/instant/seckill/seckillPromotionItem/' + str(mia_base_number)

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
            # print(body)

            if body == '' or body == '[]':
                print('mia_base_number为: ', mia_base_number)
                print('获取到的body为空值! 此处跳过')

            else:
                try:
                    tmp_data = json.loads(body)
                except:
                    tmp_data = {}
                    print('json.loads转换body时出错, 此处跳过!')
                tmp_hour = tmp_data.get('p_info', {}).get('start_time', '')[11:13]
                if tmp_hour == '22':    # 过滤掉秒杀时间为22点的
                    print('--- 销售时间为22点，不抓取!')
                    pass
                else:
                    print(tmp_data)
                    print('mia_base_number为: ', mia_base_number)
                    pid = mia_base_number
                    begin_time = tmp_data.get('p_info', {}).get('start_time', '')
                    end_time = tmp_data.get('p_info', {}).get('end_time', '')
                    item_list = tmp_data.get('item_list', [])

                    self.deal_with_data(pid, begin_time, end_time, item_list)

            sleep(.35)
            mia_base_number += 1

    def deal_with_data(self, *param):
        '''
        处理并存储相关秒杀商品的数据
        :param param: 相关参数
        :return:
        '''
        pid = param[0]
        begin_time = int(time.mktime(time.strptime(param[1], '%Y/%m/%d %H:%M:%S')))     # 把str字符串类型转换为时间戳的形式
        end_time = int(time.mktime(time.strptime(param[2], '%Y/%m/%d %H:%M:%S')))
        item_list = param[3]

        mia = MiaParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            sql_str = r'select goods_id, miaosha_time, pid from dbo.mia_xianshimiaosha where site_id=20'
            db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]
            # print(db_goods_id_list)

            for item in item_list:
                if item.get('item_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = str(item.get('item_id', ''))
                    tmp_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'

                    mia.get_goods_data(goods_id=str(goods_id))
                    goods_data = mia.deal_with_data()

                    if goods_data == {}:  # 返回的data为空则跳过
                        pass

                    else:  # 否则就解析并且插入
                        goods_url = goods_data['goods_url']
                        if re.compile(r'://m.miyabaobei.hk/').findall(goods_url) != '':
                            goods_url = 'https://www.miyabaobei.hk/item-' + str(goods_id) + '.html'
                        else:
                            goods_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'
                        goods_data['goods_url'] = goods_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['price'] = item.get('active_price')
                        goods_data['taobao_price'] = item.get('active_price')       # 秒杀最低价
                        goods_data['sub_title'] = item.get('short_info', '')
                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': timestamp_to_regulartime(begin_time),
                            'miaosha_end_time': timestamp_to_regulartime(end_time),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                        goods_data['pid'] = str(pid)

                        # pprint(goods_data)
                        # print(goods_data)
                        mia.insert_into_mia_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mia
        except:
            pass
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

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        mia_spike = MiaSpike()
        mia_spike.get_spike_hour_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))

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