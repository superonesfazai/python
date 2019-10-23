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

# TODO mia拼团放在本地跑, 服务器上被禁止403!

import sys
sys.path.append('..')

from mia_pintuan_parse import MiaPintuanParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from gc import collect
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
    _block_print_db_old_data,
    get_mia_pintuan_one_page_api_goods_info,)

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    string_to_datetime,
)
from fzutils.linux_utils import daemon_init
from fzutils.cp_utils import get_miaosha_begin_time_and_miaosha_end_time
from fzutils.common_utils import json_2_dict
from fzutils.exceptions import ResponseBodyIsNullStrException

class MiaPintuanRealTimeUpdate(object):
    def __init__(self):
        self.ip_pool_type = IP_POOL_TYPE
        self.sql_cli = None

    def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        result = self._get_db_old_data()
        if result is None:
            sleep_time = 20
            print('获取db数据失败, 休眠{}s ...'.format(sleep_time))
            sleep(sleep_time)

            return None

        index = 1
        for item in result:  # 实时更新数据
            goods_id = item[0]
            pid = item[2]
            # 2020-04-12 00:00:00
            pintuan_end_time = json_2_dict(item[1]).get('end_time')
            pintuan_end_time = datetime_to_timestamp(string_to_datetime(pintuan_end_time))
            # print(pintuan_end_time)

            data = {}
            self.sql_cli = _block_get_new_db_conn(db_obj=self.sql_cli, index=index, remainder=50)
            if self.sql_cli.is_connect_success:
                is_recent_time = self.is_recent_time(pintuan_end_time)
                if is_recent_time == 0:
                    # 已恢复原价的
                    _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        update_sql_str=mia_update_str_7,
                        sql_cli=self.sql_cli)
                    print('该goods拼团开始时间为({})'.format(json.loads(item[1]).get('begin_time')))
                    sleep(.4)

                elif is_recent_time == 2:
                    # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
                    pass

                else:  # 返回1，表示在待更新区间内
                    print('------>>>| 正在更新的goods_id为({}) | --------->>>@ 索引值为({})'.format(goods_id, index))
                    data['goods_id'] = goods_id
                    try:
                        data_list = get_mia_pintuan_one_page_api_goods_info(page_num=pid)
                    except ResponseBodyIsNullStrException:
                        index += 1
                        sleep(.4)
                        continue

                    # TODO 会导致在售商品被异常下架, 不进行判断, 一律进行更新
                    # try:
                    #     assert data_list != [], 'data_list不为空list!'
                    # except AssertionError as e:
                    #     print(e)
                    #     _handle_goods_shelves_in_auto_goods_table(
                    #         goods_id=goods_id,
                    #         update_sql_str=mia_update_str_7,
                    #         sql_cli=self.sql_cli)
                    #     sleep(.4)
                    #     index += 1
                    #     continue

                    pintuan_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in data_list]
                    # print(pintuan_goods_all_goods_id)

                    '''
                    蜜芽拼团不对内部下架的进行操作，一律都更新未过期商品 (根据pid来进行更新多次研究发现出现商品还在拼团，误删的情况很普遍)
                    '''
                    mia_pt = MiaPintuanParse(is_real_times_update_call=True)
                    if goods_id not in pintuan_goods_all_goods_id:
                        # 内部已经下架的
                        # 一律更新
                        try:
                            goods_data = self._get_mia_pt_one_goods_info(
                                mia_pt_obj=mia_pt,
                                goods_id=goods_id,)
                        except AssertionError:
                            # 返回的data为空则跳过
                            index += 1
                            continue

                        # pprint(goods_data)
                        mia_pt.update_mia_pintuan_table(data=goods_data, pipeline=self.sql_cli)
                        sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度

                    else:
                        # 未下架的
                        for item_2 in data_list:
                            if item_2.get('goods_id', '') == goods_id:
                                sub_title = item_2.get('sub_title', '')
                                try:
                                    goods_data = self._get_mia_pt_one_goods_info(
                                        mia_pt_obj=mia_pt,
                                        goods_id=goods_id,
                                        sub_title=sub_title,)
                                except AssertionError:
                                    # 返回的data为空则跳过
                                    continue

                                # pprint(goods_data)
                                mia_pt.update_mia_pintuan_table(data=goods_data, pipeline=self.sql_cli)
                                sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
                            else:
                                pass

                    try:
                        del mia_pt
                    except:
                        pass

            else:  # 表示返回的data值为空值
                print('数据库连接失败，数据库可能关闭或者维护中')
                pass

            index += 1
            collect()

        print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(10 * 60)
        collect()

    def _get_mia_pt_one_goods_info(self, mia_pt_obj, goods_id, sub_title='') -> dict:
        """
        获取mia单个goods info
        :return:
        """
        mia_pt_obj.get_goods_data(goods_id=goods_id)
        goods_data = mia_pt_obj.deal_with_data()
        assert goods_data != {}, 'goods_data不为空dict'

        goods_data['goods_id'] = str(goods_id)
        goods_data['sub_title'] = sub_title
        if goods_data['pintuan_time'] == {}:  # 当没有拼团时间时，就表示已下架拼团
            now_time = get_shanghai_time()
            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = (now_time, now_time)
        else:
            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                miaosha_time=goods_data['pintuan_time'])

        return goods_data

    def _get_db_old_data(self) -> (list, None):
        """
        获取db待更新data
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.sql_cli._delete_table(sql_str=mia_delete_str_2)
            result = list(self.sql_cli._select_table(sql_str=mia_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')

        _block_print_db_old_data(result=result)

        return result

    def is_recent_time(self, timestamp) -> int:
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
        collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = MiaPintuanRealTimeUpdate()
        tmp.run_forever()
        try:
            del tmp
        except:
            pass
        collect()
        print('一次大更新完毕'.center(30, '-'))

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