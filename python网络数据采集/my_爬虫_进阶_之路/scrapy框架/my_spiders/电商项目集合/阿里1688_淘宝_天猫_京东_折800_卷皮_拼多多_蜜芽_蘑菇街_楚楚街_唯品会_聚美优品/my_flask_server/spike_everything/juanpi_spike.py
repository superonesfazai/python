# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_spike.py
@Time    : 2017/11/20 16:57
@connect : superonesfazai@gmail.com
'''

from random import randint
import json
import re
import time
from pprint import pprint
import gc
import pytz
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from time import sleep
import os

import sys
sys.path.append('..')

from juanpi_parse import JuanPiParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import IS_BACKGROUND_RUNNING

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class JuanPiSpike(object):
    def __init__(self):
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.juanpi.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        tab_id_list = [11, 12, 13, 21, 22, 23, 31, 32, 33]      # notice

        for tab_id in tab_id_list:
            for index in range(0, 50):
                tmp_url = 'https://m.juanpi.com/act/timebuy-xrgoodslist?tab_id={0}&page={1}'.format(
                    str(tab_id), str(index)
                )
                print('待抓取的限时秒杀地址为: ', tmp_url)

                data = MyRequests.get_url_body(url=tmp_url, headers=self.headers)
                if data == '': break

                try:
                    data = json.loads(data)
                    data = data.get('data', {})
                    # print(data)
                except:
                    break

                if data.get('goodslist') == []:
                    print('tab_id={0}, page={1}的goodslist为[], 此处跳过'.format(tab_id, index))
                    break
                else:
                    data = data.get('goodslist', [])
                    # print(data)
                    if data == []:
                        print('goodslist为[], 此处跳过')
                        pass
                    else:
                        miaosha_goods_list = self.get_miaoshao_goods_info_list(data=data)
                        print(miaosha_goods_list)

                        juanpi = JuanPiParse()
                        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                        if my_pipeline.is_connect_success:
                            sql_str = 'select goods_id, miaosha_time, tab_id, page from dbo.juanpi_xianshimiaosha where site_id=15'
                            if my_pipeline._select_table(sql_str=sql_str) is None:
                                db_goods_id_list = []
                            else:
                                db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]

                            for item in miaosha_goods_list:
                                if item.get('goods_id', '') in db_goods_id_list:
                                    print('该goods_id已经存在于数据库中, 此处跳过')
                                    pass
                                else:
                                    tmp_url = 'http://shop.juanpi.com/deal/' + item.get('goods_id')
                                    juanpi.get_goods_data(goods_id=item.get('goods_id'))
                                    goods_data = juanpi.deal_with_data()

                                    if goods_data == {}:    # 返回的data为空则跳过
                                        pass
                                    else:       # 否则就解析并插入
                                        goods_data['stock_info'] = item.get('stock_info')
                                        goods_data['goods_id'] = item.get('goods_id')
                                        goods_data['spider_url'] = tmp_url
                                        goods_data['username'] = '18698570079'
                                        goods_data['price'] = item.get('price')                 # 秒杀前的原特价
                                        goods_data['taobao_price'] = item.get('taobao_price')   # 秒杀价
                                        goods_data['sub_title'] = item.get('sub_title', '')
                                        goods_data['miaosha_time'] = item.get('miaosha_time')
                                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item.get('miaosha_time'))
                                        goods_data['tab_id'] = tab_id
                                        goods_data['page'] = index

                                        # print(goods_data)
                                        juanpi.insert_into_juanpi_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                                        sleep(.4)   # 短暂sleep下避免出错跳出
                            sleep(.65)
                        else:
                            pass
                        try:
                            del juanpi
                        except:
                            pass
                        gc.collect()

                        # else:           # 下面这3句用于跳出2层for循环
            #     continue    # continue表示执行成功就继续
            # break           # break表示执行失败就跳出

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            tmp = {}
            tmp['miaosha_time'] = {
                'miaosha_begin_time': timestamp_to_regulartime(int(item.get('start_time'))),
                'miaosha_end_time': timestamp_to_regulartime(int(item.get('end_time'))),
            }
            stock = item.get('stock', 0)
            # 卷皮商品的goods_id
            tmp['goods_id'] = item.get('goods_id')
            # 限时秒杀库存信息
            tmp['stock_info'] = {
                'activity_stock': int(item.get('stock', 0)*(item.get('rate', 0)/100)),
                'stock': item.get('stock', 0),
            }
            # 原始价格
            tmp['price'] = round(float(item.get('oprice', '0')), 2)
            tmp['taobao_price'] = round(float(item.get('cprice', '0')), 2)
            miaosha_goods_list.append(tmp)

        return miaosha_goods_list

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        juanpi_spike = JuanPiSpike()
        juanpi_spike.get_spike_hour_goods_info()
        try:
            del juanpi_spike
        except:
            pass
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
