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
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)

from time import sleep
import gc
import re
import datetime
from pprint import pprint
from multiplex_code import (
    get_top_n_buyer_name_and_comment_date_by_goods_id,
    filter_crawled_comment_content,)
from my_exceptions import SqlServerConnectionException
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)
from fzutils.spider.fz_requests import Requests
from fzutils.time_utils import get_shanghai_time
from fzutils.common_utils import json_2_dict
from fzutils.spider.crawler import Crawler

class JdCommentParse(Crawler):
    def __init__(self, logger=None):
        super(JdCommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/jd/comment/',
            
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,)
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self.comment_page_switch_sleep_time = 1.2  # 评论下一页sleep time
        self._add_headers_cookies()

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            return self._data_error()

        self.lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                top_n_num=400,
                logger=self.lg,)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._data_error()

        # 根据京东手机版商品评价获取
        _tmp_comment_list = []
        for current_page in range(1, 4):
            try:
                _data = self._get_one_page_comment_info(
                    goods_id=goods_id,
                    page_num=current_page,)
            except (AssertionError, Exception):
                self.lg.error('遇到错误:', exc_info=True)
                continue

            _tmp_comment_list += _data
            sleep(self.comment_page_switch_sleep_time)

        # pprint(_tmp_comment_list)
        try:
            _comment_list = self._get_comment_list(
                _tmp_comment_list=_tmp_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list,)
        except Exception:
            self.lg.error('出错goods_id:{0}'.format(goods_id), exc_info=True)
            return self._data_error()

        _t = get_shanghai_time()
        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        pprint(self.result_data)

        return self.result_data

    def _data_error(self):
        self.result_data = {}

        return {}

    def _get_one_page_comment_info(self, goods_id, page_num) -> list:
        """
        获取单页comment info
        :return:
        """
        headers = {
            'Referer': 'https://item.m.jd.com/product/{}.html'.format(goods_id),
            'User-Agent': get_random_phone_ua(),
        }
        params = (
            # ('callback', 'skuJDEvalA'),
            ('sorttype', '5'),
            ('pagesize', '10'),
            ('sceneval', '2'),
            ('score', '3'),                 # 取好评的
            ('sku', str(goods_id)),
            ('page', str(page_num)),
            # ('t', '0.7175421988280679'),
        )
        url = 'https://wq.jd.com/commodity/comment/getcommentlist'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,)
        # self.lg.info(body)
        assert body != '', 'body不为空值!'
        data = []
        try:
            data = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                default_res={}).get('result', {}).get('comments', [])
        except IndexError:
            pass
        # pprint(data)
        self.lg.info('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num,))
        # assert data != [], 'data不为空list! 出错goods_id: {}'.format(goods_id)

        return data

    def _get_comment_list(self, _tmp_comment_list, db_top_n_buyer_name_and_comment_date_list):
        '''
        转换成需求的结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        for item in _tmp_comment_list:
            _comment_date = self._get_comment_date(item=item)

            # sku_info(有些商品评论是没有规格的所以默认为空即可，不加assert检查!)
            # eg: '颜域品牌女装2017冬季新品娃娃领加厚格纹绣花毛呢外套中长款大衣04W7135 黑色 M/38'
            ware_attributes = item.get('referenceName', '')
            # self.lg.info(str(ware_attributes))
            sku_info = ' '.join(ware_attributes.split(' ')[1:])
            # assert sku_info != '', '得到的sku_info为空str!请检查!'

            _comment_content = item.get('content', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = self._wash_comment(comment=_comment_content)

            buyer_name = item.get('nickname', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            # jd设置默认 购买量为1
            quantify = 1
            head_img = self._get_head_img_url(item=item)

            # 第一次评论图片
            _comment_img_list = item.get('images', [])
            if _comment_img_list != []:
                _comment_img_list = [{
                    'img_url': img.get('imgUrl', '').replace('s128x96_jfs', 'jfs'),     # 小图换成大图!
                } for img in _comment_img_list]

            '''追评'''
            append_comment = {}
            # star_level
            star_level = int(item.get('score', '5'))

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
            if not filter_crawled_comment_content(
                new_buyer_name=buyer_name,
                new_comment_date=_comment_date,
                db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,):
                # 过滤已采集的comment
                continue

            _comment_list.append({
                'buyer_name': buyer_name,  # 买家昵称
                'comment': comment,  # 评论内容
                'quantify': quantify,  # 评论数量
                'head_img': head_img,  # 头像
                'append_comment': append_comment,  # 追评
            })

        return _comment_list

    def _get_head_img_url(self, item) -> str:
        """
        获取头像地址
        :param item:
        :return:
        """
        # 很多都是无图的
        head_img = item.get('userImageUrl', '')
        assert head_img != '', '得到的用户头像为空值!请检查!'
        # _sma -> _big 小图换大图!
        if head_img != 'misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg':
            head_img = 'https://' + head_img.replace('_sma', '_big')
        else:
            head_img = ''

        return head_img

    def _get_comment_date(self, item) -> str:
        """
        获取comment date
        :param item:
        :return: eg: '2018-02-11 21:54:37'
        """
        _comment_date = item.get('creationTime', '')
        assert _comment_date != '', '得到的_comment_date为空str!请检查!'

        return _comment_date

    def _add_headers_cookies(self):
        # 测试发现得带cookies, 详细到cookies中的sid字符必须有
        # 先获取cookies
        _cookies = self.driver.get_url_cookies_from_phantomjs_session(url='https://item.m.jd.com/')
        # self.lg.info(str(_cookies))
        self.headers.update({
            'cookie': _cookies,
        })

        return None

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
            del self.lg
            del self.driver
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