# coding:utf-8

'''
@author = super_fazai
@File    : chuchujie_miaosha_real-times_update.py
@Time    : 2018/2/25 10:30
@connect : superonesfazai@gmail.com
'''

"""
楚楚街秒杀实时更新脚本
"""

import sys
sys.path.append('..')

from chuchujie_9_9_parse import ChuChuJie_9_9_Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import re
import json
from pprint import pprint
import time

from settings import IS_BACKGROUND_RUNNING, CHUCHUJIE_SLEEP_TIME
from decimal import Decimal

from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class ChuChuJieMiaosShaRealTimeUpdate(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = 'delete from dbo.chuchujie_xianshimiaosha where goods_id=%s'

    def _set_headers(self):
        self.headers = {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'api.chuchujie.com',
            'Referer': 'https://m.chuchujie.com/?module=99',
            'Cache-Control': 'max-age=0',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = r'select goods_id, miaosha_time, gender, page, goods_url from dbo.chuchujie_xianshimiaosha where site_id=24'
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
                chuchujie_miaosha = ChuChuJie_9_9_Parse()
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(miaosha_end_time) == 0:
                        tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀结束时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_end_time'))

                    elif self.is_recent_time(miaosha_end_time) == 2:
                        # break       # 跳出循环
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:   # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        data['goods_id'] = item[0]

                        body = self.get_one_page_goods_info(item[2], item[3])

                        if body == '{}':
                            # 可能是网络原因导致, 先跳过
                            pass

                        else:
                            try:
                                json_body = json.loads(body)
                                # print(json_body)
                            except:
                                print('json.loads转换body时出错!请检查')
                                json_body = {}
                                pass

                            try:
                                this_page_total_count = json_body.get('data', {}).get('groupList', [])[0].get('totalCount', 0)
                            except IndexError:
                                print('获取this_page_total_count时出错, 请检查!')
                                this_page_total_count = 0

                            # 获取对应gender, page的商品list
                            if this_page_total_count == 0:
                                item_list = []

                            else:
                                tmp_goods_list = json_body.get('data', {}).get('groupList', [])[0].get('dataList', [])

                                item_list = [{
                                    'goods_id': str(item_s.get('chuchuId', '')),
                                    'sub_title': item_s.get('description', ''),
                                } for item_s in tmp_goods_list]

                            if item_list == []:
                                print('#### 该gender, page对应得到的item_list为空[]!')
                                print('该商品已被下架限时秒杀活动，此处将其删除')
                                tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                pass

                            else:
                                # miaosha_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in item_list]

                                """
                                由于不会内部提前下架，所以在售卖时间内的全部进行相关更新
                                """
                                # if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                                #     print('该商品已被下架限时秒杀活动，此处将其删除')
                                #     tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                #     print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                #     pass
                                #
                                # else:  # 未下架的
                                '''
                                不更新秒杀时间和sub_title, 只更新其他相关数据
                                '''
                                # for item_2 in item_list:
                                #     if item_2.get('goods_id', '') == item[0]:
                                chuchujie_miaosha.get_goods_data(goods_id=item[0])
                                goods_data = chuchujie_miaosha.deal_with_data()

                                if goods_data == {}:  # 返回的data为空则跳过
                                    pass
                                else:
                                    goods_data['goods_id'] = str(item[0])

                                    # goods_data['sub_title'] = item_2.get('sub_title', '')

                                    # print(goods_data)
                                    chuchujie_miaosha.update_chuchujie_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                                    sleep(CHUCHUJIE_SLEEP_TIME)

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

    def get_one_page_goods_info(self, *params):
        '''
        得到一个页面的html代码
        :param params: 待传入的参数
        :return: '{}' or str
        '''
        gender, page = params
        tmp_url = 'https://api.chuchujie.com/api/'

        client = {
            "ageGroup": "AG_0to24",
            "channel": "QD_web_webkit",
            "deviceId": "0",
            "gender": gender,  # '0' -> 女 | '1' -> 男
            "imei": "0",
            "packageName": "com.culiu.purchase",
            "platform": "wap",
            "sessionId": "0",
            "shopToken": "0",
            "userId": "0",
            "version": "1.0",
            "xingeToken": ""
        }

        query = {
            "group": 4,
            "module": "99",
            "page": page,
            "tab": "all"
        }

        # 切记: Query String Parameters直接这样编码发送即可
        # 如果是要post的数据就得使用post的方法
        data = {
            'client': json.dumps(client),
            'query': json.dumps(query),
            'page': page
        }

        body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, params=data)
        if body == '':
            body = '{}'

        return body

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -86400:  # (为了后台能同步下架)所以设置为 24个小时
            # if diff_time < 0:     # (原先的时间)结束时间 与当前时间差 <= 0
            return 0  # 已过期恢复原价的
        elif diff_time > 0:
            return 1  # 表示是昨天跟今天的也就是待更新的
        else:  # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
            return 2

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = ChuChuJieMiaosShaRealTimeUpdate()
        tmp.run_forever()
        try:
            del tmp
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))
        sleep(2*60)

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