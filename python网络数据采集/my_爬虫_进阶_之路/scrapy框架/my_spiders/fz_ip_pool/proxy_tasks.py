# coding:utf-8

'''
@author = super_fazai
@File    : proxy_tasks.py
@connect : superonesfazai@gmail.com
'''

from celery.utils.log import get_task_logger
from random import choice
from scrapy.selector import Selector
import requests
from pickle import dumps
import re
from time import sleep

from items import ProxyItem
from settings import (
    CHECK_PROXY_TIMEOUT,
    parser_list,
    proxy_list_key_name,)

from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)
from fzutils.safe_utils import get_uuid3
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.celery_utils import init_celery_app
from fzutils.sql_utils import BaseRedisCli
from fzutils.common_utils import json_2_dict

app = init_celery_app()
lg = get_task_logger('proxy_tasks')      # 当前task的logger对象, tasks内部保持使用原生celery log对象
_key = get_uuid3(proxy_list_key_name)  # 存储proxy_list的key
redis_cli = BaseRedisCli()

@app.task(name='proxy_tasks._get_proxy', bind=True)   # task修饰的方法无法修改类属性
def _get_proxy(self, random_parser_list_item_index, proxy_url) -> list:
    '''
    spiders: 获取代理高匿名ip
    :return:
    '''
    def _get_base_headers():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://www.kuaidaili.com/free/intr/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def parse_body(body):
        '''解析url body'''
        def _get_ip_type(ip_type):
            '''获取ip_type'''
            # return 'http' if ip_type == 'HTTP' else 'https'
            return 'http'       # 全部返回'http'

        _ = []
        parser_obj = parser_list[random_parser_list_item_index]
        try:
            part_selector = parser_obj.get('part', '')
            assert part_selector != '', '获取到part为空值!'
            position = parser_obj.get('position', {})
            assert position != {}, '获取到position为空dict!'
            ip_selector =  position.get('ip', '')
            assert ip_selector != '', '获取到ip_selector为空值!'
            port_selector = position.get('port', '')
            assert port_selector != '', '获取到port_selector为空值!'
            ip_type_selector = position.get('ip_type', '')
            assert ip_type_selector != '', '获取到ip_type_selector为空值!'
        except AssertionError:
            return []

        for tr in Selector(text=body).css(part_selector).extract():
            o = ProxyItem()
            try:
                ip = Selector(text=tr).css('{} ::text'.format(ip_selector)).extract_first()
                if re.compile('\d+').findall(ip) == []:     # 处理不是ip地址
                    continue
                assert ip != '', 'ip为空值!'
                port = Selector(text=tr).css('{} ::text'.format(port_selector)).extract_first()
                assert port != '', 'port为空值!'
                ip_type = Selector(text=tr).css('{} ::text'.format(ip_type_selector)).extract_first()
                assert ip_type != '', 'ip_type为空值!'
                ip_type = _get_ip_type(ip_type)
            except AssertionError or Exception:
                lg.error('遇到错误:', exc_info=True)
                continue
            o['ip'] = ip
            try:
                o['port'] = int(port)
            except Exception:
                lg.error('int转换port时出错!跳过!')
                continue
            o['ip_type'] = ip_type
            o['anonymity'] = 1
            o['score'] = 100
            o['last_check_time'] = str(get_shanghai_time())
            # lg.info('[+] {}:{}'.format(ip, port))
            _.append(o)

        return _

    headers = _get_base_headers()
    # 从已抓取的代理中随机代理采集, 没有则用本机ip(first crawl)!
    try:
        encoding = parser_list[random_parser_list_item_index].get('charset')
        body = requests.get(
            url=proxy_url,
            headers=headers,
            params=None,
            cookies=None,
            proxies=_get_proxies(),
            timeout=CHECK_PROXY_TIMEOUT).content.decode(encoding)
        # lg.info(body)
    except Exception:
        lg.error('遇到错误:', exc_info=True)
        return []
    # sleep(2)

    return parse_body(body)

@app.task(name='proxy_tasks._write_into_redis', bind=True)
def _write_into_redis(self, res):
    '''
    读取并更新新采集的proxy
    :param res:
    :return:
    '''
    origin_data = redis_cli.get(_key) or dumps([])  # get为None, 则返回[]
    old = deserializate_pickle_object(origin_data)
    old += res
    redis_cli.set(name=_key, value=dumps(old))

    return True

def _get_proxies() -> dict:
    '''
    随机一个proxy
    :return:
    '''
    origin_data = redis_cli.get(_key) or dumps([])
    proxy_list = deserializate_pickle_object(origin_data)
    proxies = choice(proxy_list) if len(proxy_list) > 0 else None
    if proxies is not None:
        proxies = {
            'http': 'http://{}:{}'.format(proxies['ip'], proxies['port'])
        }
        lg.info('正在使用代理 {} crawl...'.format(proxies['http']))
    else:
        lg.info('第一次抓取使用本机ip...')

    return proxies or {}        # 如果None则返回{}

@app.task(name='proxy_tasks.check_proxy_status', bind=True)    # 一个绑定任务意味着任务函数的第一个参数总是任务实例本身(self)
def check_proxy_status(self, proxy, timeout=CHECK_PROXY_TIMEOUT) -> bool:
    '''
    检测代理状态, 突然发现, 免费网站写的信息不靠谱, 还是要自己检测代理的类型
    :param proxy: 待检测代理
    :return:
    '''
    # lg.info(str(self.request))
    res = False
    URL = 'http://httpbin.org/get'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get(url=URL, headers=headers, proxies=proxies, timeout=timeout)
        lg.info(str(response.text))
        if response.ok:
            content = json_2_dict(json_str=response.text)
            proxy_connection = content.get('headers', {}).get('Proxy-Connection', None)
            ip = content.get('origin', '')
            if ',' in ip:
                pass
            elif proxy_connection:
                pass
            else:                       # 只抓取高匿名代理
                lg.info(str('成功捕获一只高匿ip: {}'.format(proxy)))
                return True
    except Exception:
        pass

    return res