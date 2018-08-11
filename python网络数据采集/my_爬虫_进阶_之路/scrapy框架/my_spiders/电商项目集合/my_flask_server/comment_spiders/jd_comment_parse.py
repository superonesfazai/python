# coding:utf-8

'''
@author = super_fazai
@File    : jd_comment_parse.py
@Time    : 2018/4/13 13:51
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_items import CommentItem
from settings import (
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,)

from time import sleep
import gc
from logging import INFO, ERROR
import re
import datetime
from pprint import pprint

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    string_to_datetime,
)
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import json_2_dict

class JdCommentParse(object):
    def __init__(self, logger=None):
        self.result_data = {}
        self.msg = ''
        self._set_logger(logger)
        self._set_headers()
        self.comment_page_switch_sleep_time = 1.2  # 评论下一页sleep time
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)
        self._add_headers_cookies()

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        self.my_lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))

        self.goods_id = goods_id
        self.headers.update({
            'referer': 'https://item.m.jd.com/ware/view.action?wareId=' + str(goods_id),
        })

        # 根据京东手机版商品评价获取
        _tmp_comment_list = []
        for current_page in range(1, 3):
            _url = 'https://item.m.jd.com/newComments/newCommentsDetail.json'

            params = self._set_params(goods_id=goods_id, current_page=current_page)
            body = MyRequests.get_url_body(url=_url, headers=self.headers, params=params)
            # self.my_lg.info(str(body))

            _data = json_2_dict(json_str=body, logger=self.my_lg).get('wareDetailComment', {}).get('commentInfoList', [])
            if _data == []:
                self.my_lg.error('出错goods_id:{0}'.format(self.goods_id))

            _tmp_comment_list += _data

            sleep(self.comment_page_switch_sleep_time)

        # pprint(_tmp_comment_list)
        try:
            _comment_list = self._get_comment_list(_tmp_comment_list=_tmp_comment_list)
        except Exception as e:
            self.my_lg.error('出错goods_id:{0}'.format(goods_id))
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
        转换成需求的结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        for item in _tmp_comment_list:
            _comment_date = item.get('commentDate', '')
            assert _comment_date != '', '得到的_comment_date为空str!请检查!'

            # sku_info(有些商品评论是没有规格的所以默认为空即可，不加assert检查!)
            ware_attributes = item.get('wareAttributes', [])
            # self.my_lg.info(str(ware_attributes))
            sku_info = ' '.join([i.get('key', '')+':'+i.get('value', '') for i in ware_attributes])
            # assert sku_info != '', '得到的sku_info为空str!请检查!'

            _comment_content = item.get('commentData', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = self._wash_comment(comment=_comment_content)

            buyer_name = item.get('userNickName', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            # jd设置默认 购买量为1
            quantify = 1

            head_img = item.get('userImgURL', '')
            assert head_img != '', '得到的用户头像为空值!请检查!'
            head_img = 'https://' + head_img

            # 第一次评论图片
            _comment_img_list = item.get('pictureInfoList', [])
            if _comment_img_list != []:
                _comment_img_list = [{'img_url': img.get('largePicURL', '')} for img in _comment_img_list]

            '''追评'''
            append_comment = {}

            # star_level
            star_level = int(item.get('commentScore', '5'))

            if not filter_invalid_comment_content(_comment_content):
                continue

            comment = [{
                'comment': _comment_content,
                'comment_date': _comment_date,
                'sku_info': sku_info,
                'img_url_list': _comment_img_list,
                'star_level': star_level,
                'video': '',
            }]

            _comment_list.append({
                'buyer_name': buyer_name,  # 买家昵称
                'comment': comment,  # 评论内容
                'quantify': quantify,  # 评论数量
                'head_img': head_img,  # 头像
                'append_comment': append_comment,  # 追评
            })

        return _comment_list

    def _add_headers_cookies(self):
        # 测试发现得带cookies, 详细到cookies中的sid字符必须有
        # 先获取cookies
        _cookies = self.my_phantomjs.get_url_cookies_from_phantomjs_session(url='https://item.m.jd.com/')
        # self.my_lg.info(str(_cookies))
        self.headers.update({
            'cookie': _cookies,
        })

        return None

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/京东/comment/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _set_headers(self):
        self.headers = {
            'origin': 'https://item.m.jd.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
            'referer': 'https://item.m.jd.com/ware/view.action?wareId=5025518',
            'x-requested-with': 'XMLHttpRequest',
        }

    def _wash_comment(self, comment):
        '''
        清洗评论
        :param comment:
        :return:
        '''
        comment = re.compile(r'jd|\n|Jd|JD').sub('', comment)
        comment = re.compile('京东').sub('优秀网', comment)

        return comment

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
          ('type', '3'),        # '0' 全部评论 | '3' 好评
          ('isCurrentSku', 'false'),
        ]

        return _params

    def __del__(self):
        try:
            del self.my_lg
            del self.my_phantomjs
            del self.headers
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