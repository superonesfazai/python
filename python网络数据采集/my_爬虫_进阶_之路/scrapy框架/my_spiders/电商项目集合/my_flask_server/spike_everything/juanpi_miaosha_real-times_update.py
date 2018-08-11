# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_miaosha_real-times_update.py
@Time    : 2017/11/21 11:42
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from juanpi_parse import JuanPiParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import json
from pprint import pprint
import time
from settings import IS_BACKGROUND_RUNNING

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

'''
实时更新卷皮秒杀信息(卷皮频繁地更新商品所在限时秒杀列表)
'''

class Juanpi_Miaosha_Real_Time_Update(object):
    def __init__(self):
        self._set_headers()
        self.delete_sql_str = 'delete from dbo.juanpi_xianshimiaosha where goods_id=%s'

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
        这个实时更新的想法是只更新当天前天未来14小时的上架商品的信息，再未来信息价格(全为原价)暂不更新
        :return:
        '''
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = '''
        select goods_id, miaosha_time, tab_id, page 
        from dbo.juanpi_xianshimiaosha 
        where site_id=15
        order by id asc
        '''
        # 删除过期2天的的
        tmp_del_str = 'delete from dbo.juanpi_xianshimiaosha where GETDATE()-miaosha_end_time>2'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
            tmp_sql_server._delete_table(sql_str=tmp_del_str, params=None)
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

            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            juanpi_miaosha = JuanPiParse()

            for item in result:  # 实时更新数据
                miaosha_begin_time = json.loads(item[1]).get('miaosha_begin_time')
                miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time,'%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_begin_time)

                if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(miaosha_begin_time) == 0:
                        tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]), lock_timeout=2000)
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))

                    elif self.is_recent_time(miaosha_begin_time) == 2:
                        # break       # 跳出循环
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))

                        tmp_url = 'https://m.juanpi.com/act/timebuy-xrgoodslist?tab_id={0}&page={1}'.format(
                            str(item[2]), str(item[3]),
                        )
                        # print('待爬取的tab_id, page地址为: ', tmp_url)

                        data = MyRequests.get_url_body(url=tmp_url, headers=self.headers)
                        if data == '': break

                        try:
                            data = json.loads(data)
                            data = data.get('data', {})
                            # print(data)
                        except:
                            break

                        if data.get('goodslist') == []:
                            print('tab_id={0}, page={1}的goodslist为[], 此处跳过'.format(item[2], item[3]))
                            pass

                        else:
                            data = data.get('goodslist', [])
                            # print(data)
                            if data == []:
                                print('goodslist为[], 此处跳过')
                                pass
                            else:
                                miaosha_goods_list = self.get_miaoshao_goods_info_list(data=data)
                                # print(miaosha_goods_list)

                                # 该tab_id, page中现有的所有goods_id的list
                                miaosha_goods_all_goods_id = [i.get('goods_id') for i in miaosha_goods_list]
                                # print(miaosha_goods_all_goods_id)

                                if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                                    '''
                                    表示该tab_id，page中没有了该goods_id
                                    '''
                                    tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                                    print('该商品[goods_id为(%s)]已被下架限时秒杀活动，此处将其删除' % item[0])
                                    pass

                                else:       # 未下架的
                                    for item_1 in miaosha_goods_list:
                                        if item_1.get('goods_id', '') == item[0]:
                                            # # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                                            # juanpi_miaosha = JuanPiParse()
                                            juanpi_miaosha.get_goods_data(goods_id=item[0])
                                            goods_data = juanpi_miaosha.deal_with_data()

                                            if goods_data == {}:    # 返回的data为空则跳过
                                                pass
                                            else:                   # 否则就解析并且插入
                                                goods_data['stock_info'] = item_1.get('stock_info')
                                                goods_data['goods_id'] = item_1.get('goods_id')
                                                # goods_data['username'] = '18698570079'
                                                if item_1.get('stock_info').get('activity_stock') > 0:
                                                    goods_data['price'] = item_1.get('price')  # 秒杀前的原特价
                                                    goods_data['taobao_price'] = item_1.get('taobao_price')  # 秒杀价
                                                else:
                                                    pass
                                                goods_data['sub_title'] = item_1.get('sub_title', '')
                                                goods_data['miaosha_time'] = item_1.get('miaosha_time')
                                                goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item_1.get('miaosha_time'))

                                                # print(goods_data)
                                                juanpi_miaosha.to_update_juanpi_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)

                                                sleep(.2)   # 避免太快
                                        else:
                                            pass
                    if index % 10 == 0:      # 每过几个初始化一次，既能加快速度，又能优化内存
                        # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                        juanpi_miaosha = JuanPiParse()
                        gc.collect()

                    index += 1
                    gc.collect()

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            # sleep(5)
            pass
        gc.collect()

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -259200:     # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        # if diff_time < -172800:     # (原先的时间)48个小时, 只需要跟新过去48小时和对与当前时间的未来14小时的商品信息(20点到第二天10点时间间隔为14小时)
            return 0    # 已过期恢复原价的
        elif diff_time > -172800 and diff_time < 50400:
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
            tmp = {}
            tmp['miaosha_time'] = {
                'miaosha_begin_time': timestamp_to_regulartime(int(item.get('start_time'))),
                'miaosha_end_time': timestamp_to_regulartime(int(item.get('end_time'))),
            }
            stock = item.get('stock', 0)
            # 卷皮商品的goods_id
            tmp['goods_id'] = item.get('goods_id')
            # 限时秒杀库存信息
            tmp['stock_info'] = {
                'activity_stock': int(item.get('stock', 0)*(item.get('rate', 0)/100)),
                'stock': item.get('stock', 0),
            }
            # 原始价格
            tmp['price'] = round(float(item.get('oprice', '0')), 2)
            tmp['taobao_price'] = round(float(item.get('cprice', '0')), 2)
            miaosha_goods_list.append(tmp)

        return miaosha_goods_list

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Juanpi_Miaosha_Real_Time_Update()
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