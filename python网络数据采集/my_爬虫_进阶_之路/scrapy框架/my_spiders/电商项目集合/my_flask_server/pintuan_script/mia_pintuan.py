# coding:utf-8

'''
@author = super_fazai
@File    : mia_pintuan.py
@Time    : 2018/1/18 13:24
@connect : superonesfazai@gmail.com
'''

# TODO mia拼团放在本地跑, 服务器上被禁止403!

import sys
sys.path.append('..')

import re
from pprint import pprint
from gc import collect
from time import sleep

from settings import MIA_SPIKE_SLEEP_TIME
from mia_pintuan_parse import MiaPintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from multiplex_code import get_mia_pintuan_one_page_api_goods_info
from settings import (
    IS_BACKGROUND_RUNNING,
    IP_POOL_TYPE,)

from sql_str_controller import (
    mia_select_str_1,
)

from fzutils.linux_utils import daemon_init
from fzutils.exceptions import ResponseBodyIsNullStrException
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time

class MiaPintuan(object):
    def __init__(self):
        self.ip_pool_type = IP_POOL_TYPE

    def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时拼团商品信息
        :return: None
        '''
        goods_list = []
        for page_num in range(1, 4):
            # 0跟1返回一样，所有从1开始遍历
            try:
                one_page_list = get_mia_pintuan_one_page_api_goods_info(page_num=page_num)
                assert one_page_list != [], 'one_page_list不为空list!'
            except ResponseBodyIsNullStrException:
                print('page_num: {} response body is null! pass'.format(page_num))
                continue
            except AssertionError:
                break

            for item in one_page_list:
                goods_list.append(item)

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
        mia = MiaPintuanParse(is_real_times_update_call=True)
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            _ = list(my_pipeline._select_table(sql_str=mia_select_str_1))
            db_goods_id_list = [item[0] for item in _]
            # print(db_goods_id_list)

            for item in goods_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = str(item.get('goods_id', ''))
                    mia.get_goods_data(goods_id=str(goods_id))
                    goods_data = mia.deal_with_data()
                    if goods_data == {}:  # 返回的data为空则跳过
                        pass
                    else:  # 否则就解析并且插入
                        goods_url = goods_data['goods_url']
                        if re.compile(r'://m.miyabaobei.hk/').findall(goods_url) != '':
                            # 地址变了
                            # 原先
                            # goods_url = 'https://www.miyabaobei.hk/item-{}.html'.format(goods_id)
                            # now
                            goods_url = 'https://m.miyabaobei.hk/item-{}.html'.format(goods_id)

                        else:
                            goods_url = 'https://m.mia.com/item-' + str(goods_id) + '.html'

                        goods_data['goods_url'] = goods_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['sub_title'] = item.get('sub_title', '')
                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['pintuan_time'])
                        goods_data['pid'] = item.get('pid')

                        # pprint(goods_data)
                        _r = mia.insert_into_mia_pintuan_table(data=goods_data, pipeline=my_pipeline)
                        if _r:  # 更新
                            if goods_id not in db_goods_id_list:
                                db_goods_id_list.append(goods_id)

                    sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mia
        except:
            pass
        collect()

    def __del__(self):
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        mia_pintuan = MiaPintuan()
        mia_pintuan.get_pintuan_goods_info()
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(5*60)

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