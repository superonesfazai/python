# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_pintuan_real-times_update.py
@Time    : 2018/3/30 09:34
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from jumeiyoupin_pintuan_parse import JuMeiYouPinPinTuanParse
from jumeiyoupin_pintuan import JuMeiYouPinPinTuan
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
import json
import time
from logging import INFO, ERROR
from settings import (
    IS_BACKGROUND_RUNNING,
    JUMEIYOUPIN_SLEEP_TIME,
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)
from sql_str_controller import (
    jm_select_str_3,
    jm_delete_str_3,
    jm_update_str_5,)
from multiplex_code import (
    _print_db_old_data,
    _get_new_db_conn,)

from fzutils.log_utils import set_logger
from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.spider.async_always import *

class JuMeiYouPinRealTimesUpdate(object):
    def __init__(self):
        self._set_headers()
        self._set_logger()
        self.msg = ''
        self.api_all_goods_id = {}      # 预存储每个tab, index的item_list
        self.ip_pool_type = IP_POOL_TYPE

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 's.h5.jumei.com',
            'Referer': 'http://s.h5.jumei.com/yiqituan/list',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
            'X-Requested-With': 'XMLHttpRequest',
        }

    def _set_logger(self):
        self.lg = set_logger(
            logger_name=get_uuid1(),
            log_file_name=MY_SPIDER_LOGS_PATH + '/聚美优品/拼团/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR)

    async def run_forever(self):
        '''
        实时更新数据
        :return:
        '''
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            sql_cli._delete_table(sql_str=jm_delete_str_3,)
            await async_sleep(5)
            result = sql_cli._select_table(sql_str=jm_select_str_3, logger=self.lg)
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            await _print_db_old_data(result=result, logger=self.lg)
            index = 1
            for item in result:
                pintuan_end_time = json.loads(item[1]).get('end_time')
                pintuan_end_time = int(str(time.mktime(time.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                data = {}
                sql_cli = await _get_new_db_conn(
                    db_obj=sql_cli, 
                    index=index, 
                    logger=self.lg, 
                    remainder=50)
                if sql_cli.is_connect_success:
                    time_number = await self.is_recent_time(pintuan_end_time)
                    if time_number == 0:
                        await sql_cli._update_table_3(sql_str=jm_update_str_5, params=(str(get_shanghai_time()), item[0]), logger=self.lg)
                        await async_sleep(.5)
                        self.msg = '过期的goods_id为(%s)' % item[0] + ', 拼团结束时间为(%s), 删除成功!' % str(json.loads(item[1]).get('begin_time'))
                        self.lg.info(self.msg)

                    elif time_number == 2:
                        pass  # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        self.msg = '------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (item[0], str(index))
                        self.lg.info(self.msg)
                        data['goods_id'] = item[0]
                        jumeiyoupin_2 = JuMeiYouPinPinTuan(logger=self.lg)

                        _ = item[2] + '-' + str(item[3])    # 格式: 'coutuan_baby-1'
                        item_list = self.api_all_goods_id.get(_, [])    # 用于判断tab, index已在self.api_all_goods_id中

                        if item_list == []:
                            driver = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, ip_pool_type=self.ip_pool_type)
                            item_list = await jumeiyoupin_2.get_one_page_goods_list(driver=driver, tab=item[2], index=item[3])
                            try: del driver
                            except: pass

                        if item_list == []:
                            self.lg.info('获取到的body为空str, 网络原因, 此处先跳过!')
                            pass
                        else:
                            if self.api_all_goods_id.get(_) is None:
                                self.api_all_goods_id[_] = item_list

                            pintuan_goods_all_goods_id = [item_1.get('goods_id', '') for item_1 in item_list]

                            jumeiyoupin_pintuan = JuMeiYouPinPinTuanParse(logger=self.lg)
                            # 内部已经下架的(测试发现官方不会提前下架活动商品)
                            if item[0] not in pintuan_goods_all_goods_id:
                                await self.update_data_2(
                                    jumeiyoupin_pintuan=jumeiyoupin_pintuan,
                                    jumei_pintuan_url=item[4],
                                    goods_id=item[0],
                                    pipeline=sql_cli
                                )

                            else:   # 未内部下架
                                await self.update_data_1(
                                    jumeiyoupin_pintuan=jumeiyoupin_pintuan,
                                    jumeiyoupin_2=jumeiyoupin_2,
                                    jumei_pintuan_url=item[4],
                                    goods_id=item[0],
                                    item_list=item_list,
                                    pipeline=sql_cli
                                )

                else:
                    self.lg.error('数据库连接失败，此处跳过!')
                    pass

                index += 1
                gc.collect()
            self.lg.info('全部数据更新完毕'.center(100, '#'))
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(10*60)
            gc.collect()

        return None

    async def update_data_1(self, **kwargs):
        '''
        正常更新在售拼团商品信息
        :param kwargs:
        :return:
        '''
        jumeiyoupin_pintuan = kwargs.get('jumeiyoupin_pintuan')
        jumei_pintuan_url = kwargs.get('jumei_pintuan_url')
        goods_id = kwargs.get('goods_id')
        item_list = kwargs.get('item_list')
        jumeiyoupin_2 = kwargs.get('jumeiyoupin_2')
        pipeline = kwargs.get('pipeline')
        for item_2 in item_list:
            if item_2.get('goods_id', '') == goods_id:
                s_time = time.time()
                goods_data = await jumeiyoupin_pintuan.deal_with_data(jumei_pintuan_url=jumei_pintuan_url)
                if goods_data == {}:
                    pass
                else:  # 规范化
                    goods_data['goods_id'] = goods_id
                    goods_data['pintuan_time'] = item_2.get('pintuan_time', {})
                    goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = await jumeiyoupin_2.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=goods_data['pintuan_time'])

                    # pprint(goods_data)
                    # print(goods_data)
                    await jumeiyoupin_pintuan.update_jumeiyoupin_pintuan_table(data=goods_data, pipeline=pipeline, logger=self.lg)
                e_time = time.time()
                if e_time - s_time > JUMEIYOUPIN_SLEEP_TIME:  # 使其更智能点
                    pass
                else:
                    await async_sleep(JUMEIYOUPIN_SLEEP_TIME - (e_time - s_time))

            else:
                pass

        return True

    async def update_data_2(self, **kwargs):
        '''
        更新官方内部下架，实际还在售卖的商品信息
        :param kwargs:
        :return:
        '''
        jumeiyoupin_pintuan = kwargs.get('jumeiyoupin_pintuan')
        jumei_pintuan_url = kwargs.get('jumei_pintuan_url')
        goods_id = kwargs.get('goods_id')
        pipeline = kwargs.get('pipeline')
        goods_data = await jumeiyoupin_pintuan.deal_with_data(jumei_pintuan_url=jumei_pintuan_url)
        if goods_data == {}:
            pass
        else:  # 规范化
            self.lg.info('+++ 内部下架，其实还在售卖的商品更新 +++')
            goods_data['goods_id'] = goods_id
            s_time = time.time()
            if goods_data == {}:
                pass
            else:  # 规范化
                goods_data['goods_id'] = goods_id
                # pprint(goods_data)
                # print(goods_data)
                await jumeiyoupin_pintuan.update_jumeiyoupin_pintuan_table_2(data=goods_data, pipeline=pipeline, logger=self.lg)
            e_time = time.time()
            if e_time - s_time > JUMEIYOUPIN_SLEEP_TIME:  # 使其更智能点
                pass
            else:
                await async_sleep(JUMEIYOUPIN_SLEEP_TIME - (e_time - s_time))

        return True

    async def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time < -86400:  # (为了后台能同步下架)所以设置为 24个小时
            # if diff_time < 0:     # (原先的时间)结束时间 与当前时间差 <= 0
            return 0  # 已过期恢复原价的

        elif diff_time > 0:
            return 1  # 表示是昨天跟今天的也就是待更新的

        else:  # 表示过期但是处于等待的数据不进行相关先删除操作(等<=24小时时再2删除)
            return 2

    def __del__(self):
        try:
            del self.lg
            del self.msg
            del self.api_all_goods_id
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大更新即将开始'.center(30, '-'))
        tmp = JuMeiYouPinRealTimesUpdate()
        loop = get_event_loop()
        loop.run_until_complete(tmp.run_forever())      # 切记run_until_complete()一定要接收一个return值，不然视为未结束重复打印结果
        print('麻痹的执行完了')
        try:
            del tmp
            loop.close()
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))

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