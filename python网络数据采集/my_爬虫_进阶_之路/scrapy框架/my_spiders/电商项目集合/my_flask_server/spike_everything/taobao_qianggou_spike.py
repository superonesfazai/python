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

from gc import collect
from settings import (
    MY_SPIDER_LOGS_PATH,
    TAOBAO_QIANGGOU_SPIDER_HOUR_LIST,
    IS_BACKGROUND_RUNNING,
    TMALL_REAL_TIMES_SLEEP_TIME,
    IP_POOL_TYPE,)
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,)

from tmall_parse_2 import TmallParse
from sql_str_controller import tb_select_str_5
from fzutils.spider.async_always import *

class TaoBaoQiangGou(Crawler):
    def __init__(self, logger=None):
        Crawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/淘抢购/',
        )
        self._set_headers()
        self.msg = ''

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'referer': 'https://qiang.taobao.com/?spm=a21bo.2017.2003.1.5af911d94ZThxY',
            'authority': 'unszacs.m.taobao.com',
        }

    async def _get_all_goods_list(self):
        '''
        模拟构造得到淘抢购的所有商品的list, 并且解析存入每个
        :return: list
        '''
        _data = []
        _ = await self.get_crawl_time()
        for spider_time in _:
            self.lg.info('### 正在抓取的时间点为 {0} ###'.format(self._get_right_str_time(spider_time)))
            for page in range(1, 100, 1):
                self.lg.info('正在抓取第 {0} 页...'.format(page))

                body = await self._get_one_api_body(
                    page=page,
                    spider_time=spider_time,
                )
                # self.lg.info(str(body))
                if body == '':
                    self.msg = '获取到的body为空str! 出错spider_time: %s, page: %s' % (spider_time, str(page))
                    self.lg.error(self.msg)
                    continue

                try:
                    body = re.compile(r'mtopjsonp1\((.*)\)').findall(body)[0]
                except IndexError:
                    self.msg = 're筛选body时出错, 请检查! 出错spider_time: %s, page: %s' % (spider_time, str(page))
                    self.lg.error(self.msg)
                    continue
                tmp_data = await self._get_sort_data_list(body=body)
                if tmp_data is None or tmp_data == []:
                    break

                # self.lg.info(str(tmp_data))
                # 加入page, spider_time
                [_i.update({
                    'page': page,
                    'spider_time': spider_time,
                }) for _i in tmp_data]

                _data.append({
                    'data': tmp_data,
                })
                await async_sleep(1.5)

        self.lg.info(_data)
        collect()

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
            self.lg.info('正在获取淘抢购db原有goods_id, 请耐心等待...')
            db_ = list(my_pipeline._select_table(sql_str=tb_select_str_5))
            db_all_goods_id = [item[0] for item in db_]
            self.lg.info('获取完毕!!!')
            # self.lg.info(str(db_all_goods_id))

            for item in _data:
                miaosha_goods_list = await self._get_taoqianggou_goods_list(data=item.get('data', []))
                # self.lg.info(str(miaosha_goods_list))
                # pprint(miaosha_goods_list)

                for tmp_item in miaosha_goods_list:
                    if tmp_item.get('goods_id', '') in db_all_goods_id:    # 处理如果该goods_id已经存在于数据库中的情况
                        self.lg.info('该goods_id[%s]已存在db中' % tmp_item.get('goods_id', ''))
                        continue

                    if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                        self.lg.info('正在重置，并与数据库建立新连接中...')
                        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                        # my_pipeline = SqlPools()
                        self.lg.info('与数据库的新连接成功建立...')

                    if my_pipeline.is_connect_success:
                        tmall = TmallParse(logger=self.lg)
                        tmp_url = 'https://detail.tmall.com/item.htm?id={0}'.format(tmp_item.get('goods_id'))
                        goods_id = tmall.get_goods_id_from_url(tmp_url)

                        tmall.get_goods_data(goods_id=goods_id)
                        goods_data = tmall.deal_with_data()

                        if goods_data != {}:
                            # self.lg.info(str(tmp_item))
                            goods_data['goods_id'] = tmp_item.get('goods_id')
                            goods_data['spider_url'] = tmp_url
                            goods_data['miaosha_time'] = tmp_item.get('miaosha_time')
                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=tmp_item.get('miaosha_time'))
                            goods_data['page'] = tmp_item.get('page')
                            goods_data['spider_time'] = tmp_item.get('spider_time')

                            res = tmall.insert_into_taoqianggou_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                            if res:
                                if tmp_item.get('goods_id', '') not in db_all_goods_id:
                                    db_all_goods_id.append(tmp_item.get('goods_id', ''))

                            await async_sleep(TMALL_REAL_TIMES_SLEEP_TIME)

                        else:
                            await async_sleep(5)

                        try: del tmall
                        except: pass
                        collect()

    async def _get_one_api_body(self, **kwargs):
        '''
        获取一个api接口的数据
        :param kwargs:
        :return:
        '''
        page = kwargs.get('page')
        spider_time = kwargs.get('spider_time')
        base_url = 'https://unszacs.m.taobao.com/h5/mtop.msp.qianggou.queryitembybatchid/3.3/'

        data = dumps({
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
            logger=self.lg,
            ip_pool_type=self.ip_pool_type
        )
        _m_h5_tk = result_1[0]

        if _m_h5_tk == '':
            self.msg = '获取到的_m_h5_tk为空str! 出错spider_time: %s, page: %s' % (spider_time, str(page))
            self.lg.error(self.msg)
            return ''

        # 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
        result_2 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            _m_h5_tk=_m_h5_tk,
            session=result_1[1],
            logger=self.lg,
            ip_pool_type=self.ip_pool_type
        )
        body = result_2[2]

        return body

    async def _get_sort_data_list(self, body):
        '''
        获取到需求的数据
        :param body:
        :return:
        '''
        data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg).get('data', {}).get('items', [])

        return data

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
                self.lg.exception(e)

        return _

    async def get_crawl_time(self):
        '''
        得到规范的待抓取的时间点
        :return: list   格式:['201805051300', ...]
        '''
        return [str(get_shanghai_time())[0:10].replace('-', '') + item + '00' for item in TAOBAO_QIANGGOU_SPIDER_HOUR_LIST]

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
            del self.lg
            del self.msg
        except: 
            pass
        collect()

def just_fuck_run():
    '''由于写成守护进程无法运行, 采用tmux模式运行, 设置采集时间点用以防止采集冲突'''
    _spider_run_time = ['00', '01', '02', '03',]
    # _spider_run_time = ['17',]
    while True:
        if str(get_shanghai_time())[11:13] in _spider_run_time:
            while True:
                if str(get_shanghai_time())[11:13] not in _spider_run_time:
                    print('冲突时间点, 不抓取数据..., 上海时间%s' % str(get_shanghai_time()))
                    sleep(60*5)
                    break

                print('一次大抓取即将开始'.center(30, '-'))
                taobao_qianggou = TaoBaoQiangGou()
                loop = get_event_loop()
                loop.run_until_complete(taobao_qianggou._deal_with_all_goods_id())
                try:
                    del taobao_qianggou
                    loop.close()
                except:
                    pass
                collect()
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
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

def main_2():
    print('========主函数开始========')
    just_fuck_run()

if __name__ == '__main__':
    # if IS_BACKGROUND_RUNNING:
    #     main()
    #
    # else:
    just_fuck_run()