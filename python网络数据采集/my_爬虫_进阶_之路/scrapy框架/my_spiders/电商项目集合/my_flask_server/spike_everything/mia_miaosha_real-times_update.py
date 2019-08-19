# coding:utf-8

'''
@author = super_fazai
@File    : mia_miaosha_real-times_update.py
@Time    : 2018/1/17 09:46
@connect : superonesfazai@gmail.com
'''

'''
蜜芽秒杀商品实时更新脚本
'''

import sys
sys.path.append('..')

from mia_parse import MiaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import json
import time
from settings import (
    IS_BACKGROUND_RUNNING, 
    MIA_SPIKE_SLEEP_TIME,
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import (
    mia_delete_str_3,
    mia_select_str_3,
    mia_delete_str_4,
    mia_update_str_6,
)

from multiplex_code import (
    _get_new_db_conn,
    _get_async_task_result,
    _print_db_old_data,
    async_get_ms_begin_time_and_miaos_end_time_from_ms_time,
    _handle_goods_shelves_in_auto_goods_table,
)
from fzutils.spider.async_always import *

class MIUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/蜜芽/秒杀实时更新/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.delete_sql_str = mia_delete_str_3
        self.concurrency = 8    # 并发量
        self.tmp_sql_server = None
        self.goods_index = 1

    async def _get_pc_headers(self) -> dict:
        headers = await async_get_random_headers(
            upgrade_insecure_requests=False,
        )
        headers.update({
            'Host': 'm.mia.com',
        })

        return headers

    async def _get_db_old_data(self):
        self.tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.tmp_sql_server._delete_table(sql_str=mia_delete_str_4)
            await async_sleep(5)
            result = list(self.tmp_sql_server._select_table(sql_str=mia_select_str_3))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_miaosha_end_time(self, miaosha_time):
        miaosha_end_time = json.loads(miaosha_time).get('miaosha_end_time')
        miaosha_end_time = int(str(time.mktime(time.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])

        return miaosha_end_time

    async def _get_new_mia_obj(self, index):
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.mia_miaosha
            except:
                pass
            collect()
            self.mia_miaosha = MiaParse()

    async def _update_one_goods_info(self, item, index) -> tuple:
        '''
        单个更新
        :param item:
        :param index:
        :return:
        '''
        res = False
        goods_id = item[0]
        miaosha_time = item[1]
        pid = item[2]
        miaosha_begin_time, miaosha_end_time = await async_get_ms_begin_time_and_miaos_end_time_from_ms_time(
            miaosha_time=miaosha_time,
            logger=self.lg,)
        await self._get_new_mia_obj(index)
        self.tmp_sql_server = await _get_new_db_conn(
            db_obj=self.tmp_sql_server,
            index=index,
            logger=self.lg,
            remainder=30,)

        if self.tmp_sql_server.is_connect_success:
            is_recent_time = await self._is_recent_time(miaosha_end_time)
            if is_recent_time == 0:
                res = _handle_goods_shelves_in_auto_goods_table(
                    goods_id=goods_id,
                    logger=self.lg,
                    update_sql_str=mia_update_str_6,
                    sql_cli=self.tmp_sql_server,)
                self.lg.info('过期的goods_id为({}), 限时秒杀开始时间为({}), 删除成功!'.format(
                    goods_id,
                    timestamp_to_regulartime(miaosha_begin_time)))
                await async_sleep(.5)
                self.goods_index = index + 1

                return goods_id, res

            elif is_recent_time == 2:
                if datetime_to_timestamp(get_shanghai_time()) > miaosha_end_time:
                    res = _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        logger=self.lg,
                        update_sql_str=mia_update_str_6,
                        sql_cli=self.tmp_sql_server, )
                    self.lg.info('过期的goods_id为({}), 限时秒杀开始时间为({}), 删除成功!'.format(
                        goods_id,
                        timestamp_to_regulartime(miaosha_begin_time)))

                else:
                    pass

                self.goods_index = index + 1

                return goods_id, res

            else:  # 返回1，表示在待更新区间内
                self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
                tmp_url = 'https://m.mia.com/instant/seckill/seckillPromotionItem/' + str(pid)
                body = Requests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True, ip_pool_type=self.ip_pool_type)
                # print(body)
                body = '' if body == '' or body == '[]' else body
                try:
                    tmp_data = json_2_dict(
                        json_str=body,
                        default_res={},
                        logger=self.lg,)
                    assert tmp_data != {}, 'tmp_data为空dict!'
                except AssertionError:
                    self.lg.error('遇到错误:', exc_info=True)
                    self.goods_index = index + 1
                    await async_sleep(.3)

                    return goods_id, res

                item_list = tmp_data.get('item_list', [])
                # 该pid中现有的所有goods_id的list
                miaosha_goods_all_goods_id = [item_1.get('item_id', '') for item_1 in item_list]
                # self.lg.info(str(miaosha_goods_all_goods_id))
                if goods_id not in miaosha_goods_all_goods_id:  # 内部已经下架的
                    self.lg.info('该商品已被下架限时秒杀活动，此处将其删除')
                    res = _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        logger=self.lg,
                        update_sql_str=mia_update_str_6,
                        sql_cli=self.tmp_sql_server, )
                    self.lg.info('下架的goods_id为({}), 删除成功!'.format(goods_id))
                    self.goods_index = index + 1
                    await async_sleep(.3)

                    return goods_id, res

                else:  # 未下架的
                    res = await self._one_update(
                        item_list=item_list,
                        goods_id=goods_id,
                        tmp_data=tmp_data,)

        else:  # 表示返回的data值为空值
            self.lg.info('数据库连接失败，数据库可能关闭或者维护中')

        await async_sleep(MIA_SPIKE_SLEEP_TIME)  # 放慢速度
        self.goods_index = index + 1
        collect()

        return goods_id, res

    async def _update_db(self) -> None:
        '''
        秒杀实时更新
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
                self.mia_miaosha = MiaParse()
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
                del self.mia_miaosha
            except:
                pass
            collect()

    async def _one_update(self, **kwargs) -> bool:
        '''
        未下架的更新
        :param kwargs:
        :return:
        '''
        res = False
        item_list = kwargs.get('item_list')
        goods_id = kwargs.get('goods_id')
        tmp_data = kwargs.get('tmp_data')

        begin_time, end_time = await self._get_begin_time_and_end_time(tmp_data)
        for item_2 in item_list:
            if item_2.get('item_id', '') == goods_id:
                self.mia_miaosha.get_goods_data(goods_id=goods_id)
                goods_data = self.mia_miaosha.deal_with_data()
                if goods_data == {}:  # 返回的data为空则跳过
                    pass
                else:
                    goods_data['goods_id'] = str(goods_id)
                    goods_data['price'] = item_2.get('active_price')
                    goods_data['taobao_price'] = item_2.get('active_price')
                    goods_data['sub_title'] = item_2.get('short_info', '')
                    goods_data['miaosha_time'] = {
                        'miaosha_begin_time': timestamp_to_regulartime(begin_time),
                        'miaosha_end_time': timestamp_to_regulartime(end_time),
                    }
                    goods_data['miaosha_begin_time'], goods_data[
                        'miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                        miaosha_time=goods_data['miaosha_time'])

                    res = self.mia_miaosha.update_mia_xianshimiaosha_table(
                        data=goods_data,
                        pipeline=self.tmp_sql_server)
                    break
            else:
                pass

        return res

    async def _get_begin_time_and_end_time(self, tmp_data) -> tuple:
        begin_time = tmp_data.get('p_info', {}).get('start_time', '')
        end_time = tmp_data.get('p_info', {}).get('end_time', '')
        # 把str字符串类型转换为时间戳的形式
        begin_time = int(time.mktime(time.strptime(begin_time, '%Y/%m/%d %H:%M:%S')))
        end_time = int(time.mktime(time.strptime(end_time, '%Y/%m/%d %H:%M:%S')))

        return begin_time, end_time

    async def _is_recent_time(self, timestamp) -> int:
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = datetime_to_timestamp(get_shanghai_time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -86400:     # (为了后台能同步下架)所以设置为 24个小时
        # if diff_time < 0:     # (原先的时间)结束时间 与当前时间差 <= 0
            return 0    # 已过期恢复原价的
        elif diff_time > 0:
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:           # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
            return 2

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
            del self.mia_miaosha
        except:
            pass
        collect()

def _fck_run():
    _ = MIUpdater()
    loop = get_event_loop()
    loop.run_until_complete(_._update_db())
    try:
        del loop
    except:
        pass

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()