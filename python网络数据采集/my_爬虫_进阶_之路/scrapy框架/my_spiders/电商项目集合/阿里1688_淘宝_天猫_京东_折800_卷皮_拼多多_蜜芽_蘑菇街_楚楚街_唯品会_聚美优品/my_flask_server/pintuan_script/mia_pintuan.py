# coding:utf-8

'''
@author = super_fazai
@File    : mia_pintuan.py
@Time    : 2018/1/18 13:24
@connect : superonesfazai@gmail.com
'''

import json
import re
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from settings import MIA_SPIKE_SLEEP_TIME
from mia_pintuan_parse import MiaPintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import IS_BACKGROUND_RUNNING

import datetime

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class MiaPintuan(object):
    def __init__(self):
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mia.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时拼团商品信息
        :return: None
        '''
        goods_list = []
        for index in range(1, 1000):     # 0跟1返回一样，所有从1开始遍历
            tmp_url = 'https://m.mia.com/instant/groupon/common_list/' + str(index) + '/0/'
            print('正在抓取: ', tmp_url)

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
            # print(body)

            if body == '':
                print('获取到的body为空值! 此处跳过')

            else:
                try:
                    tmp_data = json.loads(body)
                except:
                    tmp_data = {}
                    print('json.loads转换body时出错, 此处跳过!')

                if tmp_data.get('data_list', []) == []:
                    print('得到的data_list为[], 此处跳过!')
                    break

                else:
                    # print(tmp_data)
                    data_list = [{
                        'goods_id': item.get('sku', ''),
                        'sub_title': item.get('intro', ''),
                        'pid': index,
                    } for item in tmp_data.get('data_list', [])]
                    # pprint(data_list)

                    for item in data_list:
                        goods_list.append(item)
                    sleep(.5)

        pprint(goods_list)
        self.deal_with_data(goods_list=goods_list)
        sleep(8)
        return None

    def deal_with_data(self, goods_list):
        '''
        处理并存储相关拼团商品的数据
        :param goods_list:
        :return:
        '''
        mia = MiaPintuanParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            sql_str = r'select goods_id, miaosha_time, pid from dbo.mia_pintuan where site_id=21'
            db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]
            # print(db_goods_id_list)

            for item in goods_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = str(item.get('goods_id', ''))
                    tmp_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'

                    mia.get_goods_data(goods_id=str(goods_id))
                    goods_data = mia.deal_with_data()

                    if goods_data == {}:  # 返回的data为空则跳过
                        pass

                    else:  # 否则就解析并且插入
                        goods_url = goods_data['goods_url']
                        if re.compile(r'://m.miyabaobei.hk/').findall(goods_url) != '':
                            goods_url = 'https://www.miyabaobei.hk/item-' + str(goods_id) + '.html'
                        else:
                            goods_url = 'https://www.mia.com/item-' + str(goods_id) + '.html'
                        goods_data['goods_url'] = goods_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['sub_title'] = item.get('sub_title', '')
                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = self.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=goods_data['pintuan_time'])
                        goods_data['pid'] = item.get('pid')

                        # pprint(goods_data)
                        # print(goods_data)
                        _r = mia.insert_into_mia_pintuan_table(data=goods_data, pipeline=my_pipeline)
                        if _r:  # 更新
                            db_goods_id_list.append(goods_id)
                            db_goods_id_list = list(set(db_goods_id_list))

                    sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mia
        except:
            pass
        gc.collect()

    def get_pintuan_begin_time_and_pintuan_end_time(self, pintuan_time):
        '''
        返回拼团开始和结束时间
        :param pintuan_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = pintuan_time.get('begin_time')
        pintuan_end_time = pintuan_time.get('end_time')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        mia_pintuan = MiaPintuan()
        mia_pintuan.get_pintuan_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(5*60)

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