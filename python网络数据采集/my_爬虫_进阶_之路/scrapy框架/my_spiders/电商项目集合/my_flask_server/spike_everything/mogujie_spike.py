# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_spike.py
@Time    : 2018/1/30 18:34
@connect : superonesfazai@gmail.com
'''

'''
蘑菇街秒杀抓取(新版无秒杀板块, 不再进行维护!)
'''

import json
import re
import time
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from mogujie_miaosha_parse import MoGuJieMiaoShaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import (
    IS_BACKGROUND_RUNNING, 
    MOGUJIE_SLEEP_TIME,
    IP_POOL_TYPE,)
import datetime
from decimal import Decimal

from sql_str_controller import mg_select_str_4

from fzutils.spider.async_always import *

class MoGuJieSpike(object):
    def __init__(self):
        self._set_headers()
        self.ip_pool_type = IP_POOL_TYPE
        self.db_goods_id_list = None

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

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        _ = self.get_today_hour_timestamp()
        for item in _:
            self.traversal_hour_timestamp(item=item)

        # 明日的商品列表
        tomorrow_hour_timestamp = [item + 1*86400 for item in _]
        for item in tomorrow_hour_timestamp:
            self.traversal_hour_timestamp(item=item)

        # 后天的商品列表
        tomorrow_hour_timestamp = [item + 2*86400 for item in _]
        for item in tomorrow_hour_timestamp:
            self.traversal_hour_timestamp(item=item)

    def deal_with_data(self, *param):
        '''
        处理并存储相关秒杀商品的数据
        :param param: 相关参数
        :return:
        '''
        print(60 * '*')
        event_time = param[0]
        item_list = param[1]
        print('秒杀开始时间:', timestamp_to_regulartime(event_time), '\t', '对应时间戳为: ', event_time)
        print(60 * '*')

        mogujie = MoGuJieMiaoShaParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        if my_pipeline.is_connect_success:
            _ = list(my_pipeline._select_table(sql_str=mg_select_str_4))
            db_goods_id_list = [item[0] for item in _]
            for item in item_list:
                goods_id = str(item.get('iid', ''))
                if goods_id in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass
                else:
                    tmp_url = item.get('link', '')
                    # print(tmp_url)
                    try:
                        object_id = re.compile('objectId=(\w+)').findall(tmp_url)[0]
                    except IndexError:      # 表示匹配到的地址不是秒杀商品的地址
                        print('+++++++ 这个url不是秒杀的url: ', tmp_url)
                        continue
                    tmp_url = 'https://shop.mogujie.com/rushdetail/{0}?objectId={1}&type=rush'.format(goods_id, object_id)
                    tmp_ = mogujie.get_goods_id_from_url(tmp_url)
                    mogujie.get_goods_data(goods_id=tmp_)
                    goods_data = mogujie.deal_with_data()
                    if goods_data == {}:  # 返回的data为空则跳过
                        pass
                    else:   # 否则就解析并且插入
                        goods_data['goods_url'] = tmp_url
                        goods_data['goods_id'] = str(goods_id)

                        # price设置为原价
                        try:
                            tmp_price_list = sorted([round(float(item_4.get('normal_price', '')), 2) for item_4 in goods_data['price_info_list']])
                            price = Decimal(tmp_price_list[-1]).__round__(2)  # 商品原价
                            goods_data['price'] = price
                        except:
                            print('设置price为原价时出错!请检查')
                            sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度
                            continue

                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': timestamp_to_regulartime(int(item.get('startTime', 0))),
                            'miaosha_end_time': timestamp_to_regulartime(int(item.get('endTime', 0))),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                        goods_data['event_time'] = str(event_time)
                        # pprint(goods_data)
                        # print(goods_data)
                        res = mogujie.insert_into_mogujie_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        if res:
                            if goods_id not in db_goods_id_list:
                                db_goods_id_list.append(goods_id)

                    sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mogujie
        except:
            pass
        gc.collect()

    def traversal_hour_timestamp(self, item):
        '''
        遍历每个需求的整点时间戳
        :param item:
        :return:
        '''
        # 先遍历today的需求的整点时间戳
        tmp_url = 'https://qiang.mogujie.com//jsonp/fastBuyListActionLet/1?eventTime={0}&bizKey=rush_main'.format(str(item))
        body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
        # print(body)
        if body == '':
            print('item为: ', item)
            print('获取到的body为空值! 此处跳过')

        else:
            try:
                body = re.compile('null\((.*)\)').findall(body)[0]
            except Exception:
                print('re匹配body中的数据时出错!')
                body = '{}'

            try:
                tmp_data = json.loads(body)
            except:
                print('json.loads转换body时出错, 此处跳过!')
                tmp_data = {}

            if tmp_data == {}:
                print('tmp_data为空{}!')
                pass
            else:
                # pprint(tmp_data)
                # print(tmp_data)

                event_time = item
                item_list = tmp_data.get('data', {}).get('list', [])

                self.deal_with_data(event_time, item_list)
                print('休眠15s...')
                sleep(15)

    def get_today_hour_timestamp(self):
        '''
        得到today的整点时间戳(需求的整点为: 9-16点)
        :return:today_hour_timestamp_list 类型 list
        '''
        today_hour_timestamp_list = []
        for hour in range(9, 17):  # 循环需求的整点时间
            a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % hour  # strftime格式化,%2d以2位的固定位宽获取int型的数值，由此获得整点字符串
            time_array = time.strptime(a, "%Y-%m-%d %H:%M:%S")  # 把一个时间字符串解析为时间元组，返回struct_time对象。
            timestamp = int(time.mktime(time_array))            # 接收struct_time对象，返回时间的浮点数
            today_hour_timestamp_list.append(timestamp)

        return today_hour_timestamp_list

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        mogujie_spike = MoGuJieSpike()
        mogujie_spike.get_spike_hour_goods_info()
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