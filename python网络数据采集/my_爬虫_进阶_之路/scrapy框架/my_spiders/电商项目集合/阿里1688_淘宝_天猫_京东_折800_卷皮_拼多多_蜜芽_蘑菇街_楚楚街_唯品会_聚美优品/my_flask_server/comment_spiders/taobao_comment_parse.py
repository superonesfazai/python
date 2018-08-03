# coding:utf-8

'''
@author = super_fazai
@File    : taobao_comment_parse.py
@Time    : 2017/4/10 11:21
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_items import CommentItem
from settings import MY_SPIDER_LOGS_PATH

from random import randint
from time import sleep
import gc
from logging import INFO, ERROR
from scrapy.selector import Selector
import re, datetime, json
from pprint import pprint
import requests

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict

class TaoBaoCommentParse(object):
    def __init__(self, logger=None):
        super(TaoBaoCommentParse, self).__init__()
        self.result_data = {}
        self.msg = ''
        self._set_logger(logger=logger)
        self._set_headers()
        self.comment_page_switch_sleep_time = 1.5   # 评论下一页sleep time

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        _tmp_comment_list = []
        self.my_lg.info('------>>>| 待抓取的goods_id: %s' % goods_id)

        '''
        下面抓取的是pc端的数据地址
        '''
        # 获取评论数据
        for current_page_num in range(1, 4):
            self.my_lg.info('------>>>| 正在抓取第%s页评论...' % str(current_page_num))
            tmp_url = 'https://rate.taobao.com/feedRateList.htm'
            _params = self._set_params(current_page_num=current_page_num, goods_id=goods_id)

            self.headers.update({'referer': 'https://item.taobao.com/item.htm?id='+goods_id})
            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, params=_params, encoding='gbk')
            # self.my_lg.info(str(body))

            try:
                body = re.compile('\((.*)\)').findall(body)[0]
            except IndexError:
                self.my_lg.error('re得到需求body时出错! 出错goods_id: ' + goods_id)
                sleep(.5)
                self.result_data = {}
                return {}

            data = json_2_dict(json_str=body, logger=self.my_lg).get('comments')
            # pprint(data)
            if data is None:
                self.my_lg.error('出错goods_id: ' + goods_id)
                self.result_data = {}
                return {}
            if data == []:  # 该页的"comments"=[], 跳出本次循环
                continue

            _tmp_comment_list += data
            sleep(self.comment_page_switch_sleep_time)

        # self.my_lg.info(str(len(_tmp_comment_list)))
        try:
            _comment_list = self._get_comment_list(_tmp_comment_list=_tmp_comment_list)
        except Exception as e:
            self.my_lg.error('出错goods_id: ' + goods_id)
            self.my_lg.exception(e)
            self.result_data = {}
            return {}

        _t = datetime.datetime.now()

        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        # pprint(self.result_data)

        return self.result_data

    def _get_comment_list(self, _tmp_comment_list):
        '''
        转化成需要的结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        _sku_info_list = []  # 用于存已有的规格
        for item in _tmp_comment_list:
            comment_date = item.get('date', '')
            assert comment_date != '', '得到的comment_date为空str!请检查!'
            comment_date = self._get_comment_date(comment_date)

            sku_info = item.get('auction', {}).get('sku', '')
            # self.my_lg.info(sku_info)
            if sku_info == '' and _sku_info_list == []:  # 规格为空就跳过, 即只抓取有效评论
                continue
            if sku_info != '':  # 不为空存入
                _sku_info_list.append(sku_info)
                _sku_info_list = list(set(_sku_info_list))
            if sku_info == '':  # 为空的，随机设置一个
                sku_info = _sku_info_list[randint(0, len(_sku_info_list) - 1)]
                # print(sku_info)
            sku_info = self._wash_sku_info(sku_info)

            # 评论照片
            img_url_list = item.get('photos', [])
            img_url_list = [{
                'img_url': 'https:' + _i.get('url', '')
            } for _i in img_url_list if _i.get('url', '') != '']

            _comment_content = item.get('content', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = self._wash_comment(comment=_comment_content)

            buyer_name = item.get('user', {}).get('nick', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            quantify = int(item.get('buyAmount', 0)) if item.get('buyAmount', 0) != 0 else 1

            tmp_head_img = item.get('user', {}).get('avatar', '')
            if re.compile(r'/default/avatar-40.png').findall(tmp_head_img) != []:
                head_img = ''

            # 无法识别是否为同一张图 只能先拿到这种规律的然后请求图片看齐地址
            # elif re.compile(r'vGNuOHcWv88YXF').findall(tmp_head_img) != []:
            #     # self.my_lg.info('https:' + tmp_head_img)
            #     if self._judge_is_taobao_head_img(url='https:' + tmp_head_img):
            #         self.my_lg.info('https:' + tmp_head_img)
            #         head_img = ''
            #     else:
            #         head_img = 'https:' + tmp_head_img

            elif tmp_head_img != '//wwc.alicdn.com/avatar/getAvatar.do?userIdStr=vGNuOHcWv88YXF-HPmvbM07HvG8SvFI0Xm7Hvm80MkZhvkk0XmcSPFPhPHQWOmvG&width=40&height=40&type=sns' \
                    or tmp_head_img != '//gw.alicdn.com/tps/i3/TB1yeWeIFXXXXX5XFXXuAZJYXXX-210-210.png_40x40.jpg':
                head_img = 'https:' + tmp_head_img

            else:
                head_img = ''

            if not filter_invalid_comment_content(_comment_content):
                continue

            comment = [{
                'comment': _comment_content,
                'comment_date': comment_date,
                'sku_info': sku_info,
                'img_url_list': img_url_list,
                'star_level': randint(4, 5),
                'video': item.get('video', ''),
            }]

            _ = {
                'buyer_name': buyer_name,   # 买家昵称
                'comment': comment,         # 评论内容
                'quantify': quantify,       # 购买数量
                'head_img': head_img,       # 头像
                'append_comment': {},       # 追评
            }

            _comment_list.append(_)

        return _comment_list

    def _judge_is_taobao_head_img(self, url):
        '''
        判断是否为淘宝默认头像地址
        :param url:
        :return:
        '''
        tmp_proxies = MyRequests._get_proxies()

        try:
            _res = requests.get(url=url, headers=self.headers, proxies=tmp_proxies)
            self.my_lg.info(str(_res.url))
            if _res.url == 'https://gw.alicdn.com/tps/i3/TB1yeWeIFXXXXX5XFXXuAZJYXXX-210-210.png_40x40.jpg':
                return True
            else:
                return False
        except:
            self.my_lg.info('检测图片地址时网络错误! 跳过!')
            return False

    def _set_logger(self, logger):
        '''
        设置logger
        :param logger:
        :return:
        '''
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        '''
        设置headers
        :return: dict
        '''
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'authority': 'rate.taobao.com',
            # 'referer': 'https://item.taobao.com/item.htm?id=555635098639',
        }

    def _wash_sku_info(self, sku_info):
        sku_info = sku_info.replace('&nbsp;', ' ').replace('&nbsp', ' ')

        return sku_info

    def _set_params(self, current_page_num, goods_id):
        '''
        设置params
        :param goods_id:
        :param current_page_num:
        :return:
        '''
        params = (
            ('auctionNumId', goods_id),
            # ('userNumId', '1681172037'),
            ('currentPageNum', str(current_page_num)),
            ('pageSize', '20'),
            ('rateType', '1'),
            ('orderType', 'sort_weight'),
            ('attribute', ''),
            ('sku', ''),
            ('hasSku', 'false'),
            ('folded', '0'),  # 把默认的0改成1能得到需求数据
            # ('ua', '098#E1hv1QvWvRGvUpCkvvvvvjiPPFMWAjEmRLdWlj1VPmPvtjEvnLsh1j1WR2cZgjnVRT6Cvvyv9VliFvmvngJjvpvhvUCvp2yCvvpvvhCv2QhvCPMMvvvCvpvVvUCvpvvvKphv8vvvpHwvvvmRvvCmDpvvvNyvvhxHvvmChvvvB8wvvUVhvvChiQvv9OoivpvUvvCCUqf1csREvpvVvpCmpaFZmphvLv84Rs+azCIajCiABq2XrqpAhjCbFO7t+3vXwyFEDLuTRLa9C7zhVTTJhLhL+87J+u0OakSGtEkfVCl1pY2ZV1OqrADn9Wma+fmtEp75vpvhvvCCBUhCvCiI712MPY147DSOSrGukn22SYHsp7uC6bSVksyCvvpvvhCv'),
            # ('_ksTS', '1523329154439_1358'),
            # ('callback', 'jsonp_tbcrate_reviews_list'),
        )

        return params

    def _wash_comment(self, comment):
        '''
        清洗评论
        :param sku_info:
        :return:
        '''
        comment = re.compile('淘宝|taobao|TAOBAO').sub('', comment)

        return comment

    def _get_comment_date(self, comment_date:str):
        '''
        将格式如:2017年12月07日 14:50 转换为 '2017-12-07 14:50:00'
        :param comment_date:
        :return:
        '''
        return comment_date.replace('年', '-').replace('月', '-').replace('日', '') + ':00'

    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    taobao = TaoBaoCommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        taobao._get_comment_data(goods_id=goods_id)

        gc.collect()