# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_pintuan.py
@Time    : 2018/3/25 11:32
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

import json
import re
import time
from pprint import pprint
import gc
from time import sleep
from logging import INFO, ERROR
import asyncio, aiohttp

from settings import MY_SPIDER_LOGS_PATH
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    IS_BACKGROUND_RUNNING,
    JUMEIYOUPIN_SLEEP_TIME,
    JUMEIYOUPIN_PINTUAN_API_TIMEOUT,
    PHANTOMJS_DRIVER_PATH,
)
import datetime
from jumeiyoupin_pintuan_parse import JuMeiYouPinPinTuanParse

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import (
    daemon_init,
    restart_program,
)
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import MyPhantomjs

class JuMeiYouPinPinTuan(object):
    def __init__(self, logger=None):
        self._set_headers()
        self.msg = ''
        self._set_logger(logger)
        self.tab_dict = {
            '母婴健康': 'coutuan_baby',
            '家居': 'coutuan_furniture',
            '饰品配饰': 'coutuan_jewellery',
            '内衣': 'coutuan_underwear',
            '食品保健': 'coutuan_food',
            '美妆': 'coutuan_makeup',
            '女装': 'coutuan_ladies',
            '礼品箱包': 'coutuan_bag',
            '数码家电': 'coutuan_3c',
            '鞋类': 'coutuan_shose',
            '下期预告': 'coutuan_pre',
        }

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

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/聚美优品/拼团/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    async def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时拼团商品信息
        :return:
        '''
        s_time = time.time()
        goods_list = []
        my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH, logger=self.my_lg)
        for key in self.tab_dict:
            self.msg = '正在抓取的分类为: ' + key
            self.my_lg.info(self.msg)
            for index in range(1, 20):
                item_list = await self.get_one_page_goods_list(my_phantomjs=my_phantomjs, key=key, tab=self.tab_dict[key], index=index)

                all_goods_id = list(set([s.get('goods_id', '') for s in goods_list]))
                for item in item_list:
                    if item.get('goods_id', '') not in all_goods_id:
                        goods_list.append(item)
                # await asyncio.sleep(.5)

                # break
            # break

        try: del my_phantomjs
        except: pass
        self.my_lg.info(str(goods_list))
        self.my_lg.info('本次抓到所有拼团商品个数为: ' + str(len(goods_list)))
        e_time = time.time()
        self.my_lg.info('总用时:' + str(e_time-s_time))
        await asyncio.sleep(3)

        return goods_list

    async def deal_with_data(self):
        '''
        处理并存储相关拼团商品的数据
        :return:
        '''
        goods_list = await self.get_pintuan_goods_info()

        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            db_goods_id_list = [item[0] for item in list(await my_pipeline.select_jumeiyoupin_pintuan_all_goods_id(logger=self.my_lg))]
            # self.my_lg.info(str(db_goods_id_list))

            index = 1
            for item in goods_list:
                if index % 20 == 0:
                    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

                if item.get('goods_id', '') in db_goods_id_list:
                    self.my_lg.info('该goods_id已经存在于数据库中, 此处跳过')
                    pass
                else:
                    goods_id = item.get('goods_id', '')
                    tmp_url = 'https://s.h5.jumei.com/yiqituan/detail?item_id={0}&type={1}'.format(goods_id, item.get('type', ''))

                    s_time = time.time()

                    jumeiyoupin = JuMeiYouPinPinTuanParse(logger=self.my_lg)
                    goods_data = await jumeiyoupin.deal_with_data(jumei_pintuan_url=tmp_url)

                    if goods_data == {} or goods_data.get('is_delete', 0) == 1:
                        pass
                    else:
                        # 规范化
                        goods_data['goods_id'] = goods_id
                        goods_data['pintuan_time'] = item.get('pintuan_time', {})
                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = await self.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=item.get('pintuan_time', {}))
                        goods_data['sort'] = item.get('sort')
                        goods_data['page'] = item.get('page')
                        goods_data['tab'] = item.get('tab')

                        # pprint(goods_data)
                        # print(goods_data)
                        await jumeiyoupin.insert_into_jumeiyoupin_pintuan_table(data=goods_data, pipeline=my_pipeline, logger=self.my_lg)

                    e_time = time.time()
                    if e_time - s_time > JUMEIYOUPIN_SLEEP_TIME:    # 使其更智能点
                        pass
                    else:
                        await asyncio.sleep(JUMEIYOUPIN_SLEEP_TIME - (e_time-s_time))
                    index += 1

        else:
            self.my_lg.error('数据库连接失败，此处跳过!')
            pass

        gc.collect()
        return None

    async def get_one_page_goods_list(self, **kwargs):
        '''
        获取单页面的goods_list
        :param kwargs:
        :return: item_list 类型list
        '''
        my_phantomjs = kwargs.get('my_phantomjs')
        key = kwargs.get('key', '')
        tab = kwargs.get('tab', '')
        index = kwargs.get('index')
        i_time = time.time()
        tmp_url = 'http://s.h5.jumei.com/yiqituan/tab_list?tab={0}&page={1}&per_page=20'.format(
            tab,
            str(index)
        )
        # 常规requests被过滤, aiohttp成功, 测试发现：设置时间短抓取较快
        # body = await MyAiohttp.aio_get_url_body(url=tmp_url, headers=self.headers, timeout=JUMEIYOUPIN_PINTUAN_API_TIMEOUT)

        # 改用phantomjs，aiohttp太慢
        body = my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)
        try: body = re.compile('<pre .*?>(.*)</pre>').findall(body)[0]
        except: pass
        await asyncio.sleep(1)
        # self.my_lg.info(body)

        self.msg = '正在抓取第' + str(index) + '页...' + ' ☭ 用时: ' + str(time.time() - i_time)
        self.my_lg.info(self.msg)

        item_list = []
        if body == '':
            self.msg = '获取到的body为空str!' + ' 出错地址: ' + tmp_url
            self.my_lg.error(self.msg)
        else:
            one_data = await self.json_2_dict(json_str=body)
            if one_data == {}:
                self.msg = '出错地址: ' + tmp_url
                self.my_lg.error(self.msg)
            else:
                if one_data.get('data', []) == []:
                    pass

                else:
                    tmp_item_list = one_data.get('data', [])

                    for item in tmp_item_list:      # 由于await 不能理解列表表达式，就采用常规做法
                        if item.get('status', '') != 'soldout':
                            item_list.append({
                                'goods_id': item.get('item_id', ''),
                                'pintuan_time': {
                                    'begin_time': timestamp_to_regulartime(item.get('start_time', '0')),
                                    'end_time': timestamp_to_regulartime(item.get('end_time', '0')),
                                },
                                'type': item.get('type', ''),
                                'sort': key,
                                'page': index,
                                'tab': tab,
                            })
                    # self.my_lg.info(str(item_list))

        return item_list

    async def json_2_dict(self, json_str):
        '''
        异步json_2_dict
        :param json_str:
        :return: {} | {...}
        '''
        try:
            tmp = json.loads(json_str)
        except Exception:
            self.my_lg.error('json转换json_str时出错,请检查!')
            tmp = {}
        return tmp

    async def get_pintuan_begin_time_and_pintuan_end_time(self, pintuan_time):
        '''
        返回拼团开始和结束时间
        :param pintuan_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = pintuan_time.get('begin_time')
        pintuan_end_time = pintuan_time.get('end_time')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        jumeiyoupin_pintuan = JuMeiYouPinPinTuan()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(jumeiyoupin_pintuan.deal_with_data())
        try:
            del jumeiyoupin_pintuan
            loop.close()
        except: pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        restart_program()       # 通过这个重启环境, 避免log重复打印

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