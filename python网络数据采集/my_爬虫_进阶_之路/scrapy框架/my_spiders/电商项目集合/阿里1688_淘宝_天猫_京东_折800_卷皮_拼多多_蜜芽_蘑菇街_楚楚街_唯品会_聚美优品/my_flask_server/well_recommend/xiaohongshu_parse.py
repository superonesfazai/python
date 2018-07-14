# coding:utf-8

'''
@author = super_fazai
@File    : xiaohongshu_parse.py
@Time    : 2018/7/9 13:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_requests import MyRequests

from settings import (
    MY_SPIDER_LOGS_PATH,
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
import time
import re

from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import get_random_pc_ua

class XiaoHongShuParse():
    def __init__(self, logger=None):
        self._set_logger(logger)
        self._set_headers()
        self.CRAWL_ARTICLE_SLEEP_TIME = 2.5     # 抓每天文章的sleep_time

    def _set_headers(self):
        self.headers = {
            'authority': 'www.xiaohongshu.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'Hm_lvt_9df7d19786b04345ae62033bd17f6278=1530954715,1530954763,1530954908,1531113520; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1530954716,1530954763,1530954907,1531113520; Hm_lpvt_d0ae755ac51e3c5ff9b1596b0c09c826=1531119425; Hm_lpvt_9df7d19786b04345ae62033bd17f6278=1531119425; beaker.session.id=b8a1a4ca0c2293ec3d447c7edbdc9dc2c528b5f2gAJ9cQEoVQhfZXhwaXJlc3ECY2RhdGV0aW1lCmRhdGV0aW1lCnEDVQoH4gcOCQIMAD2ghVJxBFUDX2lkcQVVIDNmMmM5NmE1YjQzNDQyMjA5MDM5OTIyNjU4ZjE3NjIxcQZVDl9hY2Nlc3NlZF90aW1lcQdHQdbQwdBhhRtVDl9jcmVhdGlvbl90aW1lcQhHQdbQIEMRyBF1Lg==; xhs_spses.5dde=*; xhs_spid.5dde=af753270e27cdd3c.1530953997.5.1531119433.1531115989.18f4b29f-8212-42a2-8ad6-002c47ebdb65',
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

    def _get_xiaohongshu_home_aritles_info(self):
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

        # 下面参数每个都是必须的, 且不变
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
            ('t', '1531010946'),    # 用原来的避免sign错误
            # ('t', int(time.time())),
        )

        url = 'https://www.xiaohongshu.com/api/sns/v6/homefeed'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params, cookies=None)
        # self.my_lg.info(body)
        if body == '':
            self.my_lg.error('获取到的body为空值!请检查!')
            return {}

        _ = self.json_2_dict(body).get('data', [])
        # pprint(_)
        if _ == []:
            self.my_lg.error('获取到的data为空值!请检查!')
            return {}

        _ = [{
            'id': item.get('id', ''),
            'article_link': item.get('share_link', ''),
        } for item in _]

        return _

    def _deal_with_every_article(self):
        home_articles_link_list = self._get_xiaohongshu_home_aritles_info()
        pprint(home_articles_link_list)

        for item in home_articles_link_list:    # eg: [{'id': '5b311bfc910cf67e693d273e','share_link': 'https://www.xiaohongshu.com/discovery/item/5b311bfc910cf67e693d273e'},...]
            article_id = item.get('id', '')
            article_link = item.get('article_link', '')

            if article_link != '':
                body = MyRequests.get_url_body(url=article_link, headers=self.headers)
                try:
                    article_info = re.compile('window.__INITIAL_SSR_STATE__=(.*?)</script>').findall(body)[0]
                except IndexError:
                    self.my_lg.error('获取article_info时IndexError!请检查!')
                    sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
                    continue

                article_info = self._wash_article_info(self.json_2_dict(article_info))
                pprint(article_info)
                sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            else:
                pass

    def _wash_article_info(self, _dict):
        '''
        清洗无用字段
        :param _dict:
        :return:
        '''
        try:
            _dict['NoteView']['commentInfo'] = {}   # 评论信息
            _dict['NoteView']['panelData'] = []     # 相关笔记
        except:
            pass

        return _dict

    def wash_sensitive_info(self, data):
        '''
        清洗敏感信息
        :param data:
        :return:
        '''
        data = re.compile(r'小红书|xiaohongshu|XIAOHONGSHU').sub('优秀网', data)

        tmp_str = r'''
        淘宝|taobao|TAOBAO|天猫|tmall|TMALL|
        京东|JD|jd|红书爸爸|共产党|邪教|操|艹|
        杀人|胡锦涛|江泽民|习近平
        '''.replace(' ', '').replace('\n', '')
        data = re.compile(tmp_str).sub('', data)

        return data

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
        _._deal_with_every_article()
        sleep(60)