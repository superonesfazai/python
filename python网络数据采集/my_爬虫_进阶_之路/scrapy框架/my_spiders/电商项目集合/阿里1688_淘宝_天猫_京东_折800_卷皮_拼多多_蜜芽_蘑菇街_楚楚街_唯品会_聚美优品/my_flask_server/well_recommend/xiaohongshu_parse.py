# coding:utf-8

'''
@author = super_fazai
@File    : xiaohongshu_parse.py
@Time    : 2018/7/9 13:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_logging import set_logger
from my_requests import MyRequests
from my_utils import (
    get_shanghai_time,
)

from settings import (
    MY_SPIDER_LOGS_PATH,
    HEADERS,
)

from random import randint
from logging import INFO, ERROR
import gc
from time import sleep
from json import (
    loads,
    JSONDecodeError,
)
from pprint import pprint

class XiaoHongShuParse():
    def __init__(self, logger=None):
        self._set_logger(logger)
        self._set_headers()

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS) - 1)],
            'accept': '*/*',
            # 'referer': 'https://h5.m.taobao.com/awp/core/detail.htm?id=560666972076',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/小红书/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _get_xiaohongshu_home_aritle_info(self):
        '''
        小红书主页json模拟获取
        :return:
        '''
        # cookies = {
        #     'beaker.session.id': '2ce91a013076367573e263a34e3691a510bb0479gAJ9cQEoVQhfZXhwaXJlc3ECY2RhdGV0aW1lCmRhdGV0aW1lCnEDVQoH4gcNDQoiDh9FhVJxBFULc2Vzc2lvbmlkLjFxBVgbAAAAc2Vzc2lvbi4xMjEwNDI3NjA2NTM0NjEzMjgycQZVCHVzZXJpZC4xcQdYGAAAADU4ZWRlZjc0NWU4N2U3NjBjOWMyNzAyNHEIVQNfaWRxCVUgMjMyNTRkOWU1MDUyNDY3NDkzZTMzZGM0YjE1MzUzZmZxClUOX2FjY2Vzc2VkX3RpbWVxC0dB1s/aksJmZlUOX2NyZWF0aW9uX3RpbWVxDEdB1s/akrUrE3Uu',
        #     'xhsTrackerId': '96359c99-a7b3-4725-c75d-2ee052cf2cc1',
        #     'xhs_spid.5dde': '9f350c095b58c416.1529844024.1.1529844045.1529844024.dfa500dd-18b6-4cf1-a094-3bc87addd183',
        # }

        headers = {
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive',
            # 'device_id': '2AEEF650-2CAE-480F-B30C-CA5CABC26193',
            'Accept': 'application/json',
            'Host': 'www.xiaohongshu.com',
            'User-Agent': 'discover/5.19.1 (iPhone; iOS 11.0; Scale/3.00) Resolution/1242*2208 Version/5.19.1 Build/5191001 Device/(Apple Inc.;iPhone7,1)',
            # 'Authorization': 'session.1210427606534613282',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'X-Tingyun-Id': 'LbxHzUNcfig;c=2;r=551911068',
        }

        # 下面参数每个都是必须的
        params = (
            ('deviceId', '2AEEF650-2CAE-480F-B30C-CA5CABC26193'),
            ('device_fingerprint', '201805101352429dd715d37f422fe3e64dd3923c0b0bc8017d90c099539039'),
            ('device_fingerprint1', '201805101352429dd715d37f422fe3e64dd3923c0b0bc8017d90c099539039'),
            ('lang', 'zh'),
            ('num', '10'),
            ('oid', 'homefeed_recommend'),
            ('platform', 'iOS'),
            ('sid', 'session.1210427606534613282'),
            ('sign', 'c9a9eadc6c46823ae3075d7b28fe97fa'),
            ('t', '1531010946'),
        )

        url = 'https://www.xiaohongshu.com/api/sns/v6/homefeed'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params, cookies=None)
        # self.my_lg.info(body)
        if body == '':
            self.my_lg.error('获取到的body为空值!请检查!')
            return {}

        _ = self.json_2_dict(body)
        pprint(_)

    def _parse_page(self):
        '''
        解析单个article的info
        :return:
        '''
        pass

    def json_2_dict(self, json_str):
        '''
        json_str转dict
        :param json_str:
        :return:
        '''
        _ = {}
        try:
            _ = loads(json_str)
        except JSONDecodeError:
            self.my_lg.error('json转换json_str时出错!请检查!')

        return _

    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    while True:
        _ = XiaoHongShuParse()
        _._get_xiaohongshu_home_aritle_info()
        sleep(60)