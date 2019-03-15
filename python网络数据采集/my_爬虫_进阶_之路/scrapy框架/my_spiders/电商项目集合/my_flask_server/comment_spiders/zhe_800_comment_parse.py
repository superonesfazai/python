# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_comment_parse.py
@Time    : 2018/5/4 10:27
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

try:
    from celery_tasks import _get_z8_one_page_comment_info_task
except ImportError:
    pass

from my_items import CommentItem
from settings import (
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)

from random import randint
from time import sleep
import gc
import re
from datetime import timedelta
from pprint import pprint
from my_exceptions import (
    NoNextPageException,
    SqlServerConnectionException,)
from multiplex_code import (
    get_top_n_buyer_name_and_comment_date_by_goods_id,
    filter_crawled_comment_content,
    wash_goods_comment,)

from fzutils.time_utils import (
    get_shanghai_time,
    date_parse,
    string_to_datetime,)
from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_base_headers,)
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict
from fzutils.spider.crawler import Crawler
from fzutils.celery_utils import (
    block_get_celery_async_results,
    get_current_all_celery_handled_results_list,)

class Zhe800CommentParse(Crawler):
    def __init__(self, logger=None):
        super(Zhe800CommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/折800/comment/',
        )
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        self.page_size = '20'  # 固定值
        self.comment_page_switch_sleep_time = 1.5  # 评论下一页sleep time
        self.max_page_num = 8

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            return self._data_error()

        self.lg.info('------>>>| 待抓取的goods_id: {}'.format(goods_id))
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._data_error()

        # 同步
        # all_comment_list = self._get_all_comment_info(goods_id=goods_id)
        # celery
        all_comment_list = self._get_all_comment_info_by_celery(goods_id=goods_id)

        # self.lg.info(str(len(all_comment_list)))
        try:
            _comment_list = self._get_comment_list(
                all_comment_list=all_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list)
        except Exception as e:
            self.lg.error('出错goods_id: ' + goods_id)
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

    def _get_all_comment_info_by_celery(self, goods_id) -> list:
        """
        通过celery 获取所有comment info
        :param goods_id:
        :return:
        """
        # 用celery就不管是否有下一页了has_next_page
        tasks = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('create task[where goods_id: {}, page_num: {}]...'.format(goods_id, page_num))
            try:
                async_obj = self._create_z8_one_celery_task(
                    ip_pool_type=self.ip_pool_type,
                    goods_id=goods_id,
                    page_num=page_num,
                    page_size=self.page_size,
                )
                tasks.append(async_obj)
            except:
                continue

        one_res = block_get_celery_async_results(tasks=tasks)
        all_comment_info_list = get_current_all_celery_handled_results_list(
            one_res=one_res,
            logger=self.lg)

        return all_comment_info_list

    def _create_z8_one_celery_task(self, **kwargs):
        """
        创建celery obj
        :param kwargs:
        :return:
        """
        ip_pool_type = kwargs['ip_pool_type']
        goods_id = kwargs['goods_id']
        page_num = kwargs['page_num']
        page_size = kwargs['page_size']

        async_obj = _get_z8_one_page_comment_info_task.apply_async(
            args=[
                ip_pool_type,
                goods_id,
                page_num,
                page_size,
            ],
            expires=5 * 60,
            retry=False,
        )

        return async_obj

    def _get_all_comment_info(self, goods_id) -> list:
        """
        获取所有comment info
        :param goods_id:
        :return:
        """
        # 下面是抓取m.zhe800.com的数据地址
        all_comment_list = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第{}页评论...'.format(page_num))
            try:
                data, has_next_page = self._get_one_page_comment_info(
                    page_num=page_num,
                    goods_id=goods_id)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            all_comment_list += data
            if not has_next_page:
                # 必须放在add data后面，否则会导致当前页面没被add, 就跳出
                break

            sleep(self.comment_page_switch_sleep_time)

        return all_comment_list

    def _get_one_page_comment_info(self, page_num, goods_id) -> tuple:
        """
        获取单页comment info
        :return:
        """
        def _get_params(goods_id, page_num, page_size):
            params = (
                ('productId', str(goods_id)),
                ('tagId', ''),
                ('page', str(page_num)),
                ('perPage', page_size),
            )

            return params
        
        tmp_url = 'https://th5.m.zhe800.com/app/detail/comment/list'
        headers = get_base_headers()
        headers.update({
            'referer': 'https://th5.m.zhe800.com/h5/comment/list?zid={0}&dealId=39890410&tagId='.format(str(goods_id))
        })
        params = _get_params(
            goods_id=goods_id,
            page_num=page_num,
            page_size=self.page_size,
        )
        body = Requests.get_url_body(
            url=tmp_url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={})
        # pprint(data)
        assert data.get('comments') is not None\
            and data.get('hasNext') is not None, '获取到的data为None, 出错goods_id: {}'.format(goods_id)

        # 判断是否下页还有评论信息
        # <class 'bool'>
        has_next_page = data.get('hasNext', False)
        data = data.get('comments', [])
        self.lg.info('[{}] page_num: {}'.format(
            '+' if data != [] else '-',
            page_num,))

        return data, has_next_page

    def _data_error(self):
        self.result_data = {}

        return {}

    def _get_comment_list(self, all_comment_list, db_top_n_buyer_name_and_comment_date_list):
        '''
        获取规范化的comment结果集
        :param all_comment_list:
        :return:
        '''
        _comment_list = []
        for item in all_comment_list:
            comment_date = self._get_comment_date(item=item)

            buyer_name = item.get('nickname', '')
            assert buyer_name != '', '得到的用户昵称为空值!请检查!'

            _comment_content = item.get('content', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = wash_goods_comment(comment_content=_comment_content)

            sku_info = item.get('skuDesc', '')
            # self.lg.info(sku_info)
            # 存在规格为空的
            # assert sku_info != '', '得到的sku_info为空str!请检查!'
            sku_info = self._wash_sku_info(sku_info)

            # 第一次评论照片
            img_url_list = item.get('firstEvidences', [])
            # self.lg.info(img_url_list)
            if img_url_list is None:
                img_url_list = []
            else:
                img_url_list = [{
                    'img_url': _i.get('big', '')
                } for _i in img_url_list]

            '''追评'''
            append_comment = {}
            append_comment_date = item.get('appendTime', '')
            append_comment_date = self._get_append_comment_date(append_comment_date, comment_date)
            if append_comment_date == '':    # 追评时间为空即表示无追评
                pass
            else:
                _tmp_append_comment_content = item.get('append', '')
                # 追评的图片
                _append_comment_img_list = [{'img_url': img.get('big', '')} for img in item.get('appendEvidences')] if item.get('appendEvidences') is not None else []
                # self.lg.info(_append_comment_img_list)

                append_comment = {
                    'comment_date': append_comment_date,
                    'comment': wash_goods_comment(comment_content=_tmp_append_comment_content),
                    'img_url_list': _append_comment_img_list,
                }

            # 购买数量, 随机
            quantify = randint(1, 2)
            # 用户头像, 默认留空
            head_img = ''
            # 评论星级
            star_level = int(item.get('levelStar', 5))
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
                'star_level': star_level,
                'video': '',
            }]
            _ = {
                'buyer_name': buyer_name,  # 买家昵称
                'comment': comment,  # 评论内容
                'quantify': quantify,  # 购买数量
                'head_img': head_img,  # 头像
                'append_comment': append_comment,  # 追评
            }

            _comment_list.append(_)

        return _comment_list

    def _get_append_comment_date(self, append_comment_date, comment_date) -> str:
        """
        获取并处理追评时间点
        :return:
        """
        # 处理append_comment_date值为n天后追评, or 当天追评
        if re.compile('追评').findall(append_comment_date) != []:
            add_days = re.compile('(\d+)天后').findall(append_comment_date)
            if re.compile('当天').findall(append_comment_date) != []:
                append_comment_date = comment_date
            elif add_days != []:
                append_comment_date = str(string_to_datetime(comment_date) + timedelta(days=int(add_days[0])))
            else:
                raise ValueError('未知append_comment_date: {}'.format(append_comment_date))
        else:
            pass

        return str(append_comment_date)

    def _get_comment_date(self, item) -> str:
        '''
        得到规范化的时间信息
        :param comment_date:
        :return: str 格式: 2017-05-26 09:00:00
        '''
        comment_date = item.get('createTime', '')
        assert comment_date != '', '得到的comment_date为空str!请检查!'
        # self.lg.info(comment_date)
        # datetime.datetime(2019, 2, 25, 0, 0)
        comment_date = str(date_parse(target_date_str=comment_date))

        return comment_date

    def _wash_sku_info(self, sku_info):
        sku_info = sku_info.replace('&nbsp;', ' ').replace('&nbsp', ' ')
        sku_info = re.compile('zhe800|折800|ZHE800').sub('', sku_info)

        return sku_info

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    taobao = Zhe800CommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        taobao._get_comment_data(goods_id=goods_id)

        gc.collect()