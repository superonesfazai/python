# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_comment_parse.py
@Time    : 2018/4/9 12:46
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

from random import (
    randint,
    choice,
)

import gc
from time import sleep
import re
from pprint import pprint
from json import dumps

try:
    from celery_tasks import _get_al_one_page_comment_info_task
except ImportError:
    pass

from my_exceptions import (
    SqlServerConnectionException,
    DBGetGoodsSkuInfoErrorException,)
from multiplex_code import (
    get_top_n_buyer_name_and_comment_date_by_goods_id,
    filter_crawled_comment_content,
    _get_sku_info_from_db_by_goods_id,
    wash_goods_comment,)

from fzutils.cp_utils import filter_invalid_comment_content
from fzutils.internet_utils import (
    get_random_pc_ua,
    str_cookies_2_dict,
    get_base_headers,)
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import (
    json_2_dict,
    get_random_int_number,)
from fzutils.spider.crawler import Crawler
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,)
from fzutils.celery_utils import (
    block_get_celery_async_results,
    get_current_all_celery_handled_results_list,)

class ALi1688CommentParse(Crawler):
    '''
    阿里1688评论抓取解析类
    '''
    def __init__(self, logger=None):
        # TODO 1688评论数据需要带上cookies进行请求
        cookies = TB_COOKIES
        self.login_cookies_dict = str_cookies_2_dict(cookies) if cookies is not None else None
        super(ALi1688CommentParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/1688/comment/',

            is_use_driver=False,
            driver_executable_path=PHANTOMJS_DRIVER_PATH,
            driver_cookies=cookies)
        self.result_data = {}
        self.msg = ''
        self._set_headers()
        # 可动态执行的代码
        self._exec_code = '''
        _text = str(self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').text)
        print(_text)
        assert _text != '四五星(0)', 'my assert error!'    # 通过断言来跳过执行下面的代码

        # 单个element老是定位不到, 就用elements
        # self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').click() 
        self.driver.find_elements_by_css_selector('div.tab-item')[1].click()
        # if _text == '四五星(0)':
        sleep(3)
        
        # 向下滚动10000像素
        js = 'document.body.scrollTop=10000'
        self.driver.execute_script(js)  # 每划一次，就刷6条
        sleep(4)
        '''
        self._page_sleep_time = 2
        self.max_page = 4
        self.max_page_num = 5

    def _get_comment_data(self, goods_id):
        if goods_id == '':
            self.result_data = {}
            return {}
        self.lg.info('------>>>| 待处理的goods_id为: %s' % str(goods_id))

        '''改版抓取m站接口, 分析js源码: 已破解1688 m站 get必须参数_csrf的加密方式'''
        # 即从https://m.1688.com/page/offerRemark.htm?offerId=xxxx 这个页面源码拿到csrf 即为: 下次请求四五星好评所需的_csrf
        # 时间原因先不进行修改!
        # 此外cookies也是必要的, 可用driver获取到再抽离出cookies
        # 研究发现: 其中ali-ss, ali-ss.sig为cookies必要字段
        # 下面还有问题不管怎么请求只能获取到第一页的评论
        #
        # tmp_url = 'https://m.1688.com/page/offerRemark.htm?offerId=' + str(goods_id)
        # body = self.driver.use_phantomjs_to_get_url_body(url=tmp_url)
        # # self.lg.info(str(body))
        #
        # if body == '':
        #     self.lg.error('该地址的body为空值, 出错地址: ' + tmp_url)
        #     return self._error_init()
        # try:
        #     csrf = re.compile('\"csrf\":\"(.*?)\",').findall(body)[0]
        # except IndexError:
        #     self.lg.error('获取csrf失败!')
        #     return self._error_init()
        #
        # self.lg.info('获取到的csrf值为: {}'.format(csrf))
        # cookies = self.driver._get_cookies()
        # cookies = dict_cookies_2_str(cookies)
        # self.lg.info('获取到的cookies为: {}'.format(cookies))
        # origin_comment_list = self._get_origin_comment_list(
        #     csrf=csrf,
        #     goods_id=goods_id,
        #     cookies=cookies, )
        # pprint(origin_comment_list)

        '''下面是模拟pc端好评接口'''
        try:
            # db中已有的buyer_name and comment_date_list
            db_top_n_buyer_name_and_comment_date_list = get_top_n_buyer_name_and_comment_date_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
        except SqlServerConnectionException:
            self.lg.error('db 连接异常! 此处抓取跳过!')
            return self._error_init()

        member_id = self._get_this_goods_member_id(goods_id=goods_id)
        self.lg.info('------>>>| 获取到的member_id: {0}'.format(member_id))
        if member_id == '':
            self.lg.error('获取到的member_id为空值!请检查!')
            return self._error_init()

        # 这里从db获取该商品原先的规格值
        try:
            db_sku_info = _get_sku_info_from_db_by_goods_id(
                goods_id=goods_id,
                logger=self.lg,)
            assert db_sku_info != [], 'db_sku_info为空list!'
        except DBGetGoodsSkuInfoErrorException:
            self.lg.error('获取db goods_id: {} 的sku_info失败! 此处跳过!'.format(goods_id))
            return self._error_init()

        # 同步
        # all_comment_list = self._get_all_comment_info(goods_id=goods_id, member_id=member_id)
        # celery
        all_comment_list = self._get_all_comment_info_by_celery(goods_id=goods_id, member_id=member_id)

        try:
            _comment_list = self._get_comment_list(
                all_comment_list=all_comment_list,
                db_top_n_buyer_name_and_comment_date_list=db_top_n_buyer_name_and_comment_date_list,
                db_sku_info=db_sku_info,
            )
            # pprint(_comment_list)
        except Exception:
            self.lg.error('遇到错误[goods_id:{}]:'.format(goods_id), exc_info=True)
            return self._error_init()

        _t = get_shanghai_time()
        _r = CommentItem()
        _r['goods_id'] = str(goods_id)
        _r['create_time'] = _t
        _r['modify_time'] = _t
        _r['_comment_list'] = _comment_list
        self.result_data = _r
        # pprint(self.result_data)

        return self.result_data

    def _get_all_comment_info_by_celery(self, goods_id, member_id):
        """
        获取所有comment
        :param goods_id:
        :param member_id:
        :return:
        """
        tasks = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('create task[where goods_id: {}, page_num: {}]...'.format(goods_id, page_num))
            try:
                async_obj = self._create_al_one_celery_task(
                    ip_pool_type=self.ip_pool_type,
                    goods_id=goods_id,
                    member_id=member_id,
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

    def _create_al_one_celery_task(self, **kwargs):
        """
        创建一个al celery obj
        :param kwargs:
        :return:
        """
        ip_pool_type = kwargs['ip_pool_type']
        goods_id = kwargs['goods_id']
        page_num = kwargs['page_num']
        cookies = kwargs['cookies']
        member_id = kwargs['member_id']

        async_obj = _get_al_one_page_comment_info_task.apply_async(
            args=[
                ip_pool_type,
                goods_id,
                member_id,
                page_num,
                cookies,
            ],
            expires=5 * 60,
            retry=False,
        )

        return async_obj

    def _get_all_comment_info(self, goods_id, member_id):
        """
        获取所有comment
        :param goods_id:
        :param member_id:
        :return:
        """
        all_comment_list = []
        for page_num in range(1, self.max_page_num):
            self.lg.info('------>>>| 正在抓取第{0}页...'.format(page_num))
            try:
                data = self._get_one_page_comment_info(
                    goods_id=goods_id,
                    page_num=page_num,
                    member_id=member_id, )
            except (AssertionError, Exception):
                self.lg.error('遇到错误:', exc_info=True)
                continue

            all_comment_list += data
            sleep(self._page_sleep_time)

        return all_comment_list

    def _get_comment_list(self, all_comment_list, db_top_n_buyer_name_and_comment_date_list, db_sku_info):
        """
        转换成结果集
        :param all_comment_list:
        :return:
        """
        _comment_list = []
        for item in all_comment_list:
            buyer_name = item.get('member', '')
            comment = []
            # TODO item.get('rateItem', [])只取第一条comment
            try:
                first_rate_item = item.get('rateItem', [])[0]
            except IndexError:
                continue

            _comment_content = wash_goods_comment(comment_content=first_rate_item.get('remarkContent', ''))
            if not filter_invalid_comment_content(_comment_content):
                continue

            comment_date = self._get_comment_date2(item=first_rate_item)
            comment.append({
                'comment': _comment_content,
                'comment_date': comment_date,
                'sku_info': choice(db_sku_info),  # 购买的商品规格(pc端1688商品没有规格)
                'star_level': first_rate_item.get('starLevel', 5),
                'img_url_list': [],
                'video': '',
            })
            quantify = item.get('quantity', 1)  # 购买数量
            if comment == []:  # 为空不录入
                continue

            if not filter_crawled_comment_content(
                    new_buyer_name=buyer_name,
                    new_comment_date=comment_date,
                    db_buyer_name_and_comment_date_info=db_top_n_buyer_name_and_comment_date_list,
                    logger=self.lg):
                # 过滤已采集的comment
                continue

            _ = {
                'buyer_name': buyer_name,  # 买家昵称
                'comment': comment,  # 评论内容
                'quantify': quantify,  # 购买数量
                'head_img': '',  # 用户头像
                'append_comment': {},  # 追评
            }
            _comment_list.append(_)

        return _comment_list

    def _get_one_page_comment_info(self, goods_id, page_num, member_id,) -> list:
        """
        获取单页的comment info
        :param page_num:
        :return:
        """
        def _get_params(goods_id, page_num, member_id):
            # t = str(int(time.time())) + str(randint(100, 999))
            # self.lg.info(member_id)
            params = (
                # ('callback', 'jQuery17205914468174705312_1531451658317'),
                ('_input_charset', 'GBK'),
                ('offerId', str(goods_id)),
                ('page', str(page_num)),
                ('pageSize', '15'),
                ('starLevel', '7'),
                # ('orderBy', 'date'),
                ('orderBy', ''),
                ('semanticId', ''),
                # ('showStat', '0'),
                ('showStat', '1'),
                ('content', '1'),
                # ('t', t),
                ('memberId', str(member_id)),
                ('isNeedInitRate', 'false'),
            )

            return params

        params = _get_params(
            goods_id=goods_id,
            page_num=page_num,
            member_id=member_id)
        url = 'https://rate.1688.com/remark/offerDetail/rates.json'
        headers = get_base_headers()
        headers.update({
            'referer': 'https://detail.1688.com/offer/{0}.html'.format(str(goods_id))
        })
        # 原先用Requests老是404，改用phantomjs也老是404
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            cookies=self.login_cookies_dict,)
        self.lg.info(str(body))
        assert body != '', '该地址的body为空值, 出错goods_id: {0}'.format(goods_id)

        _data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={})
        if _data.get('url') is not None:
            sleep(self._page_sleep_time)
            assert _data.get('url') is not None, '------>>>| 被重定向到404页面, 休眠{0}s中...'.format(self._page_sleep_time)

        data = _data.get('data', {}).get('rates', [])
        self.lg.info('[{}] goods_id: {}, page_num: {}'.format(
            '+' if data != [] else '-',
            goods_id,
            page_num,))

        # assert data != [], '获取到的data为空list!'

        return data

    def _get_comment_date2(self, item) -> str:
        """
        获取评论日期
        :param item:
        :return: eg: '2018-04-04 15:17:37'
        """
        comment_date = str(item.get('remarkTime', ''))

        return comment_date

    def _get_origin_comment_list(self, **kwargs) -> list:
        '''
        得到加密的接口数据信息
        :param kwargs:
        :return:
        '''
        csrf = kwargs.get('csrf', '')
        goods_id = kwargs.get('goods_id', '')
        cookies = kwargs.get('cookies', '')

        url = 'https://m.1688.com/page/offerRemark.htm'
        headers = {
            'cookie': cookies,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://m.1688.com/page/offerRemark.htm?offerId={}'.format(goods_id),
            'authority': 'm.1688.com',
            'x-requested-with': 'XMLHttpRequest',
        }

        origin_comment_list = []
        for i in range(1, self.max_page):
            __wing_navigate_options = {
                'data': {
                    'bizType': 'trade',
                    'itemId': int(goods_id),
                    'offerId': str(goods_id),
                    'page': i,
                    'pageSize': 5,
                    # 'receiveUserId': 989036456,
                    'starLevel': 7
                }
            }
            params = (
                ('_csrf', csrf),
                ('__wing_navigate_type', 'view'),
                ('__wing_navigate_url', 'detail:modules/offerRemarkList/view'),
                ('__wing_navigate_options', dumps(__wing_navigate_options)),
                ('_', str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(start_num=100, end_num=999))),
            )
            body = Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
            data = json_2_dict(body, encoding='ascii').get('data', {})
            # pprint(data)
            one = data.get('model', [])
            pprint(one)
            origin_comment_list += one
            sleep(.25)

        return origin_comment_list

    def _error_init(self):
        self.result_data = {}

        return {}

    def _get_this_goods_member_id(self, goods_id):
        '''
        获取member_id
        :param goods_id:
        :return: '' or str
        '''
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            # 'X-DevTools-Emulate-Network-Conditions-Client-Id': '5C1ED6AF76F4F84D961F136EAA06C40F',
        }
        params = (
            ('offerId', str(goods_id)),
        )
        url = 'https://m.1688.com/page/offerRemark.htm'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            self.lg.error('获取到的body为空值!此处跳过!')
            return ''

        try:
            member_id = re.compile(r'"memberId":"(.*?)",').findall(body)[0]
        except IndexError:
            self.lg.error('获取member_id时索引异常!请检查!')
            return ''

        return member_id

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://detail.1688.com/offer/44412151595.html?spm=a2604.8117111.ji00a0ac.3.2e8e3ea73bvZT4',
            'authority': 'rate.1688.com',
            # 其中的ali-ss为必须参数
            'cookie': 'ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiJFOF9XcF9NMWV5QWRKWHBVb1lLTlhaZk8iLCJfZXhwaXJlIjoxNTMxNTM0MTMwODMzLCJfbWF4QWdlIjo4NjQwMDAwMH0=; ali-ss.sig=573tlT1Aed2ggvlhClMHb8sZatbgVlRrIxljURSRZys; JSESSIONID=9L78RXlv1-k80a7jb9VDbOxXoH4H-OW2AexQ-jQ3d; cookie2=10d7bba23bbc61948af48e1dd2611282; t=1bdcbe0b678123e1755897be375b453f; _tb_token_=77fe63e3066b3; _tmp_ck_0=3Oo5x6beKeA77mSeFyI8GT8FHF5re5voELqxVsc%2FfpE4tqj%2B88wXi1tm1CBqsrie3iytT%2FtexS2f1gz4cNHi2Eu4hv7YjQ3LERzyqyHdFPQhvo0xY7gXNGXM9%2FZ1vj7kgF%2FDvB6r3ddV6BnQSr5Z6yrZIruC7DPdfJO0g23ShfLkoDeSB6j7j5l9OOSrQ0hXXsClBhhps89CzdCYLvmRWeOqmbTf1LoCMhMayyk116UUrhNQqpgoaurnG6C1XKdmm1QpNwyCdPzmJxb2%2FhafYOVC8Zmqu9DtlO48topX3Pg9HVynFVMDXBBTq6GYgoVx5rwkN6JkXezXK9RU9OIu3o9TtslpsNTXIwD1NkXOb4mUmH1PDBJ3yvST9GePCQeaxovWab0bwzQ%3D;',
        }

    def _get_comment_date(self, comment_date):
        '''
        得到datetime类型的时间
        :param comment_date: eg: 2017-12-04
        :return: datetime
        '''
        _ = str(randint(0, 23))
        if len(_) == 1:
            _hour = '0' + _
        else:
            _hour = _

        _ = str(randint(0, 59))
        if len(_) == 1:
            _min = '0' + _
        else:
            _min = _

        _ = str(randint(0, 59))
        if len(_) == 1:
            _s = '0' + _
        else:
            _s = _

        comment_date = comment_date + ' ' + _hour + ':' + _min + ':' + _s

        return comment_date

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        try:
            del self.lg
            del self.msg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    ali_1688 = ALi1688CommentParse()
    while True:
        goods_id = input('请输入要爬取的商品goods_id(以英文分号结束): ')
        goods_id = goods_id.strip('\n').strip(';')
        ali_1688._get_comment_data(goods_id=goods_id)

        gc.collect()



