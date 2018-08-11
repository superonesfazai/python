# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_miaosha_real-times_update.py
@Time    : 2017/11/16 15:57
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from zhe_800_parse import Zhe800Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
import json
from pprint import pprint
import time
from logging import (
    INFO,
    ERROR,
)
from settings import IS_BACKGROUND_RUNNING, MY_SPIDER_LOGS_PATH

from zhe_800_spike import Zhe800Spike

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
    datetime_to_timestamp,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time
from fzutils.internet_utils import get_random_pc_ua
from fzutils.log_utils import set_logger

class Zhe_800_Miaosha_Real_Time_Update(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = 'delete from dbo.zhe_800_xianshimiaosha where goods_id=%s'
        self.zhe_800_spike = Zhe800Spike()
        self._set_logger()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'zhe800.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _set_logger(self):
        self.my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/折800/秒杀实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=INFO
        )

    def run_forever(self):
        '''
        这个实时更新的想法是只更新当天前天未来两小时的上架商品的信息，再未来信息价格(全为原价)暂不更新
        :return:
        '''
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = '''
        select goods_id, miaosha_time, session_id 
        from dbo.zhe_800_xianshimiaosha 
        where site_id=14 and is_delete = 0
        '''
        # 删除过期2天的的
        tmp_del_str = 'delete from dbo.zhe_800_xianshimiaosha where GETDATE()-miaosha_end_time>2'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
            tmp_sql_server._delete_table(sql_str=tmp_del_str, params=None)
        except TypeError:
            self.my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(str(result))
            print('--------------------------------------------------------')

            self.my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            self._update_old_goods_info(tmp_sql_server=tmp_sql_server, result=result)

        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            sleep(10*60)

        return

    def _update_old_goods_info(self, tmp_sql_server, result):
        '''
        更新old goods info
        :param result:
        :return:
        '''
        index = 1
        for item in result:  # 实时更新数据
            miaosha_begin_time = json.loads(item[1]).get('miaosha_begin_time')
            miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')))[0:10])
            # self.my_lg.info(str(miaosha_begin_time))

            data = {}
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            zhe_800_miaosha = Zhe800Parse()
            if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                print('正在重置，并与数据库建立新连接中...')
                tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                print('与数据库的新连接成功建立...')

            if tmp_sql_server.is_connect_success:
                if self.is_recent_time(miaosha_begin_time) == 0:
                    tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0],))
                    self.my_lg.info('过期的goods_id为({0}), 限时秒杀开始时间为({1}), 删除成功!'.format(item[0], json.loads(item[1]).get('miaosha_begin_time')))

                elif self.is_recent_time(miaosha_begin_time) == 2:
                    pass  # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                else:  # 返回1，表示在待更新区间内
                    print('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(item[0], index))
                    data['goods_id'] = item[0]

                    try:
                        tmp_data = self.zhe_800_spike._get_one_session_id_data(base_session_id=str(item[2]))
                    except Exception:
                        self.my_lg.error(msg='', exc_info=True)
                        continue

                    if tmp_data.get('data', {}).get('blocks', []) == []:  # session_id不存在
                        self.my_lg.info('该session_id不存在，此处跳过')
                        pass

                    else:
                        tmp_data = [item_s.get('deal', {}) for item_s in tmp_data.get('data', {}).get('blocks', [])]
                        if tmp_data != []:  # 否则说明里面有数据
                            miaosha_goods_list = self.get_miaoshao_goods_info_list(data=tmp_data)
                            # pprint(miaosha_goods_list)

                            # 该session_id中现有的所有zid的list
                            miaosha_goods_all_goods_id = [i.get('zid') for i in miaosha_goods_list]

                            if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                                # tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0],))
                                self._update_is_delete(tmp_sql_server=tmp_sql_server, goods_id=item[0])
                                self.my_lg.info('该商品已被官方下架限秒活动! 下架的goods_id为({0}), 逻辑删除成功!'.format(item[0]))
                                pass

                            else:  # 未下架的
                                for item_1 in miaosha_goods_list:
                                    if item_1.get('zid', '') == item[0]:
                                        zhe_800_miaosha.get_goods_data(goods_id=item[0])
                                        goods_data = zhe_800_miaosha.deal_with_data()

                                        if goods_data == {}:  # 返回的data为空则跳过
                                            pass
                                        else:  # 否则就解析并且插入
                                            goods_data['stock_info'] = item_1.get('stock_info')
                                            goods_data['goods_id'] = str(item_1.get('zid'))
                                            # goods_data['username'] = '18698570079'
                                            if item_1.get('stock_info').get('activity_stock') > 0:
                                                goods_data['price'] = item_1.get('price')
                                                goods_data['taobao_price'] = item_1.get('taobao_price')
                                            else:
                                                pass
                                            goods_data['sub_title'] = item_1.get('sub_title')
                                            goods_data['miaosha_time'] = item_1.get('miaosha_time')
                                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                                                miaosha_time=item_1.get('miaosha_time'))

                                            if goods_data.get('is_delete', 0) == 1:
                                                self.my_lg.info('该商品[{0}]已售罄...'.format(item[0]))

                                            # self.my_lg.info(str(goods_data['stock_info']))
                                            # self.my_lg.info(str(goods_data['miaosha_time']))
                                            zhe_800_miaosha.to_update_zhe_800_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                                    else:
                                        pass

                        else:  # 说明这个sessionid没有数据, 就删除对应这个sessionid的限时秒杀商品
                            self._update_is_delete(tmp_sql_server=tmp_sql_server, goods_id=item[0])
                            self.my_lg.info('该sessionid没有相关key为jsons的数据! 过期的goods_id为({0}), 限时秒杀开始时间为({1}), 删除成功!'.format(item[0], json.loads(item[1]).get('miaosha_begin_time')))
                            pass

            else:  # 表示返回的data值为空值
                self.my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
                pass
            index += 1
            # try:
            #     del tmall
            # except:
            #     pass
            # sleep(.8)
            gc.collect()
        self.my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        gc.collect()

        return

    def _update_is_delete(self, tmp_sql_server, goods_id):
        '''
        下架商品逻辑删除
        :param goods_id:
        :return:
        '''
        delete_str = 'update dbo.zhe_800_xianshimiaosha set is_delete = 1 where goods_id=%s'
        tmp_sql_server._update_table(sql_str=delete_str, params=(goods_id,))

        return

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = datetime_to_timestamp(get_shanghai_time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -259200:     # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        # if diff_time < -172800:     # (原先的时间)48个小时, 只需要跟新过去48小时和对与当前时间的未来2小时的商品信息
            return 0    # 已过期恢复原价的
        elif diff_time > -172800 and diff_time < 7200:
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:
            return 2    # 未来时间的暂时不用更新

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
            tmp['miaosha_time'] = {
                'miaosha_begin_time': timestamp_to_regulartime(int(str(item.get('begin_time'))[0:10])),
                'miaosha_end_time': timestamp_to_regulartime(int(str(item.get('end_time'))[0:10])),
            }

            # 折800商品地址
            tmp['zid'] = item.get('zid')
            # 是否包邮
            # tmp['is_baoyou'] = item.get('is_baoyou', 0)
            # 限时秒杀的库存信息
            tmp['stock_info'] = {
                'activity_stock': item.get('activity_stock', 0),  # activity_stock为限时抢的剩余数量
                'stock': item.get('stock', 0),  # stock为限时秒杀的总库存
            }
            # 原始价格
            tmp['price'] = float(item.get('list_price'))
            # 秒杀的价格, float类型
            tmp['taobao_price'] = float(item.get('price'))
            # 子标题
            tmp['sub_title'] = item.get('description', '')
            miaosha_goods_list.append(tmp)
            # pprint(miaosha_goods_list)

        return miaosha_goods_list

    def __del__(self):
        try:
            del self.zhe_800_spike
            del self.my_lg
        except: pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Zhe_800_Miaosha_Real_Time_Update()
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
