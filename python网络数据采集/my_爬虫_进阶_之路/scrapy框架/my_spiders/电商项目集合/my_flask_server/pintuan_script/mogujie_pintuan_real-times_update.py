# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_pintuan_real-times_update.py
@Time    : 2018/2/3 19:01
@connect : superonesfazai@gmail.com
'''

# TODO 蘑菇街官方已下架拼团板块, 本爬虫不再维护!

import sys
sys.path.append('..')

from mogujie_parse import MoGuJieParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import re
import json
from pprint import pprint
import time
from settings import (
    IS_BACKGROUND_RUNNING,
    MOGUJIE_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,
)

from sql_str_controller import (
    mg_select_str_2,
    mg_delete_str_2,
    mg_update_str_5,
)
from multiplex_code import (
    _get_mogujie_pintuan_price_info_list,
    _block_print_db_old_data,
    _block_get_new_db_conn,
    _handle_goods_shelves_in_auto_goods_table,)

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
    datetime_to_timestamp,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time

class MoGuJiePinTuanRealTimesUpdate(object):
    def __init__(self):
        self._set_headers()
        self.ip_pool_type = IP_POOL_TYPE

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
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            sql_cli._delete_table(sql_str=mg_delete_str_2)
            result = list(sql_cli._select_table(sql_str=mg_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            self.my_phantomjs = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, ip_pool_type=self.ip_pool_type)
            for item in result:  # 实时更新数据
                goods_id = item[0]
                pintuan_end_time = json.loads(item[1]).get('end_time')
                pintuan_end_time = int(str(time.mktime(time.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                data = {}
                mogujie_pintuan = MoGuJieParse()
                if index % 8 == 0:
                    try: del self.my_phantomjs
                    except:pass
                    gc.collect()
                    self.my_phantomjs = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, ip_pool_type=self.ip_pool_type)

                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50)
                if sql_cli.is_connect_success:
                    if self.is_recent_time(pintuan_end_time) == 0:
                        _handle_goods_shelves_in_auto_goods_table(
                            goods_id=goods_id,
                            update_sql_str=mg_update_str_5,
                            sql_cli=sql_cli,
                        )
                        print('过期的goods_id为(%s)' % goods_id, ', 拼团开始时间为(%s), 逻辑删除成功!' % json.loads(item[1]).get('begin_time'))
                        sleep(.3)

                    elif self.is_recent_time(pintuan_end_time) == 2:
                        # break       # 跳出循环
                        pass  # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                        data['goods_id'] = goods_id

                        tmp_url = 'http://list.mogujie.com/search?page={0}&fcid={1}&algoKey=pc_tuan_book_pop&cKey=pc-tuan'.format(
                            item[3], item[2]
                        )
                        # print(tmp_url)

                        # requests请求不到数据，涉及证书认证，直接用phantomjs
                        # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
                        body = self.my_phantomjs.get_url_body(url=tmp_url)
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
                                _handle_goods_shelves_in_auto_goods_table(
                                    goods_id=goods_id,
                                    update_sql_str=mg_update_str_5,
                                    sql_cli=sql_cli,)
                                sleep(.3)

                            else:
                                tmp_item_list = tmp_data.get('result', {}).get('wall', {}).get('docs', [])
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
                                # pprint(item_list)

                                pintuan_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in item_list]
                                # print(pintuan_goods_all_goods_id)

                                '''
                                内部已经下架的(内部下架的其实并未真实下架，还在卖的，所以我就更新其商品信息数据，不更新上下架时间)
                                '''
                                if goods_id not in pintuan_goods_all_goods_id:
                                    mogujie_pintuan.get_goods_data(goods_id=goods_id)
                                    goods_data = mogujie_pintuan.deal_with_data()

                                    if goods_data == {}:
                                        pass
                                    else:
                                        # 规范化
                                        print('+++ 内部下架，其实还在售卖的商品更新')
                                        goods_data['goods_id'] = goods_id
                                        goods_data['price_info_list'] = _get_mogujie_pintuan_price_info_list(goods_data['price_info_list'])

                                        # pprint(goods_data)
                                        mogujie_pintuan.update_mogujie_pintuan_table_2(data=goods_data, pipeline=sql_cli)
                                        sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

                                else:   # 未下架的
                                    for item_2 in item_list:
                                        if item_2.get('goods_id', '') == goods_id:
                                            mogujie_pintuan.get_goods_data(goods_id=goods_id)
                                            goods_data = mogujie_pintuan.deal_with_data()

                                            if goods_data == {}: pass
                                            else:
                                                # 规范化
                                                goods_data['goods_id'] = goods_id
                                                goods_data['price_info_list'] = _get_mogujie_pintuan_price_info_list(goods_data['price_info_list'])
                                                goods_data['pintuan_time'] = item_2.get('pintuan_time', {})
                                                goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['pintuan_time'])
                                                goods_data['all_sell_count'] = item_2.get('all_sell_count', '')

                                                # pprint(goods_data)
                                                mogujie_pintuan.update_mogujie_pintuan_table(data=goods_data, pipeline=sql_cli)
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
            sleep(10 * 60)
        gc.collect()

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
        time_2 = int(datetime_to_timestamp(get_shanghai_time()))  # 当前的时间戳

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