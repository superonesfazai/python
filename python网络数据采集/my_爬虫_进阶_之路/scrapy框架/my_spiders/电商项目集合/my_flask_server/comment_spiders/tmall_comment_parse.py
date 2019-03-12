# coding:utf-8

'''
@author = super_fazai
@File    : tmall_comment_parse.py
@Time    : 2018/4/11 09:51
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse_2 import TmallParse
from taobao_parse import TaoBaoLoginAndParse
from my_items import CommentItem
from settings import (
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,
    TB_COOKIES,)

from random import randint
from time import sleep
import gc
import re
from pprint import pprint
from random import choice
from my_exceptions import (
    SqlServerConnectionException,
    DBGetGoodsSkuInfoErrorException,)
from multiplex_code import (
    get_top_n_buyer_name_and_comment_date_by_goods_id,
    filter_crawled_comment_content,
    _get_sku_info_from_db_by_goods_id,)

from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    _get_url_contain_params,
    get_random_pc_ua,)
from fzutils.time_utils import get_shanghai_time
from fzutils.common_utils import (
    wash_sensitive_info,
    json_2_dict,)
from fzutils.spider.crawler import Crawler

class TmallCommentParse(Crawler):
    def __init__(self, logger=None):
        # TODO 老数据接口得附上登录cookies才可请求成功! 且具有时效性!
        # 登陆后的cookies
        cookies = TB_COOKIES
        super(TmallCommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/天猫/comment/',
            
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
            driver_cookies=cookies,)
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self.page_size = '10'
        self.comment_page_switch_sleep_time = 1.5   # 评论下一页sleep time
        self.g_data = {}                # 临时数据
        self.max_page_num = 10

    def _get_comment_data(self, type:int, goods_id):
        """
        获取对应goods_id的评论数据
        :param type:
        :param goods_id:
        :return:
        """
        if goods_id == '' or type == '':
            return self._data_error()

        self.lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
            # pprint(db_top_n_buyer_name_and_comment_date_list)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._data_error()

        '''先获取到sellerId'''
        try:
            seller_id = self._get_seller_id(type=type, goods_id=goods_id)
            self.lg.info('------>>>| 获取到的seller_id: {}'.format(seller_id))
        except AssertionError or IndexError:
            self.lg.error('遇到错误[goods_id:{}]:'.format(goods_id), exc_info=True)
            return self._data_error()

        # 获取db sku_info list
        try:
            db_sku_info_list = _get_sku_info_from_db_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
        except DBGetGoodsSkuInfoErrorException:
            self.lg.error('获取db goods_id: {} 的sku_info失败! 此处跳过!'.format(goods_id))
            return self._data_error()

        _tmp_comment_list = []
        for current_page in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第 {0} 页的评论...'.format(str(current_page)))
            try:
                data = self._get_one_page_comment_info(
                    goods_id=goods_id,
                    seller_id=seller_id,
                    page_num=current_page)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            _tmp_comment_list += data
            # 必须进行短期休眠 否则跳滑动验证码!
            sleep(self.comment_page_switch_sleep_time)

        try:
            _comment_list = self._get_comment_list(
                _tmp_comment_list=_tmp_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list,
                db_sku_info_list=db_sku_info_list)
        except Exception as e:
            self.lg.error('出错type:{0}, goods_id:{1}'.format(str(type), goods_id))
            self.lg.exception(e)
            return self._data_error()

        _t = get_shanghai_time()
        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        # pprint(self.result_data)

        return self.result_data

    def _get_one_page_comment_info(self, goods_id, seller_id, page_num) -> list:
        """
        获取单页comment info
        :return:
        """
        _url = 'https://rate.tmall.com/list_detail_rate.htm'
        params = self._set_params(
            goods_id=goods_id,
            seller_id=seller_id,
            current_page=page_num)
        self.headers.update({
            'referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(goods_id),
        })

        # 原先用代理请求不到数据的原因是没有cookies
        # body = MyRequests.get_url_body(url=_url, headers=self.headers, params=params, encoding='gbk')
        # 所以直接用phantomjs来获取相关api数据
        _url = _get_url_contain_params(url=_url, params=params)  # 根据params组合得到url
        # self.lg.info(_url)
        body = self.driver.get_url_body(url=_url)
        # self.lg.info(str(body))
        assert body != '', '获取到的body为空str! 出错type:{0}, goods_id:{1}'.format(str(type), goods_id)

        try:
            data = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                default_res={},
                logger=self.lg,)
            redict_url = 'https:' + data.get('url', '').replace('https:', '') if data.get('url', '') != '' else ''
            if redict_url != '':
                self.lg.info(redict_url)
            else:
                pass

            data = data.get('rateDetail', {}).get('rateList', [])
        except IndexError:
            raise IndexError

        self.lg.info('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num, ))

        return data

    def _data_error(self):
        self.result_data = {}

        return {}

    def _get_comment_list(self, _tmp_comment_list, db_top_n_buyer_name_and_comment_date_list, db_sku_info_list):
        '''
        转换成需求的结果集
        :param _tmp_comment_list:
        :return:
        '''
        _comment_list = []
        for item in _tmp_comment_list:
            # pprint(item)
            _comment_date = self._get_comment_date(item=item)

            # 天猫接口拿到的sku_info默认为空
            # sku_info = ''
            # 从所有规格里面随机一个
            sku_info = str(choice(db_sku_info_list))

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
            _tmp_append_comment = item.get('appendComment', {}) if item.get('appendComment') is not None else {}
            # 追评的图片
            # pprint(_tmp_append_comment)
            _append_comment_img_list = _tmp_append_comment.get('pics', []) if _tmp_append_comment.get('pics', '') != '' else []
            if _append_comment_img_list != []:
                _append_comment_img_list = [{'img_url': 'https:' + img} for img in _append_comment_img_list]

            if _tmp_append_comment != {}:
                append_comment = {
                    'comment_date': _tmp_append_comment.get('commentTime', ''),
                    'comment': self._wash_comment(_tmp_append_comment.get('content', '')),
                    'img_url_list': _append_comment_img_list,
                }
            else:
                append_comment = {}

            if not filter_invalid_comment_content(_comment_content):
                continue

            if not filter_crawled_comment_content(
                new_buyer_name=buyer_name,
                new_comment_date=_comment_date,
                db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,):
                # 过滤已采集的comment
                continue

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

    def _get_comment_date(self, item):
        """
        获取comment date
        :param item:
        :return: eg: '2017-04-24 13:41:37'
        """
        _comment_date = item.get('rateDate', '')
        assert _comment_date != '', '得到的_comment_date为空str!请检查!'

        return _comment_date

    def _get_seller_id(self, type, goods_id):
        '''
        得到seller_id
        :param type:
        :param goods_id:
        :return:
        '''
        _ = TmallParse(logger=self.lg)
        _g = [type, goods_id]
        self.g_data = _.get_goods_data(goods_id=_g)
        seller_id = str(self.g_data.get('seller', {}).get('userId', 0))
        # self.lg.info('获取到的seller_id: ' + seller_id)
        try:
            del _
        except:
            pass
        assert seller_id != 0, '获取到的seller_id为0!'

        return seller_id

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'referer': 'https://detail.m.tmall.com/item.htm?id=524718632348',
        }

    def _wash_comment(self, comment):
        '''
        清洗评论
        :param comment:
        :return:
        '''
        add_sensitive_str_list = [
            '天猫超市',
            '天猫国际',
            '天猫全球购',
            '天猫大药房',
            '某淘',
            '某宝',
            '天猫',
            '淘宝',
            'tmall',
            'Tmall',
            'TMALL',
            'TAOBAO',
            'taobao',
        ]
        comment = wash_sensitive_info(
            data=comment,
            add_sensitive_str_list=add_sensitive_str_list
        )

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
            del self.lg
            del self.driver
            del self.g_data
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    tmall = TmallCommentParse()
    while True:
        _type = input('请输入要爬取的商品type(以英文分号结束: 0常规|1超市|2天猫国际): ')
        _type = _type.strip('\n').strip(';')
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        data = tmall._get_comment_data(type=int(_type), goods_id=goods_id)
        pprint(data)
        gc.collect()
