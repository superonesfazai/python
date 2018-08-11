# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_pintuan.py
@Time    : 2017/12/23 14:30
@connect : superonesfazai@gmail.com
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

from settings import IS_BACKGROUND_RUNNING
from juanpi_parse import JuanPiParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import datetime

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class JuanPiPinTuan(object):
    def __init__(self):
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'tuan.juanpi.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url, 得到近期所有的限时拼团商品信息
        :return:
        '''
        pintuan_goods_id_list = []
        for page in range(0, 100):
            tmp_url = 'https://tuan.juanpi.com/pintuan/get_goods_list?page={0}&pageSize=20&cid=pinhaohuo_sx&show_type=wap'.format(
                str(page)
            )
            print('正在抓取的页面地址为: ', tmp_url)

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers)
            if body == '': body = '{}'
            try:
                tmp_data = json.loads(body)
                tmp_data = tmp_data.get('data', {}).get('goods', [])
            except:
                print('json.loads转换tmp_data时出错!')
                tmp_data = []

            # print(tmp_data)
            sleep(.5)

            if tmp_data == []:
                print('该tmp_url得到的goods为空list, 此处跳过!')
                break

            tmp_pintuan_goods_id_list = [{
                'goods_id': item.get('goods_id', ''),
                'begin_time': timestamp_to_regulartime(int(item.get('start_time', ''))),
                'end_time': timestamp_to_regulartime(int(item.get('end_time', ''))),
                'all_sell_count': str(item.get('join_number_int', '')),
                'page': page,
            } for item in tmp_data]
            # print(tmp_pintuan_goods_id_list)

            for item in tmp_pintuan_goods_id_list:
                if item.get('goods_id', '') not in [item2.get('goods_id', '') for item2 in pintuan_goods_id_list]:
                    pintuan_goods_id_list.append(item)

        print('该pintuan_goods_id_list的总个数为: ', len(pintuan_goods_id_list))
        print(pintuan_goods_id_list)

        return pintuan_goods_id_list

    def _deal_with_data(self):
        '''
        处理并存储拼团商品数据
        :return:
        '''
        pintuan_goods_id_list = self._get_pintuan_goods_info()

        juanpi_pintuan = JuanPiParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        index = 1
        if my_pipeline.is_connect_success:
            sql_str = r'select goods_id, schedule, is_delete from dbo.juanpi_pintuan where site_id=18'
            db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]
            # print(db_goods_id_list)
            for item in pintuan_goods_id_list:
                if index % 5 == 0:
                    # 此处避免脚本占用大量内存
                    try: del juanpi_pintuan
                    except: pass
                    juanpi_pintuan = JuanPiParse()
                    gc.collect()

                if db_goods_id_list != []:
                    if item.get('goods_id', '') in db_goods_id_list:
                        print('该goods_id已经存在于数据库中, 此处跳过')
                        pass
                    else:
                        # * 注意卷皮的拼团时间跟它原先抓到的上下架时间是同一个时间 *
                        ## 所以就不用进行替换
                        goods_data = self.get_pintuan_goods_data(
                            juanpi_pintuan=juanpi_pintuan,
                            goods_id=item.get('goods_id', ''),
                            all_sell_count=item.get('all_sell_count', ''),
                            page=item.get('page', 0)
                        )

                        if goods_data == {}:  # 返回的data为空则跳过
                            pass
                        else:
                            # print(goods_data)
                            _r = juanpi_pintuan.insert_into_juuanpi_pintuan_table(data=goods_data, pipeline=my_pipeline)
                            if _r:  # 更新
                                db_goods_id_list.append(item.get('goods_id', ''))
                                db_goods_id_list = list(set(db_goods_id_list))

                        sleep(1)
                        index += 1

                else:
                    goods_data = self.get_pintuan_goods_data(
                        juanpi_pintuan=juanpi_pintuan,
                        goods_id=item.get('goods_id', ''),
                        all_sell_count=item.get('all_sell_count', ''),
                        page=item.get('page', 0)
                    )
                    if goods_data == {}:  # 返回的data为空则跳过
                        pass
                    else:
                        # print(goods_data)
                        _r = juanpi_pintuan.insert_into_juuanpi_pintuan_table(data=goods_data, pipeline=my_pipeline)
                        if _r:
                            db_goods_id_list.append(item.get('goods_id', ''))
                            db_goods_id_list = list(set(db_goods_id_list))

                    sleep(1)
                    index += 1

        else:
            pass
        try:
            del juanpi_pintuan
        except:
            pass
        gc.collect()

        return True

    def get_pintuan_goods_data(self, juanpi_pintuan, goods_id, all_sell_count, page):
        '''
        得到goods_data
        :param juanpi_pintuan:
        :param goods_id: 商品id
        :param page:
        :return: a dict
        '''
        tmp_url = 'http://shop.juanpi.com/deal/' + str(goods_id)
        goods_id = juanpi_pintuan.get_goods_id_from_url(tmp_url)

        juanpi_pintuan.get_goods_data(goods_id=goods_id)
        goods_data = juanpi_pintuan.deal_with_data()

        if goods_data == {}:  # 返回的data为空则跳过
            pass

        else:
            goods_data['goods_id'] = str(goods_id)
            goods_data['spider_url'] = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            goods_data['username'] = '18698570079'
            goods_data['all_sell_count'] = all_sell_count
            goods_data['page'] = page
            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = self.get_pintuan_begin_time_and_pintuan_end_time(schedule=goods_data.get('schedule', [])[0])

        gc.collect()
        return goods_data

    def get_pintuan_begin_time_and_pintuan_end_time(self, schedule):
        '''
        返回拼团开始和结束时间
        :param miaosha_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = schedule.get('begin_time')
        pintuan_end_time = schedule.get('end_time')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        juanpi_pintuan = JuanPiPinTuan()
        juanpi_pintuan._deal_with_data()
        # try:
        #     del juanpi_pintuan
        # except:
        #     pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

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