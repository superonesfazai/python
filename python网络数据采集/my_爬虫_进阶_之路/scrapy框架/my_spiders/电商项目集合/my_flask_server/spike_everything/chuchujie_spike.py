# coding:utf-8

'''
@author = super_fazai
@File    : chuchujie_spike.py
@Time    : 2018/2/24 14:32
@connect : superonesfazai@gmail.com
'''

"""
楚楚街9块9限时秒杀，商品信息抓取
"""

from random import randint
import json
import re
import time
from pprint import pprint
import gc
from time import sleep
import datetime
from decimal import Decimal
from scrapy.selector import Selector

import sys
sys.path.append('..')

from chuchujie_9_9_parse import ChuChuJie_9_9_Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    IS_BACKGROUND_RUNNING,
    CHUCHUJIE_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,
)

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs

class ChuChuJie_9_9_Spike(object):
    def __init__(self):
        self._set_headers()

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

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        all_goods_list = []
        for gender in ['0', '1']:   # 男，女
            for page in range(0, 100):  # page控制放回数据为哪一页
                print('正在抓取的page为: ', page)

                body = self.get_one_page_goods_info(gender, page)

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

                # print(this_page_total_count)
                if this_page_total_count == 0:
                    print('### 该性别的全部限时商品信息获取完毕 ###')
                    break

                tmp_goods_list = json_body.get('data', {}).get('groupList', [])[0].get('dataList', [])
                for item in tmp_goods_list:
                    item['gender'] = gender
                    item['page'] = page

                for item in tmp_goods_list:
                    if item.get('id', 0) not in [item_1.get('id', 0) for item_1 in all_goods_list]:
                        all_goods_list.append(item)

                sleep(.4)

        all_goods_list = [{
            'goods_id': str(item.get('chuchuId', '')),
            'sub_title': item.get('description', ''),
            'gender': item.get('gender', '0'),
            'page': item.get('page')
        } for item in all_goods_list]
        print(all_goods_list)
        print('本次抓取共有限时商品个数为: ', len(all_goods_list))

        self.deal_with_data(all_goods_list)

        return None

    def deal_with_data(self, *params):
        '''
        处理并存储相关秒杀商品数据
        :param params: 相关参数
        :return:
        '''
        item_list = params[0]
        chuchujie = ChuChuJie_9_9_Parse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            sql_str = 'select goods_id, miaosha_time, gender, page, goods_url from dbo.chuchujie_xianshimiaosha where site_id=24'
            db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]
            # print(db_goods_id_list)

            # my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)
            # index = 1
            for item in item_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = item.get('goods_id', '')
                    tmp_url = 'https://m.chuchujie.com/details/detail.html?id=' + str(goods_id)
                    chuchujie.get_goods_data(goods_id=goods_id)
                    goods_data = chuchujie.deal_with_data()

                    if goods_data == {}:  # 返回的data为空则跳过
                        pass

                    elif goods_data.get('is_delete', 0) == 1:   # is_delete=1(即库存为0)则跳过
                        print('------>>>| 该商品库存为0，已被抢光!')
                        pass

                    else:   # 否则就解析并且插入
                        my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

                        # 获取剩余时间
                        tmp_body = my_phantomjs.use_phantomjs_to_get_url_body(
                            url=tmp_url,
                            css_selector='p#activityTime span'
                        )
                        # print(tmp_body)

                        try: del my_phantomjs
                        except: pass
                        gc.collect()

                        if tmp_body == '':  # 获取手机版的页面完整html失败
                            sleep(.4)
                            pass

                        else:
                            # p#activityTime span
                            _t = Selector(text=tmp_body).css('p#activityTime span::text').extract_first()
                            _t = re.compile(r'剩余').sub('', _t)
                            # print(_t)
                            if _t == '' or _t is None:
                                print('获取到的_t为空值, 严重错误! 请检查!')

                            miaosha_end_time = self.get_miaosha_end_time(_t)

                            goods_data['goods_url'] = tmp_url
                            goods_data['goods_id'] = str(goods_id)
                            goods_data['sub_title'] = item.get('sub_title', '')
                            goods_data['miaosha_time'] = {
                                'miaosha_begin_time': timestamp_to_regulartime(int(time.time())),
                                'miaosha_end_time': timestamp_to_regulartime(int(miaosha_end_time)),
                            }
                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                            goods_data['gender'] = str(item.get('gender', '0'))
                            goods_data['page'] = item.get('page')

                            # pprint(goods_data)
                            # print(goods_data)
                            chuchujie.insert_into_chuchujie_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                            # sleep(CHUCHUJIE_SLEEP_TIME)  # 放慢速度   由于初始化用了phantomjs时间久，于是就不睡眠

                        # index += 1

        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del chuchujie
        except:
            pass
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

    def get_miaosha_end_time(self, _t):
        '''
        获取到秒杀结束时间点
        :param _t: 剩余时间字符串
        :return: 结束的时间戳 int
        '''
        number_list = re.compile(r'(\d+)').findall(_t)
        if re.compile(r'天').findall(_t) != []:  # 有天
            # eg: 2天17小时4分钟
            day = int(number_list[0]) * 24 * 60 * 60
            hour = int(number_list[1]) * 60 * 60
            min = int(number_list[2]) * 60

        else:   # 无天
            if re.compile(r'小时').findall(_t) != []:
                # eg: 16小时8分钟
                day = 0
                hour = int(number_list[0]) * 60 * 60
                min = int(number_list[1]) * 60

            else:   # 无小时, 即只有分钟!
                # eg: 7分钟
                day = 0
                hour = 0
                min = int(number_list[0]) * 60

        miaosha_end_time = int(time.time()) + day + hour + min

        return miaosha_end_time

    def get_miaosha_begin_time_and_miaosha_end_time(self, miaosha_time):
        '''
        返回秒杀开始和结束时间
        :param miaosha_time:
        :return: tuple  miaosha_begin_time, miaosha_end_time
        '''
        miaosha_begin_time = miaosha_time.get('miaosha_begin_time')
        miaosha_end_time = miaosha_time.get('miaosha_end_time')
        # 将字符串转换为datetime类型
        miaosha_begin_time = datetime.datetime.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')
        miaosha_end_time = datetime.datetime.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')

        return miaosha_begin_time, miaosha_end_time

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        chuchujie_spike = ChuChuJie_9_9_Spike()
        chuchujie_spike.get_spike_hour_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*2)

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