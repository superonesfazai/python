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
import json
from pprint import pprint
import time
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)

from zhe_800_spike import Zhe800Spike

from sql_str_controller import (
    z8_delete_str_3,
    z8_select_str_4,
    z8_delete_str_4,
)

from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
)

from gc import collect
from fzutils.spider.async_always import *

class Z8Updater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/折800/秒杀实时更新/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.tmp_sql_server = None
        self.goods_index = 1
        self.concurrency = 8        # 并发量
        self.delete_sql_str = z8_delete_str_3

    async def _get_db_old_data(self):
        self.tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.tmp_sql_server._delete_table(sql_str=z8_delete_str_4, params=None)
            await async_sleep(1)
            result = list(self.tmp_sql_server._select_table(sql_str=z8_select_str_4))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_miaosha_begin_time(self, miaosha_time) -> int:
        miaosha_begin_time = json_2_dict(miaosha_time).get('miaosha_begin_time')
        miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')))[0:10])

        return miaosha_begin_time

    async def _get_new_z8_obj(self, index):
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.zhe_800_spike
            except:
                pass
            collect()
            self.zhe_800_spike = Zhe800Spike()

    async def _update_is_delete(self, goods_id) -> bool:
        '''
        下架商品逻辑删除
        :param goods_id:
        :return:
        '''
        delete_str = 'update dbo.zhe_800_xianshimiaosha set is_delete = 1 where goods_id=%s'
        res = self.tmp_sql_server._update_table(sql_str=delete_str, params=(goods_id,))
        await async_sleep(.3)

        return res

    async def _update_one_goods_info(self, item, index) -> tuple:
        '''
        更新单个
        :param item:
        :param index:
        :return:
        '''
        res = False
        goods_id = item[0]
        miaosha_time = item[1]
        session_id = item[2]
        miaosha_begin_time = await self._get_miaosha_begin_time(miaosha_time)
        # self.lg.info(str(miaosha_begin_time))
        await self._get_new_z8_obj(index=index)
        self.tmp_sql_server = await _get_new_db_conn(db_obj=self.tmp_sql_server, index=index, logger=self.lg, remainder=30)

        if self.tmp_sql_server.is_connect_success:
            is_recent_time = await self._is_recent_time(miaosha_begin_time)
            if is_recent_time == 0:
                self.tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(goods_id,))
                self.lg.info('过期的goods_id为({0}), 限时秒杀开始时间为({1}), 删除成功!'.format(goods_id, json.loads(item[1]).get('miaosha_begin_time')))
                index += 1
                self.goods_index = index
                res = True
                await async_sleep(.3)

                return goods_id, res

            elif is_recent_time == 2:
                # 可能包括过期的
                self.lg.info('未来时间暂时不更新! {}'.format(timestamp_to_regulartime(miaosha_begin_time)))
                index += 1
                self.goods_index = index

                return goods_id, res

            else:  # 返回1，表示在待更新区间内
                self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
                try:
                    tmp_data = self.zhe_800_spike._get_one_session_id_data(base_session_id=str(session_id))
                except Exception:
                    self.lg.error(msg='遇到错误:', exc_info=True)
                    index += 1
                    self.goods_index = index

                    return goods_id, res

                try:
                    tmp_data = tmp_data.get('data', {}).get('blocks', [])
                    assert tmp_data != [], '该session_id不存在，此处跳过'
                except AssertionError:  # 说明这个sessionid没有数据, 就删除对应这个sessionid的限时秒杀商品
                    self.lg.error(msg='遇到错误:', exc_info=True)
                    res = await self._update_is_delete(goods_id)
                    self.lg.info(
                        msg='该sessionid没有相关key为jsons的数据! 过期的goods_id为({0}), 限时秒杀开始时间为({1}), 删除成功!'.format(
                            goods_id,
                            miaosha_begin_time))
                    index += 1
                    self.goods_index = index
                    await async_sleep(1.2)

                    return goods_id, res

                tmp_data = [item_s.get('deal', {}) for item_s in tmp_data]
                # pprint(tmp_data)
                try:
                    miaosha_goods_list = await self._get_miaoshao_goods_info_list(data=tmp_data)
                    # pprint(miaosha_goods_list)
                except ValueError:
                    await async_sleep(2)
                    index += 1
                    self.goods_index = index

                    return goods_id, res

                # 该session_id中现有的所有zid的list
                miaosha_goods_all_goods_id = [i.get('zid') for i in miaosha_goods_list]
                if goods_id not in miaosha_goods_all_goods_id:  # 内部已经下架的
                    res = await self._update_is_delete(goods_id)
                    self.lg.info('该商品已被官方下架限秒活动! 下架的goods_id为({0}), 逻辑删除成功!'.format(goods_id))
                    index += 1
                    self.goods_index = index

                    return goods_id, res

                else:  # 未下架的
                    res = await self._one_update(miaosha_goods_list=miaosha_goods_list, goods_id=goods_id)

        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')

        index += 1
        self.goods_index = index
        collect()
        await async_sleep(1.5)

        return goods_id, res

    async def _one_update(self, **kwargs) -> bool:
        '''
        未下架的更新
        :return:
        '''
        miaosha_goods_list = kwargs.get('miaosha_goods_list')
        goods_id = kwargs.get('goods_id')

        zhe_800_miaosha = Zhe800Parse()
        res = False
        for item_1 in miaosha_goods_list:
            if item_1.get('zid', '') == goods_id:
                zhe_800_miaosha.get_goods_data(goods_id=goods_id)
                goods_data = zhe_800_miaosha.deal_with_data()
                if goods_data == {}:  # 返回的data为空则跳过
                    break

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
                    goods_data['miaosha_begin_time'], goods_data[
                        'miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                        miaosha_time=item_1.get('miaosha_time'))

                    if goods_data.get('is_delete', 0) == 1:
                        self.lg.info('该商品[{0}]已售罄...'.format(goods_id))

                    # self.lg.info(str(goods_data['stock_info']))
                    # self.lg.info(str(goods_data['miaosha_time']))
                    res = zhe_800_miaosha.to_update_zhe_800_xianshimiaosha_table(
                        data=goods_data,
                        pipeline=self.tmp_sql_server)
                    break
            else:
                pass
        collect()

        return res

    async def _is_recent_time(self, timestamp) -> int:
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

    async def _update_db(self):
        '''
        秒杀数据实时更新
        :return:
        '''
        while True:
            self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                self.goods_index = 1
                tasks_params_list = TasksParamsListObj(tasks_params_list=result, step=self.concurrency)
                self.zhe_800_spike = Zhe800Spike()
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                        # self.lg.info(str(slice_params_list))
                    except AssertionError:  # 全部提取完毕, 正常退出
                        break

                    tasks = []
                    for item in slice_params_list:
                        self.lg.info('创建 task goods_id: {}'.format(item[0]))
                        tasks.append(self.loop.create_task(self._update_one_goods_info(item=item, index=index)))
                        index += 1

                    await _get_async_task_result(tasks=tasks, logger=self.lg)

                self.lg.info('全部数据更新完毕'.center(100, '#'))
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(2.5 * 60)

            try:
                del self.zhe_800_spike
            except:
                pass
            collect()

    async def _get_miaoshao_goods_info_list(self, data) -> list:
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        # pprint(data)
        for item in data:
            if item == {}:
                continue
            # pprint(item)
            tmp = {}
            tmp['miaosha_time'] = {
                'miaosha_begin_time': timestamp_to_regulartime(int(str(item.get('begin_time'))[0:10])),
                'miaosha_end_time': timestamp_to_regulartime(int(str(item.get('end_time'))[0:10])),
            }

            # 折800商品地址
            tmp['zid'] = item.get('zid')
            # 限时秒杀的库存信息
            tmp['stock_info'] = {
                'activity_stock': item.get('activity_stock', 0),  # activity_stock为限时抢的剩余数量
                'stock': item.get('stock', 0),  # stock为限时秒杀的总库存
            }
            # 原始价格
            tmp['price'] = float(item.get('list_price'))
            # 秒杀的价格, float类型
            tmp['taobao_price'] = float(item.get('price'))
            tmp['sub_title'] = item.get('description', '')
            miaosha_goods_list.append(tmp)
            # pprint(miaosha_goods_list)

        return miaosha_goods_list

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            del self.loop
        except:
            pass
        try:
            del self.zhe_800_spike
        except:
            pass
        collect()

def _fck_run():
    _ = Z8Updater()
    loop = get_event_loop()
    loop.run_until_complete(_._update_db())
    try:
        del loop
    except:
        pass

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()