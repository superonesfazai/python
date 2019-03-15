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
    filter_crawled_comment_content,
    _get_sku_info_from_db_by_goods_id,
    wash_goods_comment,)
from my_exceptions import (
    SqlServerConnectionException,
    DBGetGoodsSkuInfoErrorException,)

try:
    from celery_tasks import _get_tb_one_page_comment_info_task
except ImportError:
    pass

from random import randint, choice
from time import sleep
from gc import collect
import re
from pprint import pprint
import requests

from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    get_random_pc_ua,
    str_cookies_2_dict,
    get_base_headers,)
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import get_shanghai_time
from fzutils.spider.crawler import Crawler
from fzutils.celery_utils import (
    block_get_celery_async_results,
    get_current_all_celery_handled_results_list,)

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
        self.comment_page_switch_sleep_time = 2   # 评论下一页sleep time
        self.db_random_head_img_url_list = []
        self.max_page_num = 10

    def _get_comment_data(self, goods_id):
        """
        获取comment数据
        :param goods_id:
        :return:
        """
        if goods_id == '':
            return self._data_error_init()

        self.lg.info('------>>>| 待抓取的goods_id: {}'.format(goods_id))
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._data_error_init()

        try:
            db_sku_info_list = _get_sku_info_from_db_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
        except DBGetGoodsSkuInfoErrorException:
            self.lg.error('获取db goods_id: {} 的sku_info失败! 此处跳过!'.format(goods_id))
            return self._data_error_init()

        # 同步
        # all_comment_list = self._get_all_comment_info(goods_id=goods_id)
        # celery
        all_comment_list = self._get_all_comment_info_by_celery(goods_id=goods_id)
        # pprint(all_comment_list)

        try:
            _comment_list = self._get_comment_list(
                all_comment_list=all_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list,
                db_sku_info_list=db_sku_info_list)
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

    def _get_all_comment_info_by_celery(self, goods_id) -> list:
        """
        通过celery 获取某个goods_id所有的comment
        :param goods_id:
        :return:
        """
        tasks = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('create task[where goods_id: {}, page_num: {}]...'.format(goods_id, page_num))
            try:
                async_obj = self._create_tb_one_celery_task(
                    ip_pool_type=self.ip_pool_type,
                    goods_id=goods_id,
                    page_num=page_num,
                    cookies=self.login_cookies_dict,
                )
                tasks.append(async_obj)
            except:
                continue

        one_res = block_get_celery_async_results(tasks=tasks)
        all_comment_info_list = get_current_all_celery_handled_results_list(
            one_res=one_res,
            logger=self.lg)

        return all_comment_info_list

    def _get_all_comment_info(self, goods_id) -> list:
        """
        获取某个goods_id所有评论数据
        :param goods_id:
        :return:
        """
        all_comment_list = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第 {} 页评论...'.format(page_num))
            try:
                data = self._get_one_page_comment_info(page_num=page_num, goods_id=goods_id)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            all_comment_list += data
            sleep(self.comment_page_switch_sleep_time)

        return all_comment_list

    def _create_tb_one_celery_task(self, **kwargs):
        """
        创建一个tb celery task
        :param kwargs:
        :return:
        """
        ip_pool_type = kwargs['ip_pool_type']
        goods_id = kwargs['goods_id']
        page_num = kwargs['page_num']
        cookies = kwargs['cookies']

        async_obj = _get_tb_one_page_comment_info_task.apply_async(
            args=[
                ip_pool_type,
                goods_id,
                page_num,
                cookies,
            ],
            expires=5 * 60,
            retry=False,
        )

        return async_obj

    def _get_one_page_comment_info(self, page_num, goods_id) -> list:
        """
        获取单页评论页面信息
        :param page_num:
        :param goods_id:
        :return:
        """
        def _get_params(goods_id, page_num) -> tuple:
            return (
                ('auctionNumId', goods_id),
                # ('userNumId', '1681172037'),
                ('currentPageNum', str(page_num)),
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

        headers = get_base_headers()
        headers.update({
            'authority': 'rate.taobao.com',
            'referer': 'https://item.taobao.com/item.htm?id={}'.format(goods_id)
        })
        url = 'https://rate.taobao.com/feedRateList.htm'
        _params = _get_params(goods_id=goods_id, page_num=page_num)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
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

    def _get_comment_list(self, all_comment_list, db_top_n_buyer_name_and_comment_date_list, db_sku_info_list):
        '''
        转化成需要的结果集
        :param all_comment_list:
        :return:
        '''
        _comment_list = []
        _sku_info_list = []  # 用于存已有的规格
        for item in all_comment_list:
            comment_date = self._get_comment_date(item=item)
            sku_info = self._get_sku_info(item=item, db_sku_info_list=db_sku_info_list)

            # 评论照片
            img_url_list = item.get('photos', [])
            img_url_list = [{
                'img_url': 'https:' + _i.get('url', '')
            } for _i in img_url_list if _i.get('url', '') != '']

            _comment_content = item.get('content', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = wash_goods_comment(comment_content=_comment_content)

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
                db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,
                logger=self.lg):
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

    def _get_sku_info(self, item, db_sku_info_list) -> str:
        """
        获取sku_info
        :param item:
        :return:
        """
        sku_info = item.get('auction', {}).get('sku', '')
        # self.lg.info(sku_info)
        if sku_info == '':
            sku_info = choice(db_sku_info_list)
        else:
            sku_info = self._wash_sku_info(sku_info)

        return sku_info

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
            _res = requests.get(url=url, headers=get_base_headers(), proxies=tmp_proxies)
            self.lg.info(str(_res.url))
            if _res.url == 'https://gw.alicdn.com/tps/i3/TB1yeWeIFXXXXX5XFXXuAZJYXXX-210-210.png_40x40.jpg':
                return True
            else:
                return False
        except:
            self.lg.info('检测图片地址时网络错误! 跳过!')
            return False

    def _wash_sku_info(self, sku_info):
        sku_info = sku_info.replace('&nbsp;', ' ').replace('&nbsp', ' ')

        return sku_info

    def _get_comment_date(self, item):
        '''
        将格式如:2017年12月07日 14:50 转换为 '2017-12-07 14:50:00'
        :param comment_date:
        :return:
        '''
        comment_date = item.get('date', '')
        assert comment_date != '', '得到的comment_date为空str!请检查!'

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