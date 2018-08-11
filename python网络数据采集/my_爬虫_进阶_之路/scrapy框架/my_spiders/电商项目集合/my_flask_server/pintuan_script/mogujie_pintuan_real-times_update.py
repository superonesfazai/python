# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_pintuan_real-times_update.py
@Time    : 2018/2/5 19:01
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from mogujie_parse import MoGuJieParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import re, datetime
import json
from pprint import pprint
import time
from settings import (
    IS_BACKGROUND_RUNNING,
    MOGUJIE_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,
)

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import MyPhantomjs

class MoGuJiePinTuanRealTimesUpdate(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = 'delete from dbo.mogujie_pintuan where goods_id=%s'

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'list.mogujie.com',
            # 'Referer': 'https://pintuan.mogujie.com/ptpt/app/pd?acm=3.mce.1_10_1fvsk.51827.0.mUTadqIzS9Pbg.m_370494-pos_2-mf_4537_796033&ptp=m1._mf1_1239_4537._keyword_51827.0.xLt0G92',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = r'select goods_id, miaosha_time, fcid, page from dbo.mogujie_pintuan where site_id=23'
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

            self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)
            for item in result:  # 实时更新数据
                pintuan_end_time = json.loads(item[1]).get('end_time')
                pintuan_end_time = int(str(time.mktime(time.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                data = {}
                mogujie_pintuan = MoGuJieParse()
                if index % 8 == 0:
                    try: del self.my_phantomjs
                    except:pass
                    gc.collect()
                    self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(pintuan_end_time) == 0:
                        tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                        print('过期的goods_id为(%s)' % item[0], ', 拼团开始时间为(%s), 删除成功!' % json.loads(item[1]).get('begin_time'))

                    elif self.is_recent_time(pintuan_end_time) == 2:
                        # break       # 跳出循环
                        pass  # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        data['goods_id'] = item[0]

                        tmp_url = 'http://list.mogujie.com/search?page={0}&fcid={1}&algoKey=pc_tuan_book_pop&cKey=pc-tuan'.format(
                            item[3], item[2]
                        )
                        # print(tmp_url)

                        # requests请求不到数据，涉及证书认证，直接用phantomjs
                        # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
                        body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)
                        # print(body)

                        if body == '':
                            print('获取到的body为空值! 此处跳过')

                        else:
                            try:
                                body = re.compile(r'<pre.*?>(.*?)</pre>').findall(body)[0]
                                tmp_data = json.loads(body)
                                # pprint(tmp_data)
                            except:
                                print('json.loads转换body时出错, 请检查')
                                tmp_data = {}

                            if tmp_data.get('result', {}).get('wall', {}).get('docs', []) == []:
                                print('得到的docs为[]!')
                                print('该商品已被下架限时秒杀活动，此处将其删除')
                                tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                pass

                            else:
                                tmp_item_list = tmp_data.get('result', {}).get('wall', {}).get('docs', [])
                                # print(tmp_item_list)
                                # pprint(tmp_item_list)

                                begin_time_timestamp = int(time.time())  # 开始拼团的时间戳
                                item_list = [{
                                    'goods_id': item.get('tradeItemId', ''),
                                    'pintuan_time': {
                                        'begin_time': timestamp_to_regulartime(timestamp=begin_time_timestamp),
                                        'end_time': timestamp_to_regulartime(self.get_pintuan_end_time(begin_time_timestamp, item.get('leftTimeOrg', ''))),
                                    },
                                    'all_sell_count': str(item.get('salesVolume', 0)),
                                } for item in tmp_item_list]
                                # print(item_list)

                                pintuan_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in item_list]
                                # print(pintuan_goods_all_goods_id)

                                '''
                                内部已经下架的(内部下架的其实并未真实下架，还在卖的，所以我就更新其商品信息数据，不更新上下架时间)
                                '''
                                if item[0] not in pintuan_goods_all_goods_id:
                                    # print('该商品已被下架限时秒杀活动，此处将其删除')
                                    # tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                    # print('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                                    # pass
                                    mogujie_pintuan.get_goods_data(goods_id=item[0])
                                    goods_data = mogujie_pintuan.deal_with_data()

                                    if goods_data == {}:
                                        pass
                                    else:
                                        # 规范化
                                        print('+++ 内部下架，其实还在售卖的商品更新')
                                        tmp_price_info_list = goods_data['price_info_list']
                                        price_info_list = [{
                                            'spec_value': item_4.get('spec_value'),
                                            'pintuan_price': item_4.get('detail_price'),
                                            'detail_price': '',
                                            'normal_price': item_4.get('normal_price'),
                                            'img_url': item_4.get('img_url'),
                                            'rest_number': item_4.get('rest_number'),
                                        } for item_4 in tmp_price_info_list]

                                        goods_data['goods_id'] = item[0]
                                        goods_data['price_info_list'] = price_info_list

                                        # pprint(goods_data)
                                        # print(goods_data)
                                        mogujie_pintuan.update_mogujie_pintuan_table_2(data=goods_data, pipeline=tmp_sql_server)
                                        sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

                                else:   # 未下架的
                                    for item_2 in item_list:
                                        if item_2.get('goods_id', '') == item[0]:
                                            mogujie_pintuan.get_goods_data(goods_id=item[0])
                                            goods_data = mogujie_pintuan.deal_with_data()

                                            if goods_data == {}: pass
                                            else:
                                                # 规范化
                                                tmp_price_info_list = goods_data['price_info_list']
                                                price_info_list = [{
                                                    'spec_value': item_4.get('spec_value'),
                                                    'pintuan_price': item_4.get('detail_price'),
                                                    'detail_price': '',
                                                    'normal_price': item_4.get('normal_price'),
                                                    'img_url': item_4.get('img_url'),
                                                    'rest_number': item_4.get('rest_number'),
                                                } for item_4 in tmp_price_info_list]

                                                goods_data['goods_id'] = item[0]
                                                goods_data['price_info_list'] = price_info_list
                                                goods_data['pintuan_time'] = item_2.get('pintuan_time', {})
                                                goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = self.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=goods_data['pintuan_time'])
                                                goods_data['all_sell_count'] = item_2.get('all_sell_count', '')

                                                # pprint(goods_data)
                                                # print(goods_data)
                                                mogujie_pintuan.update_mogujie_pintuan_table(data=goods_data, pipeline=tmp_sql_server)
                                                sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

                                        else: pass

                else:
                    print('数据库连接失败，此处跳过!')
                    pass

                index += 1
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                sleep(60 * 60 * 5.5)
            else:
                sleep(5)
            gc.collect()

    def get_pintuan_begin_time_and_pintuan_end_time(self, pintuan_time):
        '''
        返回拼团开始和结束时间
        :param pintuan_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = pintuan_time.get('begin_time', '')
        pintuan_end_time = pintuan_time.get('end_time', '')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

    def get_pintuan_end_time(self, begin_time, left_time):
        '''
        处理并得到拼团结束时间
        :param begin_time: 秒杀开始时间戳
        :param left_time: 剩余时间字符串
        :return: end_time 时间戳(int)
        '''
        # 'leftTimeOrg': '6天13小时'
        # 'leftTimeOrg': '13小时57分'

        had_day = re.compile(r'天').findall(left_time)
        had_hour = re.compile(r'小时').findall(left_time)
        had_min = re.compile(r'分').findall(left_time)

        tmp = re.compile(r'\d+').findall(left_time)
        if had_day != [] and had_hour != []:    # left_time 格式为 '6天13小时'
            day, hour, min = int(tmp[0]), int(tmp[1]), 0

        elif had_day == [] and had_hour != []:  # left_time 格式为 '13小时57分'
            day, hour, min = 0, int(tmp[0]), int(tmp[1])

        elif had_day == [] and had_hour == []:  # left_time 格式为 '36分'
            print('left_time = ', left_time)
            day, hour, min = 0, 0, int(tmp[0])

        else:               # 无天, 小时, 分
            print('day, hour, min = 0, 0, 0', 'left_time = ', left_time)
            day, hour, min = 0, 0, 0

        left_end_time_timestamp = \
            day * 24 * 60 * 60 + \
            hour * 60 * 60 + \
            min * 60

        return begin_time + left_end_time_timestamp

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

    def __del__(self):
        try: del self.my_phantomjs
        except: pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = MoGuJiePinTuanRealTimesUpdate()
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