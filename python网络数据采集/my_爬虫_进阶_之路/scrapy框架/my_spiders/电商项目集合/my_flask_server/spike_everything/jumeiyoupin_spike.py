# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_spike.py
@Time    : 2018/3/18 09:42
@connect : superonesfazai@gmail.com
'''

"""
聚美优品每日10点上新限时秒杀，商品信息抓取
"""

import json
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from jumeiyoupin_parse import JuMeiYouPinParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import (
    IS_BACKGROUND_RUNNING,
    JUMEIYOUPIN_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,
)

from sql_str_controller import jm_select_str_2

from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

class JuMeiYouPinSpike(object):
    def __init__(self):
        self._set_headers()
        self.ip_pool_type = IP_POOL_TYPE

    def _set_headers(self):
        self.headers = {
            'Accept': 'application/json,text/javascript,text/plain,*/*;q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'h5.jumei.com',
            'Referer': 'https://h5.jumei.com/',
            'Cache-Control': 'max-age=0',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        all_goods_list = []
        self.my_phantomjs = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, ip_pool_type=self.ip_pool_type)
        cookies = self.my_phantomjs.get_url_cookies_from_phantomjs_session(url='https://h5.jumei.com/')
        try: del self.my_phantomjs
        except: pass
        if cookies == '':
            print('!!! 获取cookies失败 !!!')
            return False

        print('获取cookies成功!')
        self.headers.update(Cookie=cookies)

        print('开始抓取在售商品...')
        for page in range(1, 50):   # 1, 开始
            tmp_url = 'https://h5.jumei.com/index/ajaxDealactList?card_id=4057&page={0}&platform=wap&type=formal&page_key=1521336720'.format(str(page))
            print('正在抓取的page为:', page, ', 接口地址为: ', tmp_url)
            json_body = json_2_dict(Requests.get_url_body(url=tmp_url, headers=self.headers, ip_pool_type=self.ip_pool_type), default_res={})
            # print(json_body)
            this_page_item_list = json_body.get('item_list', [])
            if this_page_item_list == []:
                print('@@@@@@ 所有接口数据抓取完毕 !')
                break

            for item in this_page_item_list:
                if item.get('item_id', '') not in [item_1.get('item_id', '') for item_1 in all_goods_list]:
                    item['page'] = page
                    all_goods_list.append(item)

            sleep(.5)

        print('开始抓取预售商品...')
        for page in range(1, 50):   # 1, 开始
            tmp_url = 'https://h5.jumei.com/index/ajaxDealactList?card_id=4057&page={0}&platform=wap&type=pre&page_key=1521858480'.format(str(page))
            print('正在抓取的page为:', page, ', 接口地址为: ', tmp_url)
            json_body = json_2_dict(Requests.get_url_body(url=tmp_url, headers=self.headers, ip_pool_type=self.ip_pool_type), default_res={})
            # print(json_body)
            this_page_item_list = json_body.get('item_list', [])
            if this_page_item_list == []:
                print('@@@@@@ 所有接口数据抓取完毕 !')
                break

            for item in this_page_item_list:
                if item.get('item_id', '') not in [item_1.get('item_id', '') for item_1 in all_goods_list]:
                    item['page'] = page
                    all_goods_list.append(item)

            sleep(.5)

        all_goods_list = [{
            'goods_id': str(item.get('item_id', '')),
            'type': item.get('type', ''),
            'page': item.get('page')
        } for item in all_goods_list if item.get('item_id') is not None]
        print(all_goods_list)
        print('本次抓取到共有限时商品个数为: ', all_goods_list.__len__())

        self.deal_with_data(all_goods_list)

        return True

    def deal_with_data(self, *params):
        '''
        处理并存储相关秒杀商品数据
        :param params: 相关参数
        :return:
        '''
        item_list = params[0]
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            _ = list(my_pipeline._select_table(sql_str=jm_select_str_2))
            db_goods_id_list = [item[0] for item in _]
            # print(db_goods_id_list)

            for item in item_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass
                else:
                    jumei = JuMeiYouPinParse()
                    goods_id = item.get('goods_id', '')
                    type = item.get('type', '')
                    tmp_url = 'https://h5.jumei.com/product/detail?item_id={0}&type={1}'.format(goods_id, type)
                    jumei.get_goods_data(goods_id=[goods_id, type])
                    goods_data = jumei.deal_with_data()
                    if goods_data == {}:
                        pass

                    elif goods_data.get('is_delete', 0) == 1:
                        print('------>>>| 该商品库存为0，已被抢光!')
                        pass

                    else:   # 否则就解析并且插入
                        goods_data['goods_url'] = tmp_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': goods_data['schedule'].get('begin_time', ''),
                            'miaosha_end_time': goods_data['schedule'].get('end_time', ''),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                        goods_data['page'] = item.get('page')

                        # pprint(goods_data)
                        res = jumei.insert_into_jumeiyoupin_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        if res:
                            if goods_id not in db_goods_id_list:
                                db_goods_id_list.append(goods_id)

                        sleep(JUMEIYOUPIN_SLEEP_TIME)  # 放慢速度   由于初始化用了phantomjs时间久，于是就不睡眠

                    try: del jumei
                    except: pass

        else:
            print('数据库连接失败，此处跳过!')
            pass

        gc.collect()

    def __del__(self):
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        jumeiyoupin_spike = JuMeiYouPinSpike()
        jumeiyoupin_spike.get_spike_hour_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*4)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()