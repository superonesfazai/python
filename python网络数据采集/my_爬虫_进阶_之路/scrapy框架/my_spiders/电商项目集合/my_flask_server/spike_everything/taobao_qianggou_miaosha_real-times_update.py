# coding:utf-8

'''
@author = super_fazai
@File    : taobao_qianggou_miaosha_real-times_update.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse_2 import TmallParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from gc import collect
import time

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TMALL_REAL_TIMES_SLEEP_TIME,
    IP_POOL_TYPE,)
from sql_str_controller import (
    tb_delete_str_1,
    tb_select_str_4,
    tb_update_str_4,)
from multiplex_code import (
    _print_db_old_data,
    _get_new_db_conn,)
from fzutils.spider.async_always import *

class TaoBaoQiangGouRealTimesUpdate(Crawler):
    '''NOTICE: 由于都是当天数据, 此处不更新上下架时间，就更新商品数据'''
    def __init__(self, logger=None):
        Crawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            logger=logger,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/淘抢购实时更新/',)
        self._set_headers()
        self.delete_sql_str = tb_delete_str_1

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'referer': 'https://qiang.taobao.com/?spm=a21bo.2017.2003.1.5af911d94ZThxY',
            'authority': 'unszacs.m.taobao.com',
        }

    async def _run_forever(self):
        '''
        实时更新所有数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server._select_table(sql_str=tb_select_str_4))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        await _print_db_old_data(result=result, logger=self.lg)
        if result is not None:
            await self._update_old_goods_info(tmp_sql_server=tmp_sql_server, result=result)

        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
            self.lg.info('休眠60s...')
            sleep(60)

        return

    async def _update_old_goods_info(self, tmp_sql_server, result):
        '''
        更新old goods 数据
        :param result:
        :return:
        '''
        index = 1
        for item in result:  # 实时更新数据
            miaosha_begin_time = json_2_dict(
                json_str=item[1],
                logger=self.lg,).get('miaosha_begin_time')
            miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')))[0:10])
            # self.lg.info(str(miaosha_begin_time))

            tmall = TmallParse(logger=self.lg)
            tmp_sql_server = await _get_new_db_conn(
                db_obj=tmp_sql_server,
                index=index,
                logger=self.lg,
                remainder=20,)

            if tmp_sql_server.is_connect_success:
                if await self.is_recent_time(miaosha_begin_time) == 0:
                    # tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0],))
                    tmp_sql_server._update_table(sql_str=tb_update_str_4, params=(item[0],))
                    self.lg.info('过期的goods_id为(%s)' % item[0] + ', 限时秒杀开始时间为(%s), 删除成功!' % miaosha_begin_time)
                    await async_sleep(.3)

                else:   # 返回1, 表示在待更新的区间内
                    self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (item[0], str(index)))

                    '''NOTICE: 由于都是当天数据, 此处不更新上下架时间，就更新商品数据'''
                    goods_id = tmall.get_goods_id_from_url(item[2])

                    tmall.get_goods_data(goods_id=goods_id)
                    goods_data = tmall.deal_with_data()

                    if goods_data != {}:
                        # self.lg.info(str(item))
                        goods_data['goods_id'] = item[0]

                        await tmall._update_taoqianggou_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                        await async_sleep(TMALL_REAL_TIMES_SLEEP_TIME)
                    else:
                        await async_sleep(5)

                index += 1

            try: del tmall
            except: pass

        collect()

        return

    async def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = datetime_to_timestamp(get_shanghai_time())  # 当前的时间戳(上海时间)

        diff_time = time_1 - time_2
        # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        if diff_time < -259200:     
        # if diff_time < -172800:     
        #     # (原先的时间)48个小时, 只需要跟新过去48小时和对与当前时间的未来2小时的商品信息
            return 0    # 已过期恢复原价的
        else:
            # 表示是昨天跟今天的也就是待更新的
            return 1    

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        tqg = TaoBaoQiangGouRealTimesUpdate()
        loop = get_event_loop()
        loop.run_until_complete(tqg._run_forever())
        try:
            del tqg
            loop.close()
        except: pass
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*10)

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