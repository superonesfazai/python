# coding:utf-8

'''
@author = super_fazai
@File    : celery_tasks.py
@connect : superonesfazai@gmail.com
'''

import re
from gc import collect
from celery.utils.log import get_task_logger
from asyncio import (
    wait_for,
    Future,)
from functools import partial
from threading import (
    Thread,
    current_thread,)
from asyncio import (
    new_event_loop,
    get_event_loop,
    set_event_loop,)
from time import sleep
from multiplex_code import (
    _get_al_one_type_company_id_list,
    _get_114_one_type_company_id_list,
    _get_someone_goods_id_all_comment,)
from settings import (
    PHANTOMJS_DRIVER_PATH,
)

from company_spider import CompanySpider

from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,
    get_base_headers,
    _get_url_contain_params,
    dict_cookies_2_str,)
from fzutils.common_utils import json_2_dict
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,)
from fzutils.common_utils import get_random_int_number
from fzutils.celery_utils import *
from fzutils.spider.selector import parse_field
from fzutils.spider.fz_requests import Requests
from fzutils.spider.fz_driver import BaseDriver

"""
redis:
# 指定被修改后的redis.conf来启动
$ redis-server /usr/local/etc/redis.conf

分布式任务启动: 
1. celery -A celery_tasks worker -l info -P eventlet -c 300
单个后台 celery multi start w0 -A celery_tasks -P eventlet -c 300 -f /Users/afa/myFiles/my_spider_logs/tmp/celery_tasks.log 
(多开)
2. celery multi start w0 w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12 w13 w14 w15 w16 w17 -A celery_tasks -P eventlet -c 300 -f /Users/afa/myFiles/my_spider_logs/tmp/celery_tasks.log 

监控:
$ celery -A celery_tasks flower --address=127.0.0.1 --port=5555
$ open http://localhost:5555
"""

tasks_name = 'celery_tasks'
app = init_celery_app(
    name=tasks_name,
)
lg = get_task_logger(tasks_name)

@app.task(name=tasks_name + '._get_al_one_type_company_id_list_task', bind=True)
def _get_al_one_type_company_id_list_task(self, ip_pool_type, keyword, page_num, timeout=15):
    """
    获取al 某关键字的单页company_info
    :param self:
    :param ip_pool_type:
    :param keyword:
    :param page_num:
    :param timeout:
    :return:
    """
    # def _get_args():
    #     return [
    #         db_al_unique_id_list,
    #         ip_pool_type,
    #         lg,
    #         keyword,
    #         page_num,
    #         timeout,
    #     ]

    # loop = get_event_loop()
    # loop = new_event_loop()
    # args = _get_args()
    # try:
    #     # res = loop.run_in_executor(None, _get_al_one_type_company_id_list(
    #     #     db_al_unique_id_list=db_al_unique_id_list,
    #     #     ip_pool_type=ip_pool_type,
    #     #     logger=lg,
    #     #     keyword=keyword,
    #     #     page_num=page_num,
    #     #     timeout=timeout,
    #     # ))
    #     res = loop.run_in_executor(None, _get_al_one_type_company_id_list, *args)
    # except Exception as e:
    #     lg.error('遇到错误:', exc_info=True)
    # finally:
    #     try:
    #         del loop
    #     except:
    #         pass
    #     collect()
    #
    #     return res

    # celery不能序列化协程对象, 故无法写成协程形式, 使用常规函数式
    res = _get_al_one_type_company_id_list(
        ip_pool_type=ip_pool_type,
        logger=lg,
        keyword=keyword,
        page_num=page_num,
        timeout=timeout)
    collect()

    return res

@app.task(name=tasks_name + '._get_114_one_type_company_id_list_task', bind=True)
def _get_114_one_type_company_id_list_task(self, ip_pool_type, num_retries, parser_obj, cate_num, page_num):
    res = _get_114_one_type_company_id_list(
        ip_pool_type=ip_pool_type,
        num_retries=num_retries,
        cate_num=cate_num,
        page_num=page_num,
        parser_obj=parser_obj,
        logger=lg,)
    collect()

    return res

class TaskObj(Thread):
    '''
    重写爬虫线程
    '''
    def __init__(self, func, args=(), default_res=None):
        super(TaskObj, self).__init__()
        self.func = func
        self.args = args
        # Thread默认结果
        self.default_res = default_res
        self.res = default_res

    def run(self):
        self.res = self.func(*self.args)

    def _get_result(self):
        try:
            Thread.join(self)  # 等待线程执行完毕
            return self.res
        except Exception:
            lg.error('线程遇到错误:', exc_info=True)
            return self.default_res

@app.task(name=tasks_name + '._parse_one_company_info_task', bind=True)
def _parse_one_company_info_task(self, short_name, company_url='', province_name='', city_name='', company_id='', type_code=''):
    def oo():
        try:
            company_spider = CompanySpider()
            # 设置当前事件循环为新的事件循环, 避免报错
            set_event_loop(new_event_loop())
            loop = new_event_loop()
            res = loop.run_until_complete(company_spider._parse_one_company_info(
                short_name=short_name,
                company_url=company_url,
                province_name=province_name,
                city_name=city_name,
                company_id=company_id,
                type_code=type_code,))
        except Exception:
            lg.error('遇到错误:', exc_info=True)
            res = {}

        try:
            loop.close()
        except:
            pass
        try:
            del company_spider
        except:
            pass
        collect()

        return res

    # TODO celery与asyncio的结合使用将在celery5.0(官方未开发)以后实现, 现在celery4.2.1会出现异常!
    thread1 = TaskObj(oo, args=(), default_res={})
    thread1.start()
    lg.info('thread {} is running...'.format(current_thread().name))

    return thread1._get_result()

def _get_pc_headers() -> dict:
    return {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

def _get_phone_headers() -> dict:
    return {
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_phone_ua(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

@app.task(name=tasks_name + '._get_114_company_page_html_task', bind=True)
def _get_114_company_page_html_task(self, company_id, ip_pool_type, num_retries) -> tuple:
    '''
    获取114单个页面的page_html
    :param self:
    :param company_id:
    :return: (company_id, body)
    '''
    headers = _get_pc_headers()
    headers.update({
        'Proxy-Connection': 'keep-alive',
        # 'Referer': 'http://www.114pifa.com/c-3181.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    url = 'http://www.114pifa.com/ca/{}'.format(company_id)
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        ip_pool_type=ip_pool_type,
        encoding='gbk',
        num_retries=num_retries,)
    if body == '':
        lg.error('company body为空值! shop_url: {}'.format(url))

    lg.info('[{}] 114 company_id: {}'.format('+' if body != '' else '-', company_id))

    return company_id, body

@app.task(name=tasks_name + '._get_yw_one_type_company_id_list_task', bind=True)
def _get_yw_one_type_company_id_list_task(self, ip_pool_type, keyword, page_num, timeout=15):
    """
    获取yw某关键字的单页company_info(m 站)
    :param self:
    :param ip_pool_type:
    :param keyword:
    :param page_num:
    :param timeout:
    :return:
    """
    headers = _get_phone_headers()
    headers.update({
        # 'x-csrf-token': 'v8N2st76hSgzPPYQ-1DYgqOh',
        # 'Referer': 'http://wap.yiwugo.com/search?q=%E5%8E%8B%E7%BC%A9%E6%9C%BA',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    })
    params = (
        ('q', str(keyword)),
        ('cpage', str(page_num)),
        ('pageSize', '28'),
        ('st', '0'),
        ('m', ''),
        ('f', ''),
        ('s', ''),
    )
    s_url = 'http://wap.yiwugo.com/api/search/s.htm'
    body = Requests.get_url_body(
        url=s_url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        num_retries=6,
        timeout=timeout,)
    # lg.info(body)
    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=lg).get('prslist', [])
    # lg.info(str(data))
    company_info_list = [{
        'company_id': item.get('shopUrlId', ''),
        'company_name': item.get('shopName', ''),
    } for item in data]
    company_info_list = list_remove_repeat_dict_plus(target=company_info_list, repeat_key='company_id')
    # lg.info(str(company_info_list))

    lg.info('[{}] keyword: {}, page_num: {}'.format(
        '+' if company_info_list != [] else '-',
        keyword,
        page_num,))

    return company_info_list

@app.task(name=tasks_name + '._get_hn_one_type_company_id_list_task', bind=True)
def _get_hn_one_type_company_id_list_task(self, ip_pool_type, keyword, page_num, province_name, city_name, city_base_url, shop_item_selector:dict, shop_id_selector:dict, w3_selector:dict, num_retries=6, timeout=15,):
    """
    获取hn 某关键字的单页company_info
    :param self:
    :param ip_pool_type:
    :param keyword:
    :param page_num:
    :param province_name:
    :param city_name:
    :param city_base_url:
    :param shop_item_selector:
    :param shop_id_selector:
    :param w3_selector:
    :param num_retries:
    :param timeout:
    :return: [{'company_id': xxx, 'province_name': 'xx', 'city_name': 'xx', 'w3': 'xx'}, ...]
    """
    try:
        w3 = parse_field(
            parser=w3_selector,
            target_obj=city_base_url,
            logger=lg,)
        assert w3 != '', 'w3为空值!'
    except AssertionError:
        lg.error('遇到错误:', exc_info=True)
        return []

    headers = _get_pc_headers()
    headers.update({
        'Proxy-Connection': 'keep-alive',
    })
    params = (
        ('q', str(keyword)),
        ('sourcePage', '/'),
        ('page_no', str(page_num)),
    )
    # url = 'http://www.huoniuniu.com/goods'
    url = city_base_url + '/goods'
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        num_retries=num_retries,
        ip_pool_type=ip_pool_type,
        timeout=timeout)
    # lg.info(body)

    shop_item_list = parse_field(
        parser=shop_item_selector,
        target_obj=body,
        is_first=False,
        logger=lg,)
    # pprint(shop_item_list)

    shop_id_list = []
    for item in shop_item_list:
        try:
            company_id = parse_field(
                parser=shop_id_selector,
                target_obj=item,
                is_first=True,
                logger=lg)
            assert company_id != '', 'company_id不为空值!'
            shop_id_list.append({
                'company_id': company_id,
                'province_name': province_name,
                'city_name': city_name,
                'w3': w3,
            })
        except AssertionError:
            continue
    shop_id_list = list_remove_repeat_dict_plus(
        target=shop_id_list,
        repeat_key='company_id',)
    # pprint(shop_id_list)
    lg.info('[{}] keyword: {}, page_num: {}, province_name: {}, city_name: {}'.format(
        '+' if shop_id_list != [] else '-',
        keyword,
        page_num,
        province_name,
        city_name,
    ))
    collect()

    return shop_id_list

@app.task(name=tasks_name + '._get_tb_one_page_comment_info_task', bind=True)
def _get_tb_one_page_comment_info_task(self, ip_pool_type, goods_id, page_num, cookies:dict) -> list:
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
    params = _get_params(goods_id=goods_id, page_num=page_num)
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        encoding='gbk',
        ip_pool_type=ip_pool_type,
        cookies=cookies,)
    # lg.info(str(body))

    data = []
    try:
        data = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            logger=lg,
            default_res={}).get('comments', [])
        # pprint(data)
        assert data != [], 'data为空list!出错goods_id:{}'.format(goods_id)
    except (IndexError, AssertionError):
        sleep(.5)
        lg.error('re得到需求body时出错!出错goods_id: {}'.format(goods_id))

    lg.info('[{}] page_num: {}, goods_id: {}'.format(
        '+' if data != [] else '-',
        page_num,
        goods_id,))

    return data

@app.task(name=tasks_name + '._get_tm_one_page_comment_info_task', bind=True)
def _get_tm_one_page_comment_info_task(self, ip_pool_type, goods_id, _type, seller_id, page_num, page_size, cookies:dict) -> list:
    """
    获取天猫某goods_id单页的comment
    :param self:
    :param ip_pool_type:
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

    url = 'https://rate.tmall.com/list_detail_rate.htm'
    headers = get_base_headers()
    headers.update({
        'referer': 'https://detail.m.tmall.com/item.htm?id={}'.format(goods_id),
    })
    params = _get_params(
        goods_id=goods_id,
        seller_id=seller_id,
        page_num=page_num,
        page_size=page_size)
    # cookies必须! requests 请求无数据!
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        cookies=cookies,
        ip_pool_type=ip_pool_type,)

    # 所以直接用phantomjs来获取相关api数据
    # url = _get_url_contain_params(url=url, params=params)
    # # lg.info(url)
    # driver = BaseDriver(
    #     executable_path=PHANTOMJS_DRIVER_PATH,
    #     logger=lg,
    #     ip_pool_type=ip_pool_type,
    #     driver_cookies=dict_cookies_2_str(cookies))
    # body = driver.get_url_body(url=url)
    # try:
    #     del driver
    # except:
    #     pass
    # lg.info(str(body))

    data = []
    try:
        assert body != '', '获取到的body为空str! 出错type:{0}, goods_id:{1}'.format(_type, goods_id)
        data = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            default_res={},
            logger=lg,)
        redict_url = 'https:' + data.get('url', '').replace('https:', '') if data.get('url', '') != '' else ''
        if redict_url != '':
            lg.info(redict_url)
        else:
            pass
        data = data.get('rateDetail', {}).get('rateList', [])

    except (IndexError, AssertionError):
        lg.error('遇到错误:', exc_info=True)

    lg.info('[{}] goods_id: {}, page_num: {}'.format(
        '+' if data != [] else '-',
        goods_id,
        page_num, ))
    collect()

    return data

@app.task(name=tasks_name + '._get_al_one_page_comment_info_task', bind=True)
def _get_al_one_page_comment_info_task(self, ip_pool_type, goods_id, member_id, page_num, cookies:dict) -> list:
    """
    获取al单页评论信息
    :param self:
    :param ip_pool_type:
    :param goods_id:
    :param member_id:
    :param page_num:
    :param cookies:
    :return:
    """
    def _get_params(goods_id, page_num, member_id):
        # t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
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

    url = 'https://rate.1688.com/remark/offerDetail/rates.json'
    headers = get_base_headers()
    headers.update({
        'referer': 'https://detail.1688.com/offer/{0}.html'.format(str(goods_id))
    })
    params = _get_params(
        goods_id=goods_id,
        page_num=page_num,
        member_id=member_id)
    # 原先用Requests老是404，改用phantomjs也老是404
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        cookies=cookies,)
    # lg.info(str(body))

    data = []
    try:
        _data = json_2_dict(
            json_str=body,
            logger=lg,
            default_res={})
        assert _data.get('url') is None, '被重定向到404页面!'
        data = _data.get('data', {}).get('rates', [])

    except Exception:
        lg.error('遇到错误[goods_id:{}]:'.format(goods_id), exc_info=True)

    lg.info('[{}] goods_id: {}, page_num: {}'.format(
        '+' if data != [] else '-',
        goods_id,
        page_num,))
    collect()

    return data

@app.task(name=tasks_name + '._get_z8_one_page_comment_info_task', bind=True)
def _get_z8_one_page_comment_info_task(self, ip_pool_type, goods_id, page_num, page_size) -> list:
    """
    获取zhe800单页评论信息
    :param self:
    :param ip_pool_type:
    :param goods_id:
    :param page_num:
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

    url = 'https://th5.m.zhe800.com/app/detail/comment/list'
    headers = _get_phone_headers()
    headers.update({
        'referer': 'https://th5.m.zhe800.com/h5/comment/list?zid={0}&dealId=39890410&tagId='.format(str(goods_id))
    })
    params = _get_params(
        goods_id=goods_id,
        page_num=page_num,
        page_size=page_size,)
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type)
    # lg.info(str(body))
    _data = json_2_dict(
        json_str=body,
        logger=lg,
        default_res={})
    # pprint(_data)
    data = _data.get('comments', [])
    try:
        assert _data.get('comments') is not None \
               and _data.get('hasNext') is not None, '获取到的data为None, 出错goods_id: {}'.format(goods_id)
    except AssertionError:
        pass

    # 判断是否下页还有评论信息
    # <class 'bool'>
    # has_next_page = _data.get('hasNext', False)
    lg.info('[{}] goods_id: {}, page_num: {}'.format(
        '+' if data != [] else '-',
        goods_id,
        page_num,))
    collect()

    return data

@app.task(name=tasks_name + '._get_someone_goods_id_all_comment_task', bind=True)
def _get_someone_goods_id_all_comment_task(self, index, site_id:int, goods_id) -> dict:
    """
    获取某个goods_id的all comment info
    :param self:
    :param site_id:
    :return:
    """
    res = _get_someone_goods_id_all_comment(
        index=index,
        site_id=site_id,
        goods_id=goods_id,
        logger=lg)

    return res

@app.task(name=tasks_name + '._get_pk_one_type_company_id_list_task', bind=True)
def _get_pk_one_type_company_id_list_task(self, ip_pool_type, keyword:str, page_num, province_name, city_name, city_id, w3, num_retries=6, timeout=15,) -> list:
    """
    获取pk单个关键字单页的company_id_list
    :param self:
    :param ip_pool_type:
    :param keyword:
    :param page_num:
    :param province_name:
    :param city_name:
    :param city_id:
    :param w3:
    :param num_retries:
    :param timeout:
    :return:
    """
    headers = _get_phone_headers()
    headers.update({
        'accept': 'application/json, text/plain, */*',
        'Origin': 'https://m.ppkoo.com',
    })
    params = (
        # ('cid', '50000436'),          # 根据keywords索引的话, cid可不传
        ('keywords', keyword),
        ('hot', 'desc'),
        ('page', str(page_num)),
        ('city_id', str(city_id)),
        # ('v', '3784143914913054'),
    )
    url = 'https://www.ppkoo.com/api/Search/goods'
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        num_retries=num_retries,
        timeout=timeout,)
    # 存在: {"status":true,"total":"0","data":null}
    # lg.info(body)

    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=lg).get('data', [])
    # pprint(data)
    if data is None:
        # 处理null的赋值情况
        data = []
    else:
        pass

    company_info_list = []
    for item in data:
        try:
            company_id = item.get('business_id', '')
            assert company_id != ''
            address = item.get('shop_location', '')
            assert address != ''
            company_info_list.append({
                'company_id': company_id,
                'province_name': province_name,
                'city_name': city_name,
                'w3': w3,
                'address': address,                 # 此处即可获取详细地址!
            })
        except Exception:
            continue

    company_info_list = list_remove_repeat_dict_plus(target=company_info_list, repeat_key='company_id')
    # pprint(company_info_list)
    lg.info('[{}] keyword: {}, page_num: {}'.format(
        '+' if company_info_list != [] else '-',
        keyword,
        page_num,))

    return company_info_list

