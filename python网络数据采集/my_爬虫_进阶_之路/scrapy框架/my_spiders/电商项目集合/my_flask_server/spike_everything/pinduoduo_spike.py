# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_spike.py
@Time    : 2017/11/25 15:22
@connect : superonesfazai@gmail.com
'''

"""
拼多多退货严重, 不采集
"""

import json
import re
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from pinduoduo_parse import PinduoduoParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import (
    IS_BACKGROUND_RUNNING,
    PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST,
    PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST,
    IP_POOL_TYPE,)

from settings import PHANTOMJS_DRIVER_PATH, PINDUODUO_SLEEP_TIME

from sql_str_controller import pd_select_str_3

from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

class PinduoduoSpike(object):
    def __init__(self):
        self._set_headers()
        self.ip_pool_type = IP_POOL_TYPE
        self.driver = BaseDriver(
            executable_path=PHANTOMJS_DRIVER_PATH,
            ip_pool_type=self.ip_pool_type,
        )

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

    def _get_db_goods_id_list(self) -> list:
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        _ = my_pipeline._select_table(sql_str=pd_select_str_3)
        assert _ is not None, 'db_goods_id_list为None!'
        db_goods_id_list = [item[0] for item in list(_)]

        try:
            del my_pipeline
        except:
            pass

        return db_goods_id_list

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        all_miaosha_goods_list = self.get_all_miaosha_goods_list()
        try:
            del self.driver
        except:
            pass
        gc.collect()

        pinduoduo = PinduoduoParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            self.db_goods_id_list = self._get_db_goods_id_list()
            for item in all_miaosha_goods_list:
                '''
                注意: 明日8点半抓取到的是页面加载中返回的是空值
                '''
                if item.get('goods_id') != 'None':    # 跳过goods_id为'None'
                    if item.get('goods_id', '') in self.db_goods_id_list:
                        print('该goods_id已经存在于数据库中, 此处跳过')
                        pass
                    else:
                        tmp_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + item.get('goods_id')
                        pinduoduo.get_goods_data(goods_id=item.get('goods_id'))
                        goods_data = pinduoduo.deal_with_data()

                        # print(goods_data)
                        if goods_data == {}:  # 返回的data为空则跳过
                            print('得到的goods_data为空值，此处先跳过，下次遍历再进行处理')
                            # sleep(3)
                            pass

                        else:  # 否则就解析并插入
                            goods_data['stock_info'] = item.get('stock_info')
                            goods_data['goods_id'] = item.get('goods_id')
                            goods_data['spider_url'] = tmp_url
                            goods_data['username'] = '18698570079'
                            goods_data['price'] = item.get('price')  # 秒杀前的原特价
                            goods_data['taobao_price'] = item.get('taobao_price')  # 秒杀价
                            goods_data['sub_title'] = item.get('sub_title', '')
                            goods_data['miaosha_time'] = item.get('miaosha_time')
                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item.get('miaosha_time'))

                            if item.get('stock_info', {}).get('activity_stock', 0) <= 2:
                                # 实时秒杀库存小于等于2时就标记为 已售罄
                                print('该秒杀商品已售罄...')
                                goods_data['is_delete'] = 1

                            pinduoduo.insert_into_pinduoduo_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        sleep(PINDUODUO_SLEEP_TIME)

                else:
                    print('该goods_id为"None", 此处跳过')
                    pass
            sleep(5)

        else:
            pass
        try:
            del pinduoduo
        except:
            pass
        gc.collect()

    def get_all_miaosha_goods_list(self):
        def get_data(body):
            '''处理返回的body'''
            _ = '{}'
            try:
                _ = re.compile(r'<body>(.*)</body>').findall(body)[0]
            except IndexError:
                print('获取all_miaosha_goods_list出现索引异常!')

            return _

        # 今日秒杀
        tmp_url = 'http://apiv4.yangkeduo.com/api/spike/v2/list/today?page=0&size=2000'
        print('待爬取的今日限时秒杀数据的地址为: ', tmp_url)
        today_data = get_data(body=self.driver.get_url_body(url=tmp_url))
        today_data = self.json_to_dict(tmp_data=today_data)
        sleep(PINDUODUO_SLEEP_TIME)

        # 明日的秒杀
        tmp_url_2 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/tomorrow?page=0&size=2000'
        print('待爬取的明日限时秒杀数据的地址为: ', tmp_url_2)
        tomorrow_data = get_data(body=self.driver.get_url_body(url=tmp_url_2))
        tomorrow_data = self.json_to_dict(tmp_data=tomorrow_data)
        sleep(PINDUODUO_SLEEP_TIME)

        # 未来的秒杀
        tmp_url_3 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/all_after?page=0&size=2000'
        print('待爬取的未来限时秒杀数据的地址为: ', tmp_url_3)
        all_after_data = get_data(body=self.driver.get_url_body(url=tmp_url_3))
        all_after_data = self.json_to_dict(tmp_data=all_after_data)
        sleep(PINDUODUO_SLEEP_TIME)

        if today_data != []:
            today_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=today_data)
            # print('今日限时秒杀的商品list为: ', today_miaosha_goods_list)

        else:
            today_miaosha_goods_list = []
            print('今日秒杀的items为[]')

        if tomorrow_data != []:
            tomorrow_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=tomorrow_data)
            # print('明日限时秒杀的商品list为: ', tomorrow_miaosha_goods_list)

        else:
            tomorrow_miaosha_goods_list = []
            print('明日秒杀的items为[]')

        if all_after_data != []:
            all_after_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=all_after_data)
            # print('未来限时秒杀的商品list为: ', all_after_miaosha_goods_list)

        else:
            all_after_miaosha_goods_list = []
            print('未来秒杀的items为[]')

        all_miaosha_goods_list = today_miaosha_goods_list
        for item in tomorrow_miaosha_goods_list:
            all_miaosha_goods_list.append(item)
        for item in all_after_miaosha_goods_list:
            all_miaosha_goods_list.append(item)
        print('当前所有限时秒杀商品list为: ', all_miaosha_goods_list)

        return all_miaosha_goods_list

    def json_to_dict(self, tmp_data):
        try:
            data = json.loads(tmp_data)
            # pprint(data)
            times = [str(timestamp_to_regulartime(int(item))) for item in data.get('times', [])]
            data = data.get('items', [])
            # print(data)
            # print(times)
        except:
            print('json.loads转换data的时候出错，data为空')
            data = []
        return data

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            tmp = {}
            miaosha_begin_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time'))))
            tmp_hour = miaosha_begin_time[-8:-6]
            if tmp_hour in PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST:
                if tmp_hour in PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST:
                    '''
                    # 这些起始的点秒杀时间只有30分钟
                    '''
                    miaosha_end_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*30))
                else:
                    miaosha_end_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*60))

                tmp['miaosha_time'] = {
                    'miaosha_begin_time': miaosha_begin_time,
                    'miaosha_end_time': miaosha_end_time,
                }
                # 卷皮商品的goods_id
                tmp['goods_id'] = str(item.get('data', {}).get('goods_id'))
                # 限时秒杀库存信息
                tmp['stock_info'] = {
                    'activity_stock': int(item.get('data', {}).get('all_quantity', 0) - item.get('data', {}).get('sold_quantity', 0)),
                    'stock': item.get('data', {}).get('all_quantity', 0),
                }
                # 原始价格
                tmp['price'] = round(float(item.get('data', {}).get('normal_price', '0'))/100, 2)
                tmp['taobao_price'] = round(float(item.get('data', {}).get('price', '0'))/100, 2)
                miaosha_goods_list.append(tmp)
            else:
                pass
        return miaosha_goods_list

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        pinduoduo_spike = PinduoduoSpike()
        pinduoduo_spike.get_spike_hour_goods_info()
        try:
            del pinduoduo_spike
        except:
            pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*4)

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