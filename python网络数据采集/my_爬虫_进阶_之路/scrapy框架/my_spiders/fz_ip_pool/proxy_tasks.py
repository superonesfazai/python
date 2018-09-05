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
from requests.exceptions import (
    ConnectTimeout,
    ProxyError,
    ReadTimeout,)
from pickle import dumps
import re

from items import ProxyItem
from settings import (
    CHECK_PROXY_TIMEOUT,
    parser_list,
    proxy_list_key_name,
    high_proxy_list_key_name,
    TEST_HTTP_HEADER,)

from fzutils.time_utils import get_shanghai_time
from fzutils.internet_utils import get_random_pc_ua
from fzutils.safe_utils import get_uuid3
from fzutils.celery_utils import init_celery_app
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.sql_utils import BaseRedisCli
from fzutils.common_utils import (
    json_2_dict,
    delete_list_null_str,)
from fzutils.spider.fz_requests import Requests

app = init_celery_app()
lg = get_task_logger('proxy_tasks')             # 当前task的logger对象, tasks内部保持使用原生celery log对象
_key = get_uuid3(proxy_list_key_name)           # 存储proxy_list的key
_h_key = get_uuid3(high_proxy_list_key_name)    # 高匿key
redis_cli = BaseRedisCli()
a_66_ip = []

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
    except (ConnectTimeout, ProxyError, ReadTimeout) as e:
        lg.error('遇到错误: {}'.format(e.args[0]))
        return []
    except Exception:
        lg.error('遇到错误:', exc_info=True)
        return []
    # sleep(2)

    return parse_body(body)

def _get_66_ip_list():
    '''
    先获取66高匿名ip
    :return:
    '''
    global a_66_ip
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.66ip.cn/nm.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('getnum', ''),
        ('isp', '0'),
        ('anonymoustype', '3'),
        ('start', ''),
        ('ports', ''),
        ('export', ''),
        ('ipaddress', ''),
        ('area', '0'),
        ('proxytype', '2'),
        ('api', '66ip'),
    )

    response = requests.get('http://www.66ip.cn/nmtq.php', headers=headers, params=params, cookies=None)
    body = Requests._wash_html(response.content.decode('gbk'))
    try:
        part = re.compile(r'</script>(.*)</div>').findall(body)[0]
    except IndexError:
        part = ''
    part = re.compile('<script>.*?</script>|</div>.*</div>').sub('', part)
    # print(part)
    ip_list = delete_list_null_str(part.split('<br />'))
    # print(ip_list)
    a_66_ip = ip_list if ip_list != [] else []

    return ip_list

def _get_proxies() -> dict:
    '''
    随机一个高匿名proxy(极大概率失败, 耐心!)
    :return:
    '''
    proxy_list = deserializate_pickle_object(redis_cli.get(_h_key) or dumps([]))
    proxies = choice(proxy_list) if len(proxy_list) > 0 else None
    if proxies is not None:
        proxies = {
            'http': 'http://{}:{}'.format(proxies['ip'], proxies['port'])
        }
        lg.info('正在使用代理 {} crawl...'.format(proxies['http']))
    else:
        lg.info('第一次抓取使用本机ip...')
        # 使用66ip，免费高匿ip
        # if a_66_ip == []:
        #     _get_66_ip_list()
        # proxies = {
        #     'http': 'http://{}'.format(choice(a_66_ip)),
        # }
        # lg.info('正在使用代理 {} crawl...'.format(proxies['http']))

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
        # 'https': 'https://' + proxy,
    }
    try:
        response = requests.get(url=TEST_HTTP_HEADER, headers=headers, proxies=proxies, timeout=timeout)
        lg.info(str(response.text))
        if response.ok:
            content = json_2_dict(json_str=response.text)
            proxy_connection = content.get('headers', {}).get('Proxy-Connection', None)
            lg.info('Proxy-Connection: {}'.format(proxy_connection))
            ip = content.get('origin', '')
            if ',' in ip:           # 两个ip, 匿名度: 透明
                pass
            elif proxy_connection:
                pass
            else:                   # 只抓取高匿名代理
                lg.info(str('成功捕获一只高匿ip: {}'.format(proxy)))
                return True
        else:
            pass
    except Exception:
        pass

    return res