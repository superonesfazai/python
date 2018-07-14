# coding:utf-8

'''
@author = super_fazai
@File    : taobao_qianggou_miaosha_real-times_update.py
@Time    : 2018/5/15 10:09
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse_2 import TmallParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
from pprint import pprint
from logging import ERROR, INFO
import json
import time
import asyncio

from settings import IS_BACKGROUND_RUNNING
from settings import MY_SPIDER_LOGS_PATH
from settings import TMALL_REAL_TIMES_SLEEP_TIME

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import (
    daemon_init,
    restart_program,
)
from fzutils.internet_utils import get_random_pc_ua

class TaoBaoQiangGouRealTimesUpdate(object):
    '''NOTICE: 由于都是当天数据, 此处不更新上下架时间，就更新商品数据'''
    def __init__(self, logger=None):
        self._set_headers()
        self._set_logger(logger)
        self.delete_sql_str = 'delete from dbo.tao_qianggou_xianshimiaosha where goods_id=%s'

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'referer': 'https://qiang.taobao.com/?spm=a21bo.2017.2003.1.5af911d94ZThxY',
            'authority': 'unszacs.m.taobao.com',
            # 'cookie': 't=70c4fb481898a67a66d437321f7b5cdf; cna=nbRZExTgqWsCAXPCa6QA5B86; l=AkFBuFEM2rj4GbU8Mjl3KsFo0YZa/7Vg; thw=cn; uc3=nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBz4D93q0asbvKBQU%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _cc_=UIHiLt3xSw%3D%3D; tg=0; enc=OFbfiyN19GGi1GicxsjVmrZoFzlt9plbuviK5OuthXYfocqTD%2BL079G%2BIt4OMg6ZrbV4veSg5SQEpzuMUgLe0w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=763730917900964122; v=0; cookie2=19ba7f16e8455277ab2bab67901019f4; _tb_token_=773be3e88ed35; mt=ci=-1_0; _m_h5_tk=47dc93ea103cf8a19be23189f1f01947_1525489441273; _m_h5_tk_enc=b798cc89a71cb396c359cc8a0d5eec53; uc1=cookie14=UoTeO8kAl7LI7Q%3D%3D; isg=BOTkUQppYrpizJZJHHROfuSVteTc-pJ4maPnR_4FOa9yqYVzJowOdwBvbAGxX0A_',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/淘抢购实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    async def _run_forever(self):
        '''
        实时更新所有数据
        :return:
        '''
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = 'select goods_id, miaosha_time, goods_url, page, spider_time from dbo.tao_qianggou_xianshimiaosha where site_id=28'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
        except TypeError as e:
            self.my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is not None:
            self.my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            self.my_lg.info(str(result))
            self.my_lg.info('--------------------------------------------------------')

            self.my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            await self._update_old_goods_info(tmp_sql_server=tmp_sql_server, result=result)

        else:
            pass

        if get_shanghai_time().hour == 0:   # 0点以后不更新
            sleep(60*60*5.5)
        else:
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
            miaosha_begin_time = json.loads(item[1]).get('miaosha_begin_time')
            miaosha_begin_time = int(str(time.mktime(time.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')))[0:10])
            # self.my_lg.info(str(miaosha_begin_time))

            tmall = TmallParse(logger=self.my_lg)
            if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                self.my_lg.info('正在重置，并与数据库建立新连接中...')
                tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                self.my_lg.info('与数据库的新连接成功建立...')

            if tmp_sql_server.is_connect_success:
                if await self.is_recent_time(miaosha_begin_time) == 0:
                    tmp_sql_server._delete_table(sql_str=self.delete_sql_str, params=(item[0],))
                    self.my_lg.info('过期的goods_id为(%s)' % item[0] + ', 限时秒杀开始时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_begin_time'))

                else:   # 返回1, 表示在待更新的区间内
                    self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (item[0], str(index)))

                    '''NOTICE: 由于都是当天数据, 此处不更新上下架时间，就更新商品数据'''
                    goods_id = tmall.get_goods_id_from_url(item[2])

                    tmall.get_goods_data(goods_id=goods_id)
                    goods_data = tmall.deal_with_data()

                    if goods_data != {}:
                        # self.my_lg.info(str(item))
                        goods_data['goods_id'] = item[0]

                        await tmall._update_taoqianggou_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                        await asyncio.sleep(TMALL_REAL_TIMES_SLEEP_TIME)
                    else:
                        await asyncio.sleep(5)

                index += 1

            try: del tmall
            except: pass

        gc.collect()

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
        if diff_time < -259200:     # (为了后台能同步下架)所以设置为 72个小时, 只需要更新过去48小时和对与当前时间的未来2小时的商品信息
        # if diff_time < -172800:     # (原先的时间)48个小时, 只需要跟新过去48小时和对与当前时间的未来2小时的商品信息
            return 0    # 已过期恢复原价的
        else:
            return 1    # 表示是昨天跟今天的也就是待更新的


    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        taobao_qianggou = TaoBaoQiangGouRealTimesUpdate()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(taobao_qianggou._run_forever())
        try:
            del taobao_qianggou
            loop.close()
        except: pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        restart_program()   # 通过这个重启环境, 避免log重复打印
        sleep(60*10)

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