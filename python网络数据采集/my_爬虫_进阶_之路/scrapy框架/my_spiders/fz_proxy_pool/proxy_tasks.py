# coding:utf-8

'''
@author = super_fazai
@File    : proxy_tasks.py
@connect : superonesfazai@gmail.com
'''

from celery.utils.log import get_task_logger
from random import choice, randint
from scrapy.selector import Selector
import requests
from pickle import dumps
import re

from items import ProxyItem

from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)
from fzutils.safe_utils import get_uuid3
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.celery_utils import init_celery_app
from fzutils.sql_utils import BaseRedisCli

app = init_celery_app()
lg = get_task_logger('proxy_tasks')      # 当前task的logger对象, tasks内部保持使用原生celery log对象
_key = get_uuid3('proxy_tasks')  # 存储proxy_list的key
redis_cli = BaseRedisCli()

@app.task   # task修饰的方法无法修改类属性
def _get_kuaidaili_proxy() -> list:
    '''
    spiders: 获取快代理高匿名ip
    :return:
    '''
    def parse_body(body):
        '''解析url body'''
        table = Selector(text=body).css('div#list table tbody').extract_first()
        _ = []
        for tr in Selector(text=table).css('tr').extract():
            o = ProxyItem()
            try:
                ip = Selector(text=tr).css('td:nth-child(1) ::text').extract_first()
                assert ip != '', 'ip为空值!'
                port = Selector(text=tr).css('td:nth-child(2) ::text').extract_first()
                assert port != '', 'port为空值!'
                ip_type = Selector(text=tr).css('td:nth-child(4) ::text').extract_first()
                assert ip_type != '', 'ip_type为空值!'
                ip_type = 'http' if ip_type == 'HTTP' else 'https'
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

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Referer': 'https://www.kuaidaili.com/free/intr/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    proxy_url = 'https://www.kuaidaili.com/free/inha/' + str(randint(1, 1000))
    # 从已抓取的代理中随机代理采集, 没有则用本机ip(first crawl)!
    try:
        body = requests.get(url=proxy_url, headers=headers, params=None, cookies=None, proxies=_get_proxies()).text
        # lg.info(body)
    except Exception:
        lg.error('遇到错误:', exc_info=True)
        return []

    return parse_body(body)

@app.task
def _write_into_redis(res):
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
        lg.info('正在使用代理{}crawl...'.format(proxies['http']))
    else:
        lg.info('第一次抓取使用本机ip...')

    return proxies or {}        # 如果None则返回{}

@app.task
def check_proxy_status(proxy, timeout=8) -> bool:
    '''
    检测代理状态, 发现免费网站写的信息不靠谱, 还是要自己检测代理的类型
    :param proxy: 待检测代理
    :return:
    '''
    res = False
    URL = 'http://m.gx8899.com/'
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_phone_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    try:
        response = requests.request("GET", url=URL, headers=headers, proxies={'http': 'http://' + proxy}, timeout=timeout)
        status_code = response.status_code
        body = response.content.decode('gb2312')
        lg.info(str(body))
        if status_code != 200\
                or re.compile('8899头像网吧').findall(body) == []:
            return res

    except Exception:
        return res

    return True