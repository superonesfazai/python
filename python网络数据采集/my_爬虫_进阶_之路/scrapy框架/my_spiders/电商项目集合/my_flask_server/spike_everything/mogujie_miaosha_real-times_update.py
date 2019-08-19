# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_miaosha_real-times_update.py
@Time    : 2018/2/1 09:29
@connect : superonesfazai@gmail.com
'''

'''
蘑菇街秒杀商品实时更新脚本(新版无秒杀板块, 不再进行维护!)
'''

import sys
sys.path.append('..')

from mogujie_miaosha_parse import MoGuJieMiaoShaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import json
import time
from settings import (
    IS_BACKGROUND_RUNNING, 
    MOGUJIE_SLEEP_TIME,
    IP_POOL_TYPE,)
from decimal import Decimal
from multiplex_code import (
    _block_print_db_old_data,
    _handle_goods_shelves_in_auto_goods_table,
    async_get_ms_begin_time_and_miaos_end_time_from_ms_time,
)

from sql_str_controller import (
    mg_delete_str_3,
    mg_select_str_3,
    mg_delete_str_4,
    mg_update_str_1,
)

from fzutils.spider.async_always import *

class MoGuJieMiaoShaRealTimeUpdate(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = mg_delete_str_3
        self.ip_pool_type = IP_POOL_TYPE

    def _set_headers(self):
        self.headers = get_random_headers(
            upgrade_insecure_requests=False,
        )
        self.headers.update({
            'Host': 'm.mogujie.com',
        })

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            tmp_sql_server._delete_table(sql_str=mg_delete_str_4)
            sleep(5)
            result = list(tmp_sql_server._select_table(sql_str=mg_select_str_3))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            for item in result:  # 实时更新数据
                goods_id = item[0]
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
                        tmp_sql_server._update_table(sql_str=mg_update_str_1, params=(goods_id,))
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))
                        sleep(.5)

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
                            print('该商品已被下架限时秒杀活动，此处将其逻辑删除')
                            tmp_sql_server._update_table(sql_str=mg_update_str_1, params=(item[0],))
                            print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                            sleep(.4)   # 避免死锁

                        else:
                            # 该event_time中现有的所有goods_id的list
                            miaosha_goods_all_goods_id = [item_1.get('iid', '') for item_1 in item_list]
                            if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                                print('该商品已被下架限时秒杀活动，此处将其逻辑删除')
                                tmp_sql_server._update_table(sql_str=mg_update_str_1, params=(item[0],))
                                print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                sleep(.4)

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
                                                sleep(MOGUJIE_SLEEP_TIME)
                                                continue

                                            goods_data['miaosha_time'] = {
                                                'miaosha_begin_time': timestamp_to_regulartime(int(item_2.get('startTime', 0))),
                                                'miaosha_end_time': timestamp_to_regulartime(int(item_2.get('endTime', 0))),
                                            }
                                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                                            # print(goods_data['title'])

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
                collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        collect()

    def get_item_list(self, event_time):
        '''
        得到event_time中所有的商品信息
        :param event_time:
        :return: item_list 类型 list
        '''
        tmp_url = 'https://qiang.mogujie.com//jsonp/fastBuyListActionLet/1?eventTime={0}&bizKey=rush_main'.format(str(event_time))
        body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
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
        collect()
        print('一次大更新完毕'.center(30, '-'))

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