# coding:utf-8

'''
@author = super_fazai
@File    : tmall_comment_parse.py
@Time    : 2018/4/11 09:51
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

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
    _get_sku_info_from_db_by_goods_id,
    wash_goods_comment,)

try:
    from celery_tasks import _get_tm_one_page_comment_info_task
except ImportError:
    pass

from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    _get_url_contain_params,
    get_random_pc_ua,
    get_random_headers,
    str_cookies_2_dict,
    get_random_phone_ua,)
from fzutils.time_utils import get_shanghai_time
from fzutils.common_utils import (
    wash_sensitive_info,
    json_2_dict,)
from fzutils.spider.crawler import Crawler
from fzutils.spider.fz_requests import Requests
from fzutils.celery_utils import (
    block_get_celery_async_results,
    get_current_all_celery_handled_results_list,)

class TmallCommentParse(Crawler):
    def __init__(self, logger=None):
        # TODO 老数据接口得附上登录cookies才可请求成功! 且具有时效性!
        # 登陆后的cookies
        self.login_cookies_dict = str_cookies_2_dict(TB_COOKIES)
        super(TmallCommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/天猫/comment/',
            
            is_use_driver=False,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
            driver_cookies=TB_COOKIES,)
        self.result_data = {}
        self.msg = ''
        self.page_size = '10'
        self.comment_page_switch_sleep_time = 1.5   # 评论下一页sleep time
        self.g_data = {}                # 临时数据
        self.max_page_num = 10

    def _get_comment_data(self, _type:int, goods_id):
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

        try:
            # 先获取到sellerId
            seller_id = self._get_seller_id(_type=type, goods_id=goods_id)
            self.lg.info('------>>>| 获取到的seller_id: {}'.format(seller_id))

            # 获取db sku_info list
            db_sku_info_list = _get_sku_info_from_db_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
            # pprint(db_sku_info_list)
        except (AssertionError, IndexError,):
            self.lg.error('遇到错误[goods_id:{}]:'.format(goods_id), exc_info=True)
            return self._data_error()

        except DBGetGoodsSkuInfoErrorException:
            self.lg.error('获取db goods_id: {} 的sku_info失败! 此处跳过!'.format(goods_id))
            return self._data_error()

        # 同步
        # all_comment_list = self._get_all_comment_list(
        #     goods_id=goods_id,
        #     seller_id=seller_id,
        #     _type=_type)
        # celery
        all_comment_list = self._get_all_comment_list_by_celery(
            goods_id=goods_id,
            seller_id=seller_id,
            _type=_type)
        # pprint(all_comment_list)

        try:
            _comment_list = self._get_comment_list(
                all_comment_list=all_comment_list,
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

    def _get_all_comment_list_by_celery(self, goods_id, seller_id, _type) -> list:
        """
        通过celery获取所有comment
        :param goods_id:
        :param seller_id:
        :param _type:
        :return:
        """
        tasks = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('create task[where goods_id: {}, page_num: {}]...'.format(goods_id, page_num))
            try:
                async_obj = self._create_tm_one_celery_task(
                    ip_pool_type=self.ip_pool_type,
                    goods_id=goods_id,
                    page_num=page_num,
                    cookies=self.login_cookies_dict,
                    page_size=self.page_size,
                    _type=_type,
                    seller_id=seller_id,
                )
                tasks.append(async_obj)
                # self.lg.info('async_obj: {}'.format(str(async_obj)))
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

        one_res = block_get_celery_async_results(tasks=tasks)
        # self.lg.info(str(one_res))
        all_comment_info_list = get_current_all_celery_handled_results_list(
            one_res=one_res,
            logger=self.lg)

        return all_comment_info_list

    def _create_tm_one_celery_task(self, **kwargs):
        """
        创建tm celery obj
        :param kwargs:
        :return:
        """
        ip_pool_type = kwargs['ip_pool_type']
        goods_id = kwargs['goods_id']
        page_num = kwargs['page_num']
        cookies = kwargs['cookies']
        page_size = kwargs['page_size']
        _type = kwargs['_type']
        seller_id = kwargs['seller_id']

        # 重新导入
        from celery_tasks import _get_tm_one_page_comment_info_task

        async_obj = _get_tm_one_page_comment_info_task.apply_async(
            args=[
                ip_pool_type,
                goods_id,
                _type,
                seller_id,
                page_num,
                page_size,
                cookies,
            ],
            expires=5 * 60,
            retry=False,
        )

        return async_obj

    def _get_all_comment_list(self, goods_id, seller_id, _type) -> list:
        """
        获取所有评论
        :param goods_id:
        :return:
        """
        all_comment_list = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第 {0} 页的评论...'.format(str(page_num)))
            try:
                data = self._get_one_page_comment_info(
                    goods_id=goods_id,
                    seller_id=seller_id,
                    page_num=page_num,
                    _type=_type)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            all_comment_list += data
            # 必须进行短期休眠 否则跳滑动验证码!
            sleep(self.comment_page_switch_sleep_time)

        return all_comment_list

    def _get_one_page_comment_info(self, goods_id, seller_id, page_num, _type) -> list:
        """
        获取单页comment info
        :return:
        """
        def _get_params(goods_id, seller_id, page_num, page_size):
            callback = '_DLP_2519_der_3_currentPage_{0}_pageSize_{1}_'.format(page_num, page_size)
            params = (
                ('itemId', goods_id),
                ('sellerId', seller_id),
                ('order', '3'),
                ('currentPage', str(page_num)),
                ('pageSize', page_size),
                ('callback', callback),
            )

            return params

        _url = 'https://rate.tmall.com/list_detail_rate.htm'
        headers = get_random_headers(
            connection_status_keep_alive=False,
            upgrade_insecure_requests=False,
            cache_control='', )
        headers.update({
            'referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(goods_id),
        })
        params = _get_params(
            goods_id=goods_id,
            seller_id=seller_id,
            page_num=page_num,
            page_size=self.page_size)
        # cookies必须! requests 请求无数据!
        body = Requests.get_url_body(
            url=_url,
            headers=headers,
            params=params,
            cookies=self.login_cookies_dict,
            ip_pool_type=self.ip_pool_type,)

        # 所以直接用phantomjs来获取相关api数据
        # _url = _get_url_contain_params(url=_url, params=params)
        # self.lg.info(_url)
        # body = self.driver.get_url_body(url=_url)
        # self.lg.info(str(body))
        assert body != '', '获取到的body为空str! 出错type:{0}, goods_id:{1}'.format(_type, goods_id)

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

    def _get_comment_list(self, all_comment_list, db_top_n_buyer_name_and_comment_date_list, db_sku_info_list):
        '''
        转换成需求的结果集
        :param all_comment_list:
        :return:
        '''
        _comment_list = []
        for item in all_comment_list:
            # pprint(item)
            _comment_date = self._get_comment_date(item=item)

            sku_info = item.get('auctionSku', '')
            # self.lg.info(sku_info)
            if sku_info == '':
                # 从所有规格里面随机一个
                sku_info = str(choice(db_sku_info_list))

            _comment_content = item.get('rateContent', '')
            assert _comment_content != '', '得到的评论内容为空str!请检查!'
            _comment_content = wash_goods_comment(comment_content=_comment_content)

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
                    'comment': wash_goods_comment(comment_content=_tmp_append_comment.get('content', '')),
                    'img_url_list': _append_comment_img_list,
                }
            else:
                append_comment = {}

            if not filter_invalid_comment_content(_comment_content):
                continue

            if not filter_crawled_comment_content(
                new_buyer_name=buyer_name,
                new_comment_date=_comment_date,
                db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,
                logger=self.lg):
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

    def _get_seller_id(self, _type, goods_id):
        '''
        得到seller_id
        :param type:
        :param goods_id:
        :return:
        '''
        # TODO 与更新脚本接口冲突
        # tmall = TmallParse(logger=self.lg)
        # _g = [_type, goods_id]
        # self.g_data = tmall.get_goods_data(goods_id=_g)
        # seller_id = str(self.g_data.get('seller', {}).get('userId', 0))
        # # self.lg.info('获取到的seller_id: ' + seller_id)
        # try:
        #     del tmall
        # except:
        #     pass

        # 方案2:
        headers = self._get_phone_headers()
        headers.update({
            'authority': 'detail.m.tmall.com',
        })
        # 测试发现: 必要字段_tb_token_, cookie2, t
        params = (
            ('id', goods_id),
        )
        # 处理天猫国际
        url = 'https://detail.m.tmall.com/item.htm' if _type != 2 else 'https://detail.m.tmall.hk/item.htm'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            cookies=self.login_cookies_dict)
        # self.lg.info(body)

        seller_id = '0'
        try:
            seller_id = str(re.compile('\"userId\":(\d+),').findall(body)[0])
        except (IndexError, Exception):
            pass
        # self.lg.info(seller_id)

        assert seller_id != '0', '获取到的seller_id为0!'

        return seller_id

    @staticmethod
    def _get_phone_headers():
        return {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        try:
            del self.lg
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
        data = tmall._get_comment_data(_type=int(_type), goods_id=goods_id)
        pprint(data)
        gc.collect()
