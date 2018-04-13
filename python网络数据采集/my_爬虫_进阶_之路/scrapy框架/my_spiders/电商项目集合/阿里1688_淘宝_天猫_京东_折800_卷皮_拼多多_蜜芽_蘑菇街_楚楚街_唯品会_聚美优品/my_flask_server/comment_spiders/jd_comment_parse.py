# coding:utf-8

'''
@author = super_fazai
@File    : jd_comment_parse.py
@Time    : 2018/4/13 13:51
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_phantomjs import MyPhantomjs
from my_requests import MyRequests
from my_logging import set_logger
from my_utils import get_shanghai_time, string_to_datetime
from settings import HEADERS, MY_SPIDER_LOGS_PATH

from random import randint
from time import sleep
import gc
from logging import INFO, ERROR
import re, datetime, json
from pprint import pprint

class JdCommentParse(object):
    def __init__(self, logger=None):
        self.result_data = {}
        self.msg = ''
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/京东/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger
        self.headers = {
            'origin': 'https://item.m.jd.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS)-1)],
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
            'referer': 'https://item.m.jd.com/ware/view.action?wareId=5025518',
            'authority': 'item.m.jd.com',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.comment_page_switch_sleep_time = 1.2  # 评论下一页sleep time
        self.my_phantomjs = MyPhantomjs()

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        self.my_lg.info('待抓取的goods_id: %s' % goods_id)

        # 测试发现得带cookies, 详细到cookies中的sid字符必须有
        # 先获取cookies
        _cookies = self.my_phantomjs.get_url_cookies_from_phantomjs_session(url='https://item.m.jd.com/')
        # self.my_lg.info(str(_cookies))
        self.headers.update({
            'cookie': _cookies,
            'referer': 'https://item.m.jd.com/ware/view.action?wareId=' + str(goods_id),
        })

        # 根据京东手机版商品评价获取
        _tmp_comment_list = []
        for current_page in range(1, 3):
            _url = 'https://item.m.jd.com/newComments/newCommentsDetail.json'

            params = self._set_params(goods_id=goods_id, current_page=current_page)
            body = MyRequests.get_url_body(url=_url, headers=self.headers, params=params)
            self.my_lg.info(str(body))

            sleep(self.comment_page_switch_sleep_time)

    def _set_params(self, goods_id, current_page):
        '''
        设置params
        :param goods_id:
        :param current_page:
        :return:
        '''
        _params = [
          ('wareId', goods_id),
          ('offset', str(current_page)),
          ('num', '10'),
          ('checkParam', 'LUIPPTP'),
          ('category', '670_671_1105'),
          ('isUseMobile', 'true'),
          ('evokeType', ''),
          ('type', '0'),
          ('isCurrentSku', 'false'),
        ]

        return _params

    def __del__(self):
        try:
            del self.my_lg
            del self.my_phantomjs
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    jd = JdCommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        jd._get_comment_data(goods_id=goods_id)

        gc.collect()