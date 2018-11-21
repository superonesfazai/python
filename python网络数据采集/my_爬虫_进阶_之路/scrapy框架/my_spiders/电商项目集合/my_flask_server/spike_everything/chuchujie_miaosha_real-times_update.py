# coding:utf-8

'''
@author = super_fazai
@File    : chuchujie_miaosha_real-times_update.py
@Time    : 2018/2/25 10:30
@connect : superonesfazai@gmail.com
'''

"""
楚楚街秒杀实时更新脚本
"""

import sys
sys.path.append('..')

from chuchujie_9_9_parse import ChuChuJie_9_9_Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from gc import collect
import json
from pprint import pprint
import time

from settings import (
    IS_BACKGROUND_RUNNING, 
    CHUCHUJIE_SLEEP_TIME,
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import (
    cc_delete_str_1,
    cc_select_str_1,
    cc_delete_str_2,
)
from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
)

from fzutils.spider.async_always import *

class CCUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/楚楚街/秒杀实时更新/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.tmp_sql_server = None
        self.concurrency = 8    # 并发量
        self.goods_index = 1
        self.delete_sql_str = cc_delete_str_1

    async def _get_pc_headers(self):
        return {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'api.chuchujie.com',
            'Referer': 'https://m.chuchujie.com/?module=99',
            'Cache-Control': 'max-age=0',
            'User-Agent': get_random_pc_ua(),
        }

    async def _get_db_old_data(self) -> (list, None):
        self.tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            self.tmp_sql_server._delete_table(sql_str=cc_delete_str_2)
            await async_sleep(1)
            result = list(self.tmp_sql_server._select_table(sql_str=cc_select_str_1))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_miaosha_end_time(self, miaosha_time) -> int:
        miaosha_end_time = json_2_dict(miaosha_time).get('miaosha_end_time')
        miaosha_end_time = int(str(time.mktime(time.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])

        return miaosha_end_time

    async def _get_new_cc_obj(self, index):
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.chuchujie_miaosha
            except:
                pass
            collect()
            self.chuchujie_miaosha = ChuChuJie_9_9_Parse()

    async def _update_one_goods_info(self, item, index):
        '''
        更新单个
        :param item:
        :param index:
        :return:
        '''
        res = False
        goods_id = item[0]
        miaosha_time = item[1]
        gender = item[2]
        page = item[3]
        miaosha_end_time = await self._get_miaosha_end_time(miaosha_time)
        # self.lg.info(str(miaosha_end_time))
        await self._get_new_cc_obj(index=index)
        self.tmp_sql_server = await _get_new_db_conn(db_obj=self.tmp_sql_server, index=index, logger=self.lg, remainder=25)

        if self.tmp_sql_server.is_connect_success:
            is_recent_time = await self._is_recent_time(miaosha_end_time)
            if is_recent_time == 0:
                res = self.tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(goods_id,))
                self.lg.info('过期的goods_id为({}), 限时秒杀结束时间为({}), 删除成功!'.format(goods_id, miaosha_end_time))
                await async_sleep(.3)
                index += 1
                self.goods_index = index

                return goods_id, res

            elif is_recent_time == 2:
                index += 1
                self.goods_index = index

                return goods_id, res

            else:  # 返回1，表示在待更新区间内
                # 释放内存, 在外面声明就会占用很大的, 所以此处优化内存的方法是声明后再删除释放
                self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
                body = await self._get_one_page_goods_info(gender, page)
                if body == '':
                    index += 1
                    self.goods_index = index
                    await async_sleep(.3)

                    return goods_id, res

                json_body = json_2_dict(body, default_res={})
                try:
                    this_page_total_count = json_body.get('data', {}).get('groupList', [])[0].get('totalCount', 0)
                except IndexError:
                    self.lg.error('获取this_page_total_count时出错, 请检查!')
                    this_page_total_count = 0

                item_list = await self._get_item_list(this_page_total_count=this_page_total_count, json_body=json_body)
                if item_list == []:
                    self.lg.info('#### 该gender, page对应得到的item_list为空[]!\n该商品已被下架限时秒杀活动，此处将其删除')
                    res = self.tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0]))
                    self.lg.info('下架的goods_id为({}), 删除成功!'.format(goods_id))
                    await async_sleep(.3)
                    index += 1
                    self.goods_index = index

                    return goods_id, res

                else:
                    res = await self._one_update(goods_id=goods_id, item_list=item_list)

        else:  # 表示返回的data值为空值
            self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
            pass

        index += 1
        self.goods_index = index
        collect()
        await async_sleep(CHUCHUJIE_SLEEP_TIME)

        return goods_id, res

    async def _update_db(self) -> None:
        '''
        秒杀数据更新
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
                self.chuchujie_miaosha = ChuChuJie_9_9_Parse()
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
                del self.chuchujie_miaosha
            except:
                pass
            collect()

    async def _get_item_list(self, **kwargs) -> list:
        '''
        获取对应gender, page的商品list
        :return:
        '''
        this_page_total_count = kwargs.get('this_page_total_count')
        json_body = kwargs.get('json_body')
        tmp_goods_list = json_body.get('data', {}).get('groupList', [])[0].get('dataList', [])

        item_list = [{
            'goods_id': str(item_s.get('chuchuId', '')),
            'sub_title': item_s.get('description', ''),
        } for item_s in tmp_goods_list] if this_page_total_count != 0 else []

        return item_list

    async def _one_update(self, **kwargs):
        '''
        未下架的更新
        :param kwargs:
        :return:
        '''
        res = False
        goods_id = kwargs.get('goods_id')
        item_list = kwargs.get('item_list')

        # miaosha_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in item_list]
        # 由于不会内部提前下架，所以在售卖时间内的全部进行相关更新
        # if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
        #     self.lg.info('该商品已被下架限时秒杀活动，此处将其删除')
        #     tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(goods_id))
        #     self.lg.info('下架的goods_id为({}), 删除成功!'.format(goods_id))
        #     pass
        #
        # else:  # 未下架的
        # 不更新秒杀时间和sub_title, 只更新其他相关数据
        # for item_2 in item_list:
        #     if item_2.get('goods_id', '') == goods_id:
        self.chuchujie_miaosha.get_goods_data(goods_id=goods_id)
        goods_data = self.chuchujie_miaosha.deal_with_data()
        if goods_data == {}:  # 返回的data为空则跳过
            pass
        else:
            goods_data['goods_id'] = str(goods_id)
            # goods_data['sub_title'] = item_2.get('sub_title', '')
            # print(goods_data)
            res = self.chuchujie_miaosha.update_chuchujie_xianshimiaosha_table(
                data=goods_data,
                pipeline=self.tmp_sql_server)

        return res

    async def _get_one_page_goods_info(self, *params) -> str:
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

        body = Requests.get_url_body(url=tmp_url, headers=self.headers, params=data, ip_pool_type=self.ip_pool_type)

        return body

    async def _is_recent_time(self, timestamp) -> int:
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = datetime_to_timestamp(get_shanghai_time())  # 当前的时间戳

        diff_time = time_1 - time_2
        # if diff_time < -86400:  # (为了后台能同步下架)所以设置为 24个小时
        if diff_time < -100000:     # 设置大点避免还在卖的被下掉
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
            del self.chuchujie_miaosha
        except:
            pass
        collect()

def _fck_run():
    _ = CCUpdater()
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
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()