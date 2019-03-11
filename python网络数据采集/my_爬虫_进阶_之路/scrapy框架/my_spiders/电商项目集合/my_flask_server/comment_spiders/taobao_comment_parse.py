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
from settings import (
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,
    TB_COOKIES,)
from multiplex_code import (
    _get_random_head_img_url_from_db,
    get_top_n_buyer_name_and_comment_date_by_goods_id,
    filter_crawled_comment_content,)
from my_exceptions import SqlServerConnectionException

from random import randint
from time import sleep
from gc import collect
import re
from pprint import pprint
import requests

from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    get_random_pc_ua,
    str_cookies_2_dict,)
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import get_shanghai_time
from fzutils.spider.crawler import Crawler

class TaoBaoCommentParse(Crawler):
    def __init__(self, logger=None):
        # TODO 下面抓取的是pc端的数据地址(新版pc被重定向到登陆页, 强制登陆, 可以带上登录cookies请求!) 也可以抓取h5站点的在mtop.taobao.rate.detaillist.get接口里面, 有签名
        # cookies = None
        # x5sec 字段必须有
        cookies = TB_COOKIES
        self.login_cookies_dict = str_cookies_2_dict(cookies) if cookies is not None else None
        super(TaoBaoCommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/comment/',
        )
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self.comment_page_switch_sleep_time = 2   # 评论下一页sleep time
        self.db_random_head_img_url_list = []
        self.max_page_num = 8

    def _get_comment_data(self, goods_id):
        """
        获取comment数据
        :param goods_id:
        :return:
        """
        if goods_id == '':
            return self._data_error_init()

        _tmp_comment_list = []
        self.lg.info('------>>>| 待抓取的goods_id: {}'.format(goods_id))
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                top_n_num=400,
                logger=self.lg,)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._data_error_init()

        # 获取评论数据
        for current_page_num in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第 {} 页评论...'.format(current_page_num))
            try:
                data = self._get_one_page_comment_info(page_num=current_page_num, goods_id=goods_id)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            _tmp_comment_list += data
            sleep(self.comment_page_switch_sleep_time)

        # self.lg.info(str(len(_tmp_comment_list)))
        try:
            _comment_list = self._get_comment_list(
                _tmp_comment_list=_tmp_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list)
        except Exception as e:
            self.lg.error('出错goods_id: ' + goods_id)
            self.lg.exception(e)
            return self._data_error_init()

        _t = get_shanghai_time()

        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        # pprint(self.result_data)

        return self.result_data

    def _get_one_page_comment_info(self, page_num, goods_id) -> list:
        """
        获取单页评论页面信息
        :param page_num:
        :param goods_id:
        :return:
        """
        tmp_url = 'https://rate.taobao.com/feedRateList.htm'
        _params = self._set_params(current_page_num=page_num, goods_id=goods_id)

        self.headers.update({
            'referer': 'https://item.taobao.com/item.htm?id=' + goods_id
        })
        body = Requests.get_url_body(
            url=tmp_url,
            headers=self.headers,
            params=_params,
            encoding='gbk',
            ip_pool_type=self.ip_pool_type,
            cookies=self.login_cookies_dict,)
        # self.lg.info(str(body))

        try:
            body = re.compile('\((.*)\)').findall(body)[0]
        except IndexError:
            sleep(.5)
            raise IndexError('re得到需求body时出错! 出错goods_id: ' + goods_id)

        data = json_2_dict(json_str=body, logger=self.lg).get('comments')
        # pprint(data)
        if data is None:
            assert data is not None, '出错goods_id: ' + goods_id

        self.lg.info('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num, ))
        # assert data != [], '该页的"comments"=[], 跳出本次循环!'

        return data

    def _get_comment_list(self, _tmp_comment_list, db_top_n_buyer_name_and_comment_date_list):
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
            # self.lg.info(sku_info)
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
            head_img = self._get_head_img_url(item=item)

            ori_video_info = item.get('video', {}) if item.get('video') is not None else {}
            video_url = ori_video_info.get('cloudVideoUrl', '')
            video_url = 'https:' + video_url if video_url != '' else ''

            if not filter_invalid_comment_content(_comment_content):
                continue

            if not filter_crawled_comment_content(
                new_buyer_name=buyer_name,
                new_comment_date=comment_date,
                db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,):
                # 过滤已采集的comment
                continue

            comment = [{
                'comment': _comment_content,
                'comment_date': comment_date,
                'sku_info': sku_info,
                'img_url_list': img_url_list,
                'star_level': randint(4, 5),
                'video': video_url,
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

    def _get_head_img_url(self, item):
        """
        获取头像url
        :param item:
        :return:
        """
        # 未赋值则先进行赋值!
        self.db_random_head_img_url_list = _get_random_head_img_url_from_db(
            need_head_img_num=30,
            logger=self.lg) \
            if self.db_random_head_img_url_list == [] else self.db_random_head_img_url_list
        tmp_head_img = item.get('user', {}).get('avatar', '')
        head_img = ''
        if re.compile(r'/default/avatar-40.png').findall(tmp_head_img) != []:
            pass

        # # 无法识别是否为同一张图 只能先拿到这种规律的然后请求图片看齐地址
        # elif re.compile(r'vGNuOHcWv88YXF').findall(tmp_head_img) != []:
        #     # self.lg.info('https:' + tmp_head_img)
        #     if self._judge_is_taobao_head_img(url='https:' + tmp_head_img):
        #         self.lg.info('https:' + tmp_head_img)
        #         pass
        #     else:
        #         head_img = 'https:' + tmp_head_img

        elif tmp_head_img != '//wwc.alicdn.com/avatar/getAvatar.do?userIdStr=vGNuOHcWv88YXF-HPmvbM07HvG8SvFI0Xm7Hvm80MkZhvkk0XmcSPFPhPHQWOmvG&width=40&height=40&type=sns' \
                or tmp_head_img != '//gw.alicdn.com/tps/i3/TB1yeWeIFXXXXX5XFXXuAZJYXXX-210-210.png_40x40.jpg':
            head_img = 'https:' + tmp_head_img

        else:
            pass

        # 处理宽高40,40 变成150,150
        head_img = head_img.replace('width=40', 'width=150').replace('height=40', 'height=150') \
            if head_img != '' else ''

        if head_img == '':
            # 为空则从db中随机获取一张
            try:
                head_img = self.db_random_head_img_url_list[randint(0, len(self.db_random_head_img_url_list)-1)]
            except IndexError:
                pass

        return head_img

    def _data_error_init(self):
        self.result_data = {}

        return {}

    def _judge_is_taobao_head_img(self, url):
        '''
        判断是否为淘宝默认头像地址
        :param url:
        :return:
        '''
        tmp_proxies = Requests._get_proxies(ip_pool_type=self.ip_pool_type)

        try:
            _res = requests.get(url=url, headers=self.headers, proxies=tmp_proxies)
            self.lg.info(str(_res.url))
            if _res.url == 'https://gw.alicdn.com/tps/i3/TB1yeWeIFXXXXX5XFXXuAZJYXXX-210-210.png_40x40.jpg':
                return True
            else:
                return False
        except:
            self.lg.info('检测图片地址时网络错误! 跳过!')
            return False

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
            del self.lg
        except:
            pass
        collect()

if __name__ == '__main__':
    taobao = TaoBaoCommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        taobao._get_comment_data(goods_id=goods_id)

        collect()