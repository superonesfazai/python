# coding:utf-8

'''
@author = super_fazai
@File    : tmall_comment_parse.py
@Time    : 2018/4/11 09:51
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse import TmallParse
from my_phantomjs import MyPhantomjs
from my_logging import set_logger
from my_utils import get_shanghai_time, string_to_datetime, _get_url_contain_params
from settings import HEADERS, MY_SPIDER_LOGS_PATH

from random import randint
from time import sleep
import gc
from logging import INFO, ERROR
from scrapy.selector import Selector
import re, datetime, json
from pprint import pprint

class TmallCommentParse(object):
    def __init__(self, logger=None):
        self.result_data = {}
        self.msg = ''
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/天猫/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS)-1)],
            'accept': '*/*',
            'referer': 'https://detail.m.tmall.com/item.htm?id=524718632348',
        }
        self.page_size = '10'
        self.comment_page_switch_sleep_time = 1.5   # 评论下一页sleep time
        self.my_phantomjs = MyPhantomjs()

    def _get_comment_data(self, type:int, goods_id):
        if goods_id == '' or type == '':
            self.result_data = {}
            return {}
        self.my_lg.info('待抓取的goods_id: %s' % goods_id)

        '''
        先通过网页源码，获取到sellerId
        '''
        try:
            _ = TmallParse()
            _g = [type, goods_id]
            seller_id = str(_.get_goods_data(goods_id=_g).get('seller', {}).get('userId', 0))
            self.my_lg.info('获取到的seller_id: ' + seller_id)
            try: del _
            except: pass
            assert seller_id != 0, '获取到的seller_id为0! 出错goods_id: ' + goods_id
        except AssertionError as e:
            self.my_lg.error(e.args[0])
            self.result_data = {}
            return {}

        _tmp_comment_list = []
        for current_page in range(1, 4):
            _url = 'https://rate.tmall.com/list_detail_rate.htm'

            params = self._set_params(goods_id=goods_id, seller_id=seller_id, current_page=current_page)
            self.headers.update({'referer': 'https://detail.m.tmall.com/item.htm?id='+goods_id})

            # 原先用代理请求不到数据的原因是没有cookies
            # body = MyRequests.get_url_body(url=_url, headers=self.headers, params=params, encoding='gbk')

            # 所以直接用phantomjs来获取相关api数据
            _url = _get_url_contain_params(url=_url, params=params)     # 根据params组合得到url
            # self.my_lg.info(_url)

            body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=_url)
            # self.my_lg.info(str(body))
            if body == '':
                self.my_lg.error('获取到的body为空str! 出错type:{0}, goods_id:{1}'.format(str(type), goods_id))
                self.result_data = {}
                return {}

            try:
                _ = re.compile('\((.*)\)').findall(body)[0]
            except IndexError:
                _ = {}
                self.my_lg.error('索引异常! 出错type:{0}, goods_id:{1}'.format(str(type), goods_id))

            try:
                data = json.loads(_).get('rateDetail', {}).get('rateList', [])
                # pprint(data)
            except:
                data = []
                self.my_lg.error('json.loads转换_出错! 出错type:{0}, goods_id:{1}'.format(str(type), goods_id))
            _tmp_comment_list += data
            sleep(self.comment_page_switch_sleep_time)

        try:
            _comment_list = self._get_comment_list(_tmp_comment_list=_tmp_comment_list)
        except Exception as e:
            self.my_lg.error('出错type:{0}, goods_id:{1}'.format(str(type), goods_id))
            self.my_lg.exception(e)
            self.result_data = {}
            return {}

        _t = datetime.datetime.now()
        self.result_data = {
            'goods_id': str(goods_id),
            'create_time': _t,
            'modify_time': _t,
            '_comment_list': _comment_list,
        }
        pprint(self.result_data)
        return self.result_data

    def _get_comment_list(self, _tmp_comment_list):
        '''
        转换成需求的结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        for item in _tmp_comment_list:
            _comment_date = item.get('rateDate', '')
            assert _comment_date != '', '得到的_comment_date为空str!请检查!'

            # 天猫接口拿到的sku_info默认为空
            sku_info = ''

            _comment_content = item.get('rateContent', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = self._wash_comment(comment=_comment_content)

            buyer_name = item.get('displayUserNick', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            # 天猫设置默认 购买量为1
            quantify = 1

            # 天猫没有head_img回传，就设置一个默认地址
            head_img = ''

            # 第一次评论图片
            _comment_img_list = item.get('pics', []) if item.get('pics', '') != '' else []
            if _comment_img_list != []:
                _comment_img_list = [{'img_url': 'https:' + img} for img in _comment_img_list]

            '''追评'''
            _tmp_append_comment = item.get('appendComment', {}) if item.get('appendComment', '') != '' else {}
            # 追评的图片
            _append_comment_img_list = _tmp_append_comment.get('pics', []) if _tmp_append_comment.get('pics',
                                                                                                      '') != '' else []
            if _append_comment_img_list != []:
                _append_comment_img_list = [{'img_url': 'https:' + img} for img in _comment_img_list]

            if _tmp_append_comment != {}:
                append_comment = {
                    'comment_date': _tmp_append_comment.get('commentTime', ''),
                    'comment': self._wash_comment(_tmp_append_comment.get('content', '')),
                    'img_url_list': _append_comment_img_list,
                }
            else:
                append_comment = {}

            comment = [{
                'comment': _comment_content,
                'comment_date': _comment_date,
                'sku_info': sku_info,
                'img_url_list': _comment_img_list,
                'star_level': randint(4, 5),
                'video': '',
            }]

            _ = {
                'buyer_name': buyer_name,           # 买家昵称
                'comment': comment,                 # 评论内容
                'quantify': quantify,               # 评论数量
                'head_img': head_img,               # 头像
                'append_comment': append_comment,   # 追评
            }

            _comment_list.append(_)

        return _comment_list

    def _wash_comment(self, comment):
        '''
        清洗评论
        :param comment:
        :return:
        '''
        comment = comment.replace('天猫', '')

        return comment

    def _set_params(self, **kwargs):
        '''
        设置params
        :param kwargs:
        :return:
        '''
        goods_id = kwargs.get('goods_id')
        seller_id = kwargs.get('seller_id')
        current_page = kwargs.get('current_page')
        callback = '_DLP_2519_der_3_currentPage_{0}_pageSize_{1}_'.format(str(current_page), self.page_size)
        _params = (
            ('itemId', goods_id),
            ('sellerId', seller_id),
            ('order', '3'),
            ('currentPage', str(current_page)),
            ('pageSize', self.page_size),
            ('callback', callback),
        )

        return _params

    def __del__(self):
        try:
            del self.my_lg
            del self.my_phantomjs
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    tmall = TmallCommentParse()
    while True:
        _type = input('请输入要爬取的商品type(以英文分号结束): ')
        _type = _type.strip('\n').strip(';')
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        tmall._get_comment_data(type=int(_type), goods_id=goods_id)

        gc.collect()
