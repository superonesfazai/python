# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_pintuan.py
@Time    : 2017/12/18 17:09
@connect : superonesfazai@gmail.com
'''

# TODO 折800拼团放在本地跑, 服务器上代理缘故404!

import sys
sys.path.append('..')

from settings import (
    IS_BACKGROUND_RUNNING,
    ZHE_800_PINTUAN_SLEEP_TIME,
    IP_POOL_TYPE,)
from zhe_800_pintuan_parse import Zhe800PintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from sql_str_controller import z8_select_str_1
from fzutils.spider.async_always import *

class Zhe800Pintuan(object):
    def __init__(self):
        self._set_headers()
        self.ip_pool_type = IP_POOL_TYPE

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'pina.m.zhe800.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url, 得到近期所有的限时拼团商品信息
        :return:
        '''
        zid_list = []
        for page in range(0, 100):
            tmp_url = 'https://pina.m.zhe800.com/nnc/list/deals.json?page={0}&size=500'.format(str(page))
            print('正在抓取的页面地址为: ', tmp_url)

            tmp_body = Requests.get_url_body(
                url=tmp_url,
                headers=self.headers,
                high_conceal=True,
                ip_pool_type=self.ip_pool_type,
                proxy_type=PROXY_TYPE_HTTPS,
                num_retries=3,)

            tmp_data = json_2_dict(
                json_str=tmp_body,
                default_res={}).get('objects', [])
            # print(tmp_data)

            if tmp_data == []:
                print('该tmp_url得到的object为空list, 此处跳过!')
                break

            tmp_zid_list = [(item.get('product', {}).get('zid', ''), page) for item in tmp_data]
            # print(tmp_zid_list)

            for item in tmp_zid_list:
                if item != '':
                    zid_list.append(item)

        zid_list = list(set(zid_list))
        print('该zid_list的总个数为: ', len(zid_list))
        print(zid_list)

        return zid_list

    def _deal_with_data(self):
        '''
        处理并存储抓取到的拼团商品的数据
        :return:
        '''
        zid_list = self._get_pintuan_goods_info()

        zhe_800_pintuan = Zhe800PintuanParse(is_real_times_update_call=True)
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        if my_pipeline.is_connect_success:
            _ = list(my_pipeline._select_table(sql_str=z8_select_str_1))
            db_goods_id_list = [item[0] for item in _]
            for item in zid_list:
                item_goods_id = item[0]
                if item_goods_id in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    continue

                tmp_url = 'https://pina.m.zhe800.com/detail/detail.html?zid=' + str(item_goods_id)
                goods_id = zhe_800_pintuan.get_goods_id_from_url(tmp_url)

                zhe_800_pintuan.get_goods_data(goods_id=goods_id)
                goods_data = zhe_800_pintuan.deal_with_data()

                if goods_data == {}:  # 返回的data为空则跳过
                    pass
                else:  # 否则就解析并且插入
                    goods_data['goods_id'] = str(item_goods_id)
                    goods_data['spider_url'] = tmp_url
                    goods_data['username'] = '18698570079'
                    goods_data['page'] = str(item[1])
                    goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                        miaosha_time=goods_data.get('schedule', [])[0])

                    # print(goods_data)
                    _r = zhe_800_pintuan.insert_into_zhe_800_pintuan_table(
                        data=goods_data,
                        pipeline=my_pipeline)
                    if _r:
                        # 插入就更新
                        db_goods_id_list.append(item_goods_id)
                        db_goods_id_list = list(set(db_goods_id_list))

                sleep(ZHE_800_PINTUAN_SLEEP_TIME)
                collect()

        else:
            pass
        try:
            del zhe_800_pintuan
        except:
            pass
        collect()

        return None

    def __del__(self):
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        zhe_800_pintuan = Zhe800Pintuan()
        zhe_800_pintuan._deal_with_data()
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

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