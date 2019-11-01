# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_spike.py
@Time    : 2017/11/14 13:54
@connect : superonesfazai@gmail.com
'''

import re
import time
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from settings import (
    BASE_SESSION_ID, 
    MAX_SESSION_ID, 
    SPIDER_START_HOUR, 
    SPIDER_END_HOUR, 
    ZHE_800_SPIKE_SLEEP_TIME,
    IP_POOL_TYPE,
    IS_BACKGROUND_RUNNING,
    PHANTOMJS_DRIVER_PATH,)
from zhe_800_parse import Zhe800Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from sql_str_controller import z8_select_str_5

from fzutils.spider.async_always import *

class Zhe800Spike(object):
    def __init__(self):
        self.headers = self._get_pc_headers()
        self.ip_pool_type = IP_POOL_TYPE

    @staticmethod
    def _get_pc_headers():
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'zhe800.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    @staticmethod
    def _get_begin_times_timestamp(data) -> int:
        _ = str(data.get('data', {}).get('blocks', [])[0].get('deal', {}).get('begin_time', ''))[:10]
        if _ != '':
            pass
        elif data.get('data', {}).get('blocks', [])[0].get('showcase', {}) != {}:  # 未来时间
            print('*** 未来时间 ***')
            # pprint(data.get('data', {}))
            _ = str(data.get('data', {}).get('blocks', [])[1].get('deal', {}).get('begin_time', ''))[:10]
        else:
            raise Exception
        begin_times_timestamp = int(_)  # 将如 "2017-09-28 10:00:00"的时间字符串转化为时间戳，然后再将时间戳取整

        return begin_times_timestamp

    def _get_db_goods_id_list(self, my_pipeline) -> list:
        _ = list(my_pipeline._select_table(sql_str=z8_select_str_5))
        db_goods_id_list = [item[0] for item in _]

        return db_goods_id_list

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        base_session_id = BASE_SESSION_ID
        while base_session_id < MAX_SESSION_ID:
            print('待抓取的session_id为: ', base_session_id)
            data = self._get_one_session_id_data(base_session_id=base_session_id)
            sleep(.5)
            if data.get('data', {}).get('blocks', []) == []:     # session_id不存在
                base_session_id += 2
                continue

            try:
                begin_times_timestamp = self._get_begin_times_timestamp(data)
            except Exception as e:
                print('遇到严重错误: ', e)
                base_session_id += 2
                continue

            print('秒杀时间为: ', timestamp_to_regulartime(begin_times_timestamp))
            is_recent_time = self.is_recent_time(timestamp=begin_times_timestamp)
            if not is_recent_time:  # 说明秒杀日期合法
                base_session_id += 2
                continue

            try:
                data = [item_s.get('deal', {}) for item_s in data.get('data', {}).get('blocks', [])]
            except Exception as e:
                print('遇到严重错误: ', e)
                base_session_id += 2
                continue
            # pprint(data)

            if data != []:  # 否则说明里面有数据
                miaosha_goods_list = self.get_miaoshao_goods_info_list(data=data)
                # pprint(miaosha_goods_list)

                zhe_800 = Zhe800Parse()
                my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                if my_pipeline.is_connect_success:
                    db_goods_id_list = self._get_db_goods_id_list(my_pipeline)
                    for item in miaosha_goods_list:
                        if item.get('zid', '') in db_goods_id_list:
                            print('该goods_id已经存在于数据库中, 此处跳过')
                            pass
                        else:
                            tmp_url = 'https://shop.zhe800.com/products/' + str(item.get('zid', ''))
                            goods_id = zhe_800.get_goods_id_from_url(tmp_url)

                            zhe_800.get_goods_data(goods_id=goods_id)
                            goods_data = zhe_800.deal_with_data()
                            if goods_data == {}:    # 返回的data为空则跳过
                                pass
                            else:       # 否则就解析并且插入
                                goods_data['stock_info'] = item.get('stock_info')
                                goods_data['goods_id'] = str(item.get('zid'))
                                goods_data['spider_url'] = tmp_url
                                goods_data['username'] = '18698570079'
                                goods_data['price'] = item.get('price')
                                goods_data['taobao_price'] = item.get('taobao_price')
                                goods_data['sub_title'] = item.get('sub_title')
                                # goods_data['is_baoyou'] = item.get('is_baoyou')
                                goods_data['miaosha_time'] = item.get('miaosha_time')
                                goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                                    miaosha_time=item.get('miaosha_time'))
                                goods_data['session_id'] = str(base_session_id)

                                # print(goods_data)
                                res = zhe_800.insert_into_zhe_800_xianshimiaosha_table(
                                    data=goods_data,
                                    pipeline=my_pipeline)
                                if res:
                                    if goods_id not in db_goods_id_list:
                                        db_goods_id_list.append(goods_id)

                                sleep(ZHE_800_SPIKE_SLEEP_TIME)   # 放慢速度

                    sleep(4)
                else:
                    pass
                try:
                    del zhe_800
                except:
                    pass
                gc.collect()

            else:       # 说明这个sessionid没有数据
                print('该sessionid没有相关key为jsons的数据')
                pass

            base_session_id += 2

    def _get_one_session_id_data(self, base_session_id) -> dict:
        '''
        得到一个session_id的data
        :param base_session_id:
        :return:
        '''
        _data = []
        for _page in range(1, 20):
            '''per_page为20固定，其他不返回数据'''
            headers = {
                'Sec-Fetch-Mode': 'no-cors',
                # 'Referer': 'https://g.zhe800.com/xianshiqiang/index',
                'User-Agent': get_random_phone_ua(),
            }
            params = (
                ('session_id', str(base_session_id)),
                ('page', str(_page)),
                ('source', 'h5'),
                ('new_user', '0'),
                ('per_page', '20'),
                ('callback', 'jsonp3'),
            )
            url = 'https://zapi.zhe800.com/zhe800_n_api/xsq/m/session_deals'
            body = Requests.get_url_body(
                url=url,
                headers=headers,
                params=params,
                ip_pool_type=IP_POOL_TYPE,
                proxy_type=PROXY_TYPE_HTTPS,
                timeout=15,
                num_retries=4,)
            # print(body)
            try:
                data = json_2_dict(
                    json_str=re.compile('jsonp3\((.*)\);').findall(body)[0],
                    default_res={}, )
                # pprint(data)
            except IndexError:
                sleep(.3)
                continue

            # print(type(data.get('data', {}).get('has_next')))
            if data.get('msg', '') == '无效场次':
                print('该session_id不存在，此处跳过')
                break

            if not data.get('data', {}).get('has_next', True):
                print('该session_id没有下页了!!')
                break
            else:
                print('正在抓取该session_id的第 {0} 页...'.format(_page))

            for _i in data.get('data', {}).get('blocks', []):
                _data.append(_i)

            sleep(.3)

        return {
            'data': {
                'blocks': _data,
            }
        }

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
            try:
                tmp['miaosha_time'] = {
                    'miaosha_begin_time': timestamp_to_regulartime(int(str(item.get('begin_time'))[:10])),
                    'miaosha_end_time': timestamp_to_regulartime(int(str(item.get('end_time'))[:10])),
                }
                # 折800商品地址
                tmp['zid'] = item.get('zid', '')
                assert tmp['zid'] != ''
            except (ValueError, AssertionError):
                continue

            # 限时秒杀的库存信息
            tmp['stock_info'] = {
                'activity_stock': item.get('activity_stock', 0),  # activity_stock为限时抢的剩余数量
                'stock': item.get('stock', 0),  # stock为限时秒杀的总库存
            }
            tmp['price'] = float(item.get('list_price'))
            tmp['taobao_price'] = float(item.get('price'))
            tmp['sub_title'] = item.get('description', '')
            miaosha_goods_list.append(tmp)
            # pprint(miaosha_goods_list)

        return miaosha_goods_list

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: True or False
        '''
        time_1 = int(timestamp)
        time_2 = time.time()  # 当前的时间戳
        time_1 = time.localtime(time_1)
        time_2 = time.localtime(time_2)
        if time_1.tm_year > time_2.tm_year:
            print('** 该年份为未来时间年份 **')
            if time_1.tm_hour >= SPIDER_START_HOUR and time_1.tm_hour <= SPIDER_END_HOUR:  # 规定到SPIDER_START_HOUR点到SPIDER_END_HOUR点的商品信息
                print('合法时间')
                # diff_days = abs(time_1.tm_mday - time_2.tm_mday)
                return True
            else:
                print('该小时在{0}点到{1}点以外，此处不处理跳过'.format(SPIDER_START_HOUR, SPIDER_END_HOUR))
                return False

        if time_1.tm_year == time_2.tm_year:
            if time_1.tm_mon > time_2.tm_mon:   # 先处理得到的time_1的月份大于当前月份的信息(即未来月份的)
                print('** 该月份为未来时间月份 **')
                if time_1.tm_hour >= SPIDER_START_HOUR and time_1.tm_hour <= SPIDER_END_HOUR:  # 规定到SPIDER_START_HOUR点到SPIDER_END_HOUR点的商品信息
                    print('合法时间')
                    # diff_days = abs(time_1.tm_mday - time_2.tm_mday)
                    return True
                else:
                    print('该小时在{0}点到{1}点以外，此处不处理跳过'.format(SPIDER_START_HOUR, SPIDER_END_HOUR))
                    return False

            if time_1.tm_mon >= time_2.tm_mon:  # 如果目标时间的月份时间 >= 当前月份(月份合法, 表示是当前月份或者是今年其他月份)
                if time_1.tm_mday >= time_2.tm_mday-2:  # 这样能抓到今天的前两天的信息
                    if time_1.tm_hour >= SPIDER_START_HOUR and time_1.tm_hour <= SPIDER_END_HOUR:    # 规定到SPIDER_START_HOUR点到SPIDER_END_HOUR点的商品信息
                        print('合法时间')
                        # diff_days = abs(time_1.tm_mday - time_2.tm_mday)
                        return True
                    else:
                        print('该小时在{0}点到{1}点以外，此处不处理跳过'.format(SPIDER_START_HOUR, SPIDER_END_HOUR))
                        return False
                else:
                    print('该日时间已过期, 此处跳过')
                    return False
            else:  # 月份过期
                print('该月份时间已过期，此处跳过')
                return False

        else:
            print('非本年度的限时秒杀时间，此处跳过')
            return False

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        zhe_800_spike = Zhe800Spike()
        zhe_800_spike.get_spike_hour_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(10*60)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()
