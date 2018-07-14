# coding:utf-8

'''
@author = super_fazai
@File    : taobao_qianggou_spike.py
@Time    : 2018/5/5 10:44
@connect : superonesfazai@gmail.com
'''

"""
淘抢购板块抓取清洗入库
    url: https://qiang.taobao.com/?spm=a21bo.2017.2003.1.5af911d94ZThxY
"""

import sys
sys.path.append('..')

import json
import re
from pprint import pprint
from decimal import Decimal
from time import sleep
import gc
from logging import INFO, ERROR
import asyncio
import multiprocessing

from settings import (
    MY_SPIDER_LOGS_PATH,
    TAOBAO_QIANGGOU_SPIDER_HOUR_LIST,
    PHANTOMJS_DRIVER_PATH,
    IS_BACKGROUND_RUNNING,
    TMALL_REAL_TIMES_SLEEP_TIME
)
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools
)

from taobao_parse import TaoBaoLoginAndParse
from tmall_parse_2 import TmallParse

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import (
    daemon_init,
    restart_program,
)
from fzutils.cp_utils import (
    get_miaosha_begin_time_and_miaosha_end_time,
    calculate_right_sign,
    get_taobao_sign_and_body,
)
from fzutils.internet_utils import get_random_pc_ua

class TaoBaoQiangGou(object):
    def __init__(self, logger=None):
        self._set_headers()
        self._set_logger(logger)
        self.msg = ''

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
                log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/淘抢购/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    async def _get_all_goods_list(self):
        '''
        模拟构造得到淘抢购的所有商品的list, 并且解析存入每个
        :return: list
        '''
        _data = []
        _ = await self.get_crawl_time()
        for spider_time in _:
            self.my_lg.info('### 正在抓取的时间点为 {0} ###'.format(self._get_right_str_time(spider_time)))
            for page in range(1, 100, 1):
                self.my_lg.info('正在抓取第 {0} 页...'.format(page))

                body = await self._get_one_api_body(
                    page=page,
                    spider_time=spider_time,
                )
                # self.my_lg.info(str(body))
                if body == '':
                    self.msg = '获取到的body为空str! 出错spider_time: %s, page: %s' % (spider_time, str(page))
                    self.my_lg.error(self.msg)
                    continue

                try:
                    body = re.compile(r'mtopjsonp1\((.*)\)').findall(body)[0]
                except IndexError:
                    self.msg = 're筛选body时出错, 请检查! 出错spider_time: %s, page: %s' % (spider_time, str(page))
                    self.my_lg.error(self.msg)
                    continue
                tmp_data = await self._get_sort_data_list(body=body)
                if tmp_data is None or tmp_data == []:
                    break

                # self.my_lg.info(str(tmp_data))
                # 加入page, spider_time
                [_i.update({
                    'page': page,
                    'spider_time': spider_time,
                }) for _i in tmp_data]

                _data.append({
                    'data': tmp_data,
                })
                await asyncio.sleep(1.5)

        self.my_lg.info(_data)
        gc.collect()

        return _data

    async def _deal_with_all_goods_id(self):
        '''
        获取每个详细分类的商品信息
        :return: None
        '''
        _data = await self._get_all_goods_list()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        index = 1
        if my_pipeline.is_connect_success:
            self.my_lg.info('正在获取淘抢购db原有goods_id, 请耐心等待...')
            sql_str = r'select goods_id from dbo.tao_qianggou_xianshimiaosha where site_id=28'
            db_ = list(my_pipeline._select_table(sql_str=sql_str))
            db_all_goods_id = [item[0] for item in db_]
            self.my_lg.info('获取完毕!!!')
            # self.my_lg.info(str(db_all_goods_id))

            for item in _data:
                miaosha_goods_list = await self._get_taoqianggou_goods_list(data=item.get('data', []))
                # self.my_lg.info(str(miaosha_goods_list))
                # pprint(miaosha_goods_list)

                for tmp_item in miaosha_goods_list:
                    if tmp_item.get('goods_id', '') in db_all_goods_id:    # 处理如果该goods_id已经存在于数据库中的情况
                        self.my_lg.info('该goods_id[%s]已存在db中' % tmp_item.get('goods_id', ''))
                        continue

                    if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                        self.my_lg.info('正在重置，并与数据库建立新连接中...')
                        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                        # my_pipeline = SqlPools()
                        self.my_lg.info('与数据库的新连接成功建立...')

                    if my_pipeline.is_connect_success:
                        tmall = TmallParse(logger=self.my_lg)
                        tmp_url = 'https://detail.tmall.com/item.htm?id={0}'.format(tmp_item.get('goods_id'))
                        goods_id = tmall.get_goods_id_from_url(tmp_url)

                        tmall.get_goods_data(goods_id=goods_id)
                        goods_data = tmall.deal_with_data()

                        if goods_data != {}:
                            # self.my_lg.info(str(tmp_item))
                            goods_data['goods_id'] = tmp_item.get('goods_id')
                            goods_data['spider_url'] = tmp_url
                            goods_data['miaosha_time'] = tmp_item.get('miaosha_time')
                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=tmp_item.get('miaosha_time'))
                            goods_data['page'] = tmp_item.get('page')
                            goods_data['spider_time'] = tmp_item.get('spider_time')

                            tmall.insert_into_taoqianggou_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                            await asyncio.sleep(TMALL_REAL_TIMES_SLEEP_TIME)

                        else:
                            await asyncio.sleep(5)

                        try: del tmall
                        except: pass
                        gc.collect()

    async def _get_one_api_body(self, **kwargs):
        '''
        获取一个api接口的数据
        :param kwargs:
        :return:
        '''
        page = kwargs.get('page')
        spider_time = kwargs.get('spider_time')

        base_url = 'https://unszacs.m.taobao.com/h5/mtop.msp.qianggou.queryitembybatchid/3.3/'

        data = json.dumps({
            "batchId": spider_time,        # '201805051000'
            "page": page,
            "pageSize":50,
        })

        params = {
            'api': 'mtop.msp.qianggou.queryItemByBatchId',
            'appKey': '12574478',
            'callback': 'mtopjsonp1',
            'type': 'jsonp',
            # 't': t,
            # 'sign': '7d70f0f2c8bc74770ee88f3a4f67a792',
            'v': '3.3',
            'data': data,
        }

        result_1 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            logger=self.my_lg
        )
        _m_h5_tk = result_1[0]

        if _m_h5_tk == '':
            self.msg = '获取到的_m_h5_tk为空str! 出错spider_time: %s, page: %s' % (spider_time, str(page))
            self.my_lg.error(self.msg)
            return ''

        # 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
        result_2 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            _m_h5_tk=_m_h5_tk,
            session=result_1[1],
            logger=self.my_lg
        )
        body = result_2[2]

        return body

    async def _get_sort_data_list(self, body):
        '''
        获取到需求的数据
        :param body:
        :return:
        '''
        try:
            _ = json.loads(body)
        except Exception:
            self.my_lg.error('json.loads转换body出错, 此处跳过!')
            _ = {}

        # if _.get('data', {}).get('items', []) == []:
        #     self.my_lg.info(str(_))

        return _.get('data', {}).get('items', [])

    async def _get_taoqianggou_goods_list(self, data):
        '''
        将data转换为需求的list
        :param data:
        :return:
        '''
        _ = []
        if data != []:
            try:
                _ = [{
                    'goods_id': item.get('itemId', ''),
                    'goods_url': 'https:' + item.get('pcUrl', ''),
                    'page': item.get('page'),
                    'spider_time': item.get('spider_time'),
                    'miaosha_time': {
                        'miaosha_begin_time': self._get_right_str_time(item.get('startTime', '')),
                        'miaosha_end_time': self._get_right_str_time(item.get('endTime', '')),
                    },
                } for item in data]
            except Exception as e:
                self.my_lg.exception(e)

        return _

    async def get_crawl_time(self):
        '''
        得到规范的待抓取的时间点
        :return: list   格式:['201805051300', ...]
        '''
        return [str(get_shanghai_time())[0:10].replace('-', '')+item+'00' for item in TAOBAO_QIANGGOU_SPIDER_HOUR_LIST]

    def _get_right_str_time(self, str_time):
        '''
        将字符串格式'201805051000'转换为'2018-05-05 10:00:00'
        :param str_time:
        :return:
        '''
        if len(str_time) < 13:
            str_time += '00'

        return str_time[0:4] + '-' + str_time[4:6] + '-' + str_time[6:8] + ' ' + str_time[8:10] + ':' + str_time[10:12] + ':' + str_time[12:14]

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
        except: pass
        gc.collect()

def just_fuck_run():
    '''由于写成守护进程无法运行, 采用tmux模式运行, 设置采集时间点用以防止采集冲突'''
    _spider_run_time = ['00', '01', '02', '03',]
    while True:
        if str(get_shanghai_time())[11:13] in _spider_run_time:
            while True:
                if str(get_shanghai_time())[11:13] not in _spider_run_time:
                    print('冲突时间点, 不抓取数据..., 上海时间%s' % str(get_shanghai_time()))
                    sleep(60*5)
                    break

                print('一次大抓取即将开始'.center(30, '-'))
                taobao_qianggou = TaoBaoQiangGou()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(taobao_qianggou._deal_with_all_goods_id())
                try:
                    del taobao_qianggou
                    loop.close()
                except: pass
                gc.collect()
                print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
                restart_program()   # 通过这个重启环境, 避免log重复打印
                sleep(60*30)

        else:
            print('未在脚本运行时间点...休眠中, 上海时间%s' % str(get_shanghai_time()))
            sleep(60*2)

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

def main_2():
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    just_fuck_run()

if __name__ == '__main__':
    # if IS_BACKGROUND_RUNNING:
    #     main()
    #
    # else:
    just_fuck_run()