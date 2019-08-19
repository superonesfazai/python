# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_miaosha_real-times_update.py
@Time    : 2018/3/18 09:42
@connect : superonesfazai@gmail.com
'''

"""
聚美优品每日10点上新商品数据实时更新
"""

import sys
sys.path.append('..')

from jumeiyoupin_parse import JuMeiYouPinParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import (
    IS_BACKGROUND_RUNNING,
    JUMEIYOUPIN_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)

from sql_str_controller import (
    jm_delete_str_1,
    jm_select_str_1,
    jm_delete_str_2,
    jm_update_str_4,)

from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
    _handle_goods_shelves_in_auto_goods_table,
    async_get_ms_begin_time_and_miaos_end_time_from_ms_time,
)

from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

class JMYPUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/聚美优品/秒杀实时更新/',
            ip_pool_type=IP_POOL_TYPE,)
        self.sql_cli = None
        self.delete_sql_str = jm_delete_str_1
        self.goods_index = 1
        self.concurrency = 10   # 并发量

    async def _get_pc_headers(self):
        headers = await async_get_random_headers(
            upgrade_insecure_requests=False,
        )
        headers.update({
            'accept': 'application/json,text/javascript,text/plain,*/*;q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'h5.jumei.com',
            'referer': 'https://h5.jumei.com/',
            'X-Requested-With': 'XMLHttpRequest',
        })

        return headers

    async def _get_db_old_data(self) -> (list, None):
        '''
        待更新数据
        :return:
        '''
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.sql_cli._delete_table(sql_str=jm_delete_str_2)
            await async_sleep(5)
            result = list(self.sql_cli._select_table(sql_str=jm_select_str_1))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_cookies(self) -> str:
        '''
        获取请求需要的cookies
        :return:
        '''
        # 获取cookies
        my_phantomjs = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, ip_pool_type=self.ip_pool_type)
        cookies = my_phantomjs.get_url_cookies_from_phantomjs_session(url='https://h5.jumei.com/')
        try:
            del my_phantomjs
        except:
            pass
        if cookies == '':
            self.lg.error('!!! 获取cookies失败 !!!')

        self.lg.info('获取cookies成功!')

        return cookies

    async def _get_new_jumei_obj(self, index):
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.jumeiyoupin_miaosha
            except:
                pass
            collect()
            self.jumeiyoupin_miaosha = JuMeiYouPinParse()

    async def _get_one_page_all_goods_list(self, *params) -> (list, str):
        '''
        得到一个页面地址的所有商品list
        :return: str | list 类型
        '''
        page = params[0]
        all_goods_list = []
        tmp_url = 'https://h5.jumei.com/index/ajaxDealactList?card_id=4057&page={0}&platform=wap&type=formal&page_key=1521336720'.format(str(page))
        # print('正在抓取的page为:', page, ', 接口地址为: ', tmp_url)
        json_body = json_2_dict(Requests.get_url_body(url=tmp_url, headers=self.headers, ip_pool_type=self.ip_pool_type), default_res={}, logger=self.lg)
        if json_body == {}:
            return '网络错误!'

        this_page_item_list = json_body.get('item_list', [])
        if this_page_item_list == []:
            return []

        for item in this_page_item_list:
            if item.get('item_id', '') not in [item_1.get('item_id', '') for item_1 in all_goods_list]:
                item['page'] = page
                all_goods_list.append(item)

        all_goods_list = [{
            'goods_id': str(item.get('item_id', '')),
            'type': item.get('type', ''),
            'page': item.get('page')
        } for item in all_goods_list if item.get('item_id') is not None]

        return all_goods_list

    async def _update_one_goods_info(self, item, index):
        '''
        更新单个
        :return:
        '''
        res = False
        goods_id = item[0]
        miaosha_time = item[1]
        page = item[2]
        goods_url = item[3]
        miaosha_begin_time, miaosha_end_time = await async_get_ms_begin_time_and_miaos_end_time_from_ms_time(
            miaosha_time=miaosha_time,
            logger=self.lg,)
        await self._get_new_jumei_obj(index=index)
        self.sql_cli = await _get_new_db_conn(
            db_obj=self.sql_cli,
            index=index,
            logger=self.lg,)

        if self.sql_cli.is_connect_success:
            is_recent_time_res = await self._is_recent_time(miaosha_end_time)
            if is_recent_time_res == 0:
                res = _handle_goods_shelves_in_auto_goods_table(
                    goods_id=goods_id,
                    logger=self.lg,
                    update_sql_str=jm_update_str_4,
                    sql_cli=self.sql_cli, )
                self.lg.info('过期的goods_id为({}), 限时秒杀结束时间为({}), 逻辑删除成功!'.format(
                    goods_id, 
                    timestamp_to_regulartime(miaosha_end_time)))
                await async_sleep(.3)

            elif is_recent_time_res == 2:
                if datetime_to_timestamp(get_shanghai_time()) > miaosha_end_time:
                    res = _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        logger=self.lg,
                        update_sql_str=jm_update_str_4,
                        sql_cli=self.sql_cli, )
                    self.lg.info('过期的goods_id为({}), 限时秒杀结束时间为({}), 逻辑删除成功!'.format(
                        goods_id,
                        timestamp_to_regulartime(miaosha_end_time)))
                    
                else:
                    pass

            else:  # 返回1，表示在待更新区间内
                self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
                this_page_all_goods_list = await self._get_one_page_all_goods_list(page)
                if isinstance(this_page_all_goods_list, str):
                    self.lg.error('网络错误!先跳过')
                    await async_sleep(1.5)
                    return res

                elif this_page_all_goods_list == []:
                    res = _handle_goods_shelves_in_auto_goods_table(
                        goods_id=goods_id,
                        logger=self.lg,
                        update_sql_str=jm_update_str_4,
                        sql_cli=self.sql_cli, )
                    self.lg.error('#### 该page对应得到的this_page_all_goods_list为空[]!')
                    self.lg.error('** 该商品已被下架限时秒杀活动, 此处将其逻辑删除, goods_id:{}'.format(goods_id))
                    await async_sleep(.3)

                else:
                    """
                    由于不会内部提前下架，所以在售卖时间内的全部进行相关更新
                    """
                    # miaosha_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in this_page_all_goods_list]
                    #
                    # if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                    #     self.lg.info('该商品已被下架限时秒杀活动，此处将其删除')
                    #     res = _handle_goods_shelves_in_auto_goods_table(
                    #         goods_id=goods_id,
                    #         logger=self.lg,
                    #         update_sql_str=jm_update_str_4,
                    #         sql_cli=self.sql_cli, )
                    #     self.lg.info('下架的goods_id为(%s)' % item[0], ', 删除成功!')
                    #     pass

                    # else:  # 未下架的
                    tmp_r = self.jumeiyoupin_miaosha.get_goods_id_from_url(goods_url)
                    self.jumeiyoupin_miaosha.get_goods_data(goods_id=tmp_r)
                    goods_data = self.jumeiyoupin_miaosha.deal_with_data()
                    if goods_data == {}:  # 返回的data为空则跳过
                        pass
                    else:
                        goods_data['goods_id'] = goods_id
                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': goods_data['schedule'].get('begin_time', ''),
                            'miaosha_end_time': goods_data['schedule'].get('end_time', ''),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(
                            miaosha_time=goods_data['miaosha_time'])
                        res = self.jumeiyoupin_miaosha.update_jumeiyoupin_xianshimiaosha_table(data=goods_data, pipeline=self.sql_cli)

        else:  # 表示返回的data值为空值
            self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
            pass

        index += 1
        self.goods_index = index
        collect()
        await async_sleep(JUMEIYOUPIN_SLEEP_TIME)

        return [goods_id, res]

    async def _update_db(self):
        '''
        数据更新
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
                cookies = await self._get_cookies()
                self.headers = await self._get_pc_headers()
                self.headers.update({
                    'Cookie': cookies,
                })
                self.jumeiyoupin_miaosha = JuMeiYouPinParse()
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
                await async_sleep(10)
            try:
                del self.jumeiyoupin_miaosha
            except:
                pass
            collect()

    async def _is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(datetime_to_timestamp(get_shanghai_time()))

        diff_time = time_1 - time_2
        if diff_time < -86400:      # (为了后台能同步下架)所以设置为 24个小时
            # if diff_time < 0:     # (原先的时间)结束时间 与当前时间差 <= 0
            return 0                # 已过期恢复原价的
        elif diff_time > 0:
            return 1                # 表示是昨天跟今天的也就是待更新的
        else:                       # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
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
            del self.jumeiyoupin_miaosha
        except:
            pass
        collect()

def _fck_run():
    _ = JMYPUpdater()
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