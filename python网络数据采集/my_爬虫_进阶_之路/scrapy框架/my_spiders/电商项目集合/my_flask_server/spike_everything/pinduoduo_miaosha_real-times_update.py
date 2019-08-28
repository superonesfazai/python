# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_miaosha_real-times_update.py
@connect : superonesfazai@gmail.com
'''

"""
拼多多退货严重, 不维护
"""

import sys
sys.path.append('..')

from pinduoduo_parse import PinduoduoParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
import json
from pprint import pprint
import time
from settings import (
    IS_BACKGROUND_RUNNING, 
    PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST, 
    PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST,
    IP_POOL_TYPE,)

from settings import (
    PHANTOMJS_DRIVER_PATH, 
    PINDUODUO_SLEEP_TIME,)
from multiplex_code import (
    _block_print_db_old_data,
    _block_get_new_db_conn,
)

from sql_str_controller import (
    pd_delete_str_1,
    pd_select_str_2,
)

from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

'''
实时更新拼多多秒杀信息
'''

class Pinduoduo_Miaosha_Real_Time_Update(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = pd_delete_str_1
        self.ip_pool_type = IP_POOL_TYPE
        self.driver = BaseDriver(executable_path=EXECUTABLE_PATH, ip_pool_type=self.ip_pool_type)

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

    def run_forever(self):
        '''
        这个实时更新的想法是只更新当天未来2小时的上架商品的信息，再未来信息价格(全为原价)暂不更新
        :return:
        '''
        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(sql_cli._select_table(sql_str=pd_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            pinduoduo_miaosha = PinduoduoParse()

            all_miaosha_goods_list = self.get_all_miaosha_goods_list()

            # 其中所有goods_id的list
            miaosha_goods_all_goods_id = [i.get('goods_id') for i in all_miaosha_goods_list]
            # print(miaosha_goods_all_goods_id)

            for item in result:  # 实时更新数据
                # 对于拼多多先拿到该商品的结束时间点
                miaosha_end_time = json.loads(item[1]).get('miaosha_end_time')
                miaosha_end_time = int(str(time.mktime(time.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50)
                if sql_cli.is_connect_success:
                    if self.is_recent_time(miaosha_end_time) == 0:
                        sql_cli._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀结束时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_end_time'))
                        sleep(.3)

                    elif self.is_recent_time(miaosha_end_time) == 2:
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))

                        if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                            '''
                            表示其中没有了该goods_id
                            '''
                            sql_cli._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                            print('该商品[goods_id为(%s)]已被下架限时秒杀活动，此处将其删除' % item[0])
                            sleep(.3)

                        else:       # 未下架的
                            for item_1 in all_miaosha_goods_list:
                                if item_1.get('goods_id', '') == item[0]:
                                    # # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                                    # pinduoduo_miaosha = PinduoduoParse()
                                    pinduoduo_miaosha.get_goods_data(goods_id=item[0])
                                    goods_data = pinduoduo_miaosha.deal_with_data()

                                    if goods_data == {}:  # 返回的data为空则跳过
                                        # sleep(3)
                                        pass
                                    else:  # 否则就解析并且插入
                                        goods_data['stock_info'] = item_1.get('stock_info')
                                        goods_data['goods_id'] = item_1.get('goods_id')
                                        if item_1.get('stock_info').get('activity_stock') > 0:
                                            goods_data['price'] = item_1.get('price')  # 秒杀前的原特价
                                            goods_data['taobao_price'] = item_1.get('taobao_price')  # 秒杀价
                                        else:
                                            pass
                                        goods_data['sub_title'] = item_1.get('sub_title', '')
                                        goods_data['miaosha_time'] = item_1.get('miaosha_time')
                                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item_1.get('miaosha_time'))

                                        if item_1.get('stock_info').get('activity_stock') <= 1:
                                            # 实时秒杀库存小于等于1时就标记为 已售罄
                                            print('该秒杀商品已售罄...')
                                            goods_data['is_delete'] = 1

                                        # print(goods_data)
                                        pinduoduo_miaosha.to_update_pinduoduo_xianshimiaosha_table(data=goods_data, pipeline=sql_cli)
                                    sleep(PINDUODUO_SLEEP_TIME)
                                else:
                                    pass

                    index += 1
                    gc.collect()

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(3 * 60)
        # del ali_1688
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
        # print('待爬取的今日限时秒杀数据的地址为: ', tmp_url)
        today_data = get_data(body=self.driver.get_url_body(url=tmp_url))
        today_data = self.json_to_dict(tmp_data=today_data)

        # 明日的秒杀
        tmp_url_2 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/tomorrow?page=0&size=2000'
        # print('待爬取的明日限时秒杀数据的地址为: ', tmp_url_2)
        tomorrow_data = get_data(body=self.driver.get_url_body(url=tmp_url_2))
        tomorrow_data = self.json_to_dict(tmp_data=tomorrow_data)

        # 未来的秒杀
        tmp_url_3 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/all_after?page=0&size=2000'
        # print('待爬取的未来限时秒杀数据的地址为: ', tmp_url_3)
        all_after_data = get_data(body=self.driver.get_url_body(url=tmp_url_3))
        all_after_data = self.json_to_dict(tmp_data=all_after_data)

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
        # print('当前所有限时秒杀商品list为: ', all_miaosha_goods_list)

        return all_miaosha_goods_list

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

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestr: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time <= -86400:     # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        # if diff_time <= 0:
            return 0    # 已过期恢复原价的
        elif diff_time > 0 and diff_time <= 7200:   # 未来2小时的
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:
            return 2    # 未来时间的暂时不用更新

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Pinduoduo_Miaosha_Real_Time_Update()
        tmp.run_forever()
        try:
            del tmp
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))
        sleep(3*60)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()