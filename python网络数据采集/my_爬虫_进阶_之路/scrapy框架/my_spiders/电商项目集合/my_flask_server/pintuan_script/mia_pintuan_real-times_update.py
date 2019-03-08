# coding:utf-8

'''
@author = super_fazai
@File    : mia_pintuan_real-times_update.py
@Time    : 2018/1/23 13:36
@connect : superonesfazai@gmail.com
'''

'''
蜜芽拼团商品实时更新脚本
'''

import sys
sys.path.append('..')

from mia_pintuan_parse import MiaPintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import json
from pprint import pprint
from settings import (
    IS_BACKGROUND_RUNNING, 
    MIA_SPIKE_SLEEP_TIME,
    IP_POOL_TYPE,)

from sql_str_controller import (
    mia_delete_str_2,
    mia_select_str_2,
    mia_update_str_7,
)
from multiplex_code import (
    _handle_goods_shelves_in_auto_goods_table,
    _block_get_new_db_conn,
    _block_print_db_old_data,)

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    string_to_datetime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time
from fzutils.common_utils import json_2_dict

class Mia_Pintuan_Real_Time_Update(object):
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
            'Host': 'm.mia.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            sql_cli._delete_table(sql_str=mia_delete_str_2)
            result = list(sql_cli._select_table(sql_str=mia_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            for item in result:  # 实时更新数据
                goods_id = item[0]
                # 2020-04-12 00:00:00
                pintuan_end_time = json_2_dict(item[1]).get('end_time')
                pintuan_end_time = datetime_to_timestamp(string_to_datetime(pintuan_end_time))
                # print(pintuan_end_time)

                data = {}
                mia_pintuan = MiaPintuanParse()
                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50)
                if sql_cli.is_connect_success:
                    if self.is_recent_time(pintuan_end_time) == 0:
                        _handle_goods_shelves_in_auto_goods_table(
                            goods_id=goods_id,
                            update_sql_str=mia_update_str_7,
                            sql_cli=sql_cli)
                        print('该goods拼团开始时间为({})'.format(json.loads(item[1]).get('begin_time')))
                        sleep(.4)

                    elif self.is_recent_time(pintuan_end_time) == 2:
                        pass

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                        data['goods_id'] = goods_id
                        # print('------>>>| 爬取到的数据为: ', data)
                        tmp_url = 'https://m.mia.com/instant/groupon/common_list/' + str(item[2]) + '/0/'
                        # print(tmp_url)

                        try:
                            body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
                            assert body != '', 'body不为空值!'
                            tmp_data = json_2_dict(json_str=body)
                            assert tmp_data != {}, 'tmp_data不为空dict!'
                        except AssertionError as e:
                            print(e)
                            continue

                        if tmp_data.get('data_list', []) == []:
                            print('得到的data_list为[]!')
                            _handle_goods_shelves_in_auto_goods_table(
                                goods_id=goods_id,
                                update_sql_str=mia_update_str_7,
                                sql_cli=sql_cli)
                            sleep(.4)

                        else:
                            data_list = [{
                                'goods_id': item_2.get('sku', ''),
                                'sub_title': item_2.get('intro', ''),
                            } for item_2 in tmp_data.get('data_list', [])]
                            # pprint(data_list)

                            pintuan_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in data_list]
                            # print(pintuan_goods_all_goods_id)

                            '''
                            蜜芽拼团不对内部下架的进行操作，一律都更新未过期商品 (根据pid来进行更新多次研究发现出现商品还在拼团，误删的情况很普遍)
                            '''
                            if goods_id not in pintuan_goods_all_goods_id:  # 内部已经下架的
                                # 一律更新
                                mia_pintuan.get_goods_data(goods_id=goods_id)
                                goods_data = mia_pintuan.deal_with_data()

                                if goods_data == {}:  # 返回的data为空则跳过
                                    pass
                                else:
                                    goods_data['goods_id'] = str(goods_id)
                                    if goods_data['pintuan_time'] == {}:  # 当没有拼团时间时，就表示已下架拼团(未让其正常更新进数据库, 我把拼团开始结束时间都设置为当前时间)
                                        now_time = get_shanghai_time()
                                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = (now_time, now_time)
                                    else:
                                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['pintuan_time'])

                                    # pprint(goods_data)
                                    # print(goods_data)
                                    mia_pintuan.update_mia_pintuan_table(data=goods_data, pipeline=sql_cli)
                                    sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度

                            else:       # 未下架的
                                for item_2 in data_list:
                                    if item_2.get('goods_id', '') == goods_id:
                                        mia_pintuan.get_goods_data(goods_id=goods_id)
                                        goods_data = mia_pintuan.deal_with_data()

                                        if goods_data == {}:  # 返回的data为空则跳过
                                            continue

                                        goods_data['goods_id'] = str(goods_id)
                                        goods_data['sub_title'] = item_2.get('sub_title', '')
                                        if goods_data['pintuan_time'] == {}:    # 当没有拼团时间时，就表示已下架拼团
                                            now_time = get_shanghai_time()
                                            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = (now_time, now_time)
                                        else:
                                            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['pintuan_time'])

                                        # pprint(goods_data)
                                        # print(goods_data)
                                        mia_pintuan.update_mia_pintuan_table(data=goods_data, pipeline=sql_cli)
                                        sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
                                    else:
                                        pass

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(10 * 60)
        gc.collect()

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
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Mia_Pintuan_Real_Time_Update()
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