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

import time
from settings import (
    IS_BACKGROUND_RUNNING,
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import (
    jp_delete_str_3,
    jp_select_str_4,
    jp_delete_str_4,
    jp_update_str_6,
)

from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
    async_get_ms_begin_time_and_miaos_end_time_from_ms_time,
    _handle_goods_shelves_in_auto_goods_table,
)

from fzutils.spider.async_always import *

'''
实时更新卷皮秒杀信息(卷皮频繁地更新商品所在限时秒杀列表)
'''

class JPUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/卷皮/秒杀实时更新/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.tmp_sql_server = None
        self.concurrency = 8
        self.goods_index = 1
        self.delete_sql_str = jp_delete_str_3

    async def _get_pc_headers(self) -> dict:
        headers = await async_get_random_headers(upgrade_insecure_requests=False)
        headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'host': 'm.juanpi.com',
        })

        return headers

    async def _get_db_old_data(self) -> (None, list):
        self.tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.tmp_sql_server._delete_table(sql_str=jp_delete_str_4, params=None)
            await async_sleep(5)
            result = list(self.tmp_sql_server._select_table(sql_str=jp_select_str_4))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_new_jp_obj(self, index):
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.juanpi_miaosha
            except:
                pass
            collect()
            self.juanpi_miaosha = JuanPiParse()

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
        tab_id = item[2]
        page = item[3]
        miaosha_begin_time, miaosha_end_time = await async_get_ms_begin_time_and_miaos_end_time_from_ms_time(
            miaosha_time=miaosha_time,
            logger=self.lg,)
        await self._get_new_jp_obj(index=index)
        self.tmp_sql_server = await _get_new_db_conn(db_obj=self.tmp_sql_server, index=index, logger=self.lg, remainder=30)

        if self.tmp_sql_server.is_connect_success:
            is_recent_time = await self._is_recent_time(miaosha_begin_time)
            if is_recent_time == 0:
                res = _handle_goods_shelves_in_auto_goods_table(
                    goods_id=goods_id,
                    logger=self.lg,
                    update_sql_str=jp_update_str_6,
                    sql_cli=self.tmp_sql_server,)
                self.lg.info('过期的goods_id为({}), 限时秒杀开始时间为({}), 逻辑删除成功!'.format(
                    goods_id,
                    timestamp_to_regulartime(miaosha_begin_time)))
                await async_sleep(.3)
                index += 1
                self.goods_index = index

                return goods_id, res

            elif is_recent_time == 2:
                if datetime_to_timestamp(get_shanghai_time()) > miaosha_end_time:
                    res = _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        logger=self.lg,
                        update_sql_str=jp_update_str_6,
                        sql_cli=self.tmp_sql_server, )
                    self.lg.info('过期的goods_id为({}), 限时秒杀开始时间为({}), 逻辑删除成功!'.format(
                        goods_id,
                        timestamp_to_regulartime(miaosha_begin_time)))
                else:
                    self.lg.info('goods_id: {}, 未来时间跳过更新...'.format(goods_id))
                index += 1
                self.goods_index = index

                return goods_id, res

            else:  # 返回1，表示在待更新区间内
                self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
                tmp_url = 'https://m.juanpi.com/act/timebuy-xrgoodslist?tab_id={0}&page={1}'.format(
                    str(tab_id), str(page),
                )
                # self.lg.info('待爬取的tab_id, page地址为: {}'.format(tmp_url))
                body = Requests.get_url_body(url=tmp_url, headers=await self._get_pc_headers(), ip_pool_type=self.ip_pool_type)
                try:
                    data = json_2_dict(body, default_res={}).get('data', {})
                    assert data != {}, 'data为空dict!'
                    data = data.get('goodslist', [])
                    assert data != [], 'tab_id={0}, page={1}的goodslist为[], 此处跳过'.format(tab_id, page)
                except AssertionError:
                    self.lg.error(msg='遇到错误:', exc_info=True)
                    index += 1
                    self.goods_index = index
                    await async_sleep(.3)

                    return goods_id, res

                miaosha_goods_list = await self._get_miaoshao_goods_info_list(data=data)
                # self.lg.info(str(miaosha_goods_list))
                # 该tab_id, page中现有的所有goods_id的list
                miaosha_goods_all_goods_id = [i.get('goods_id') for i in miaosha_goods_list]
                self.lg.info(str(miaosha_goods_all_goods_id))
                if goods_id not in miaosha_goods_all_goods_id:  # 内部已经下架的
                    if miaosha_goods_all_goods_id != []:        # 测试发现miaosha_goods_all_goods_id不为空，则未下架, 跳过!
                        self.lg.info('该商品[{}]未下架, 此处不进行更新跳过!!'.format(goods_id))
                    else:
                        # 表示该tab_id，page中没有了该goods_id
                        res = _handle_goods_shelves_in_auto_goods_table(
                            goods_id=goods_id,
                            logger=self.lg,
                            update_sql_str=jp_update_str_6,
                            sql_cli=self.tmp_sql_server, )
                        self.lg.info('该商品[goods_id为({})]已被下架限时秒杀活动，此处将其逻辑删除'.format(goods_id))

                    index += 1
                    self.goods_index = index
                    await async_sleep(.3)

                    return goods_id, res

                else:  # 未下架的
                    res = await self._one_update(miaosha_goods_list=miaosha_goods_list, goods_id=goods_id)

        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')

        index += 1
        self.goods_index = index
        await async_sleep(1.2)

        return goods_id, res

    async def _update_db(self) -> None:
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
                self.juanpi_miaosha = JuanPiParse()
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
                del self.juanpi_miaosha
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
        miaosha_goods_list = kwargs.get('miaosha_goods_list')
        goods_id = kwargs.get('goods_id')

        for item_1 in miaosha_goods_list:
            if item_1.get('goods_id', '') == goods_id:
                self.juanpi_miaosha.get_goods_data(goods_id=goods_id)
                goods_data = self.juanpi_miaosha.deal_with_data()
                if goods_data == {}:  # 返回的data为空则跳过
                    break
                else:  # 否则就解析并且插入
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
                    goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                        miaosha_time=item_1.get('miaosha_time'))

                    res = self.juanpi_miaosha.to_update_juanpi_xianshimiaosha_table(
                        data=goods_data,
                        pipeline=self.tmp_sql_server)
                    await async_sleep(.3)  # 避免太快
                    break
            else:
                pass

        return res

    async def _get_miaoshao_goods_info_list(self, data) -> list:
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

    async def _is_recent_time(self, timestamp) -> int:
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

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            del self.loop
        except:
            pass
        collect()

def _fck_run():
    # 遇到: PermissionError: [Errno 13] Permission denied: 'ghostdriver.log'
    # 解决方案: sudo touch /ghostdriver.log && sudo chmod 777 /ghostdriver.log
    _ = JPUpdater()
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