# coding:utf-8

'''
@author = super_fazai
@File    : my_requests.py
@Time    : 2017/3/22 10:13
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

import requests
from random import randint
from ..ip_pools import (
    MyIpPools,
    ip_proxy_pool,
    fz_ip_pool,)
from ..internet_utils import get_base_headers
from ..common_utils import _print
import re
import gc
from pprint import pprint

__all__ = [
    'MyRequests',
    'Requests',
]

class MyRequests(object):
    def __init__(self):
        '''
        :param high_conceal: 代理是否高匿
        '''
        super(MyRequests, self).__init__()

    @classmethod
    def get_url_body(cls,
                     url,
                     use_proxy=True,
                     headers:dict=get_base_headers(),
                     params=None,
                     data=None,
                     cookies=None,
                     had_referer=False,
                     encoding='utf-8',
                     method='get',
                     timeout=12,
                     num_retries=1,
                     high_conceal=True,
                     ip_pool_type=ip_proxy_pool):
        '''
        根据url得到body
        :param url:
        :param use_proxy: 是否使用代理模式, 默认使用
        :param headers:
        :param params:
        :param data:
        :param cookies:
        :param had_referer:
        :param encoding:
        :param method:
        :param timeout:
        :param num_retries:
        :param high_conceal: 代理是否为高匿名
        :return: '' 表示error | str 表示success
        '''
        if use_proxy:
            # 设置代理ip
            tmp_proxies = cls._get_proxies(ip_pool_type=ip_pool_type, high_conceal=high_conceal)
            if tmp_proxies == {}:
                print('获取代理失败, 此处跳过!')
                return ''
            # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(tmp_proxies.get('http')))
        else:
            tmp_proxies = {}

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        with requests.session() as s:
            try:
                response = s.request(method=method, url=url, headers=tmp_headers, params=params, data=data, cookies=cookies, proxies=tmp_proxies, timeout=timeout)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                # print(str(response.url))
                try:
                    _ = response.content.decode(encoding)
                except Exception:   # 报编码错误
                    _ = response.text
                body = cls._wash_html(_)
                # print(str(body))

            except Exception as e:
                # print(e)
                if num_retries > 1:
                    return cls.get_url_body(method=method, url=url, headers=tmp_headers, params=params, data=data, cookies=cookies, had_referer=had_referer, encoding=encoding, timeout=timeout, num_retries=num_retries-1)
                else:
                    print('requests.get()请求超时....')
                    print('data为空!')
                    body = ''

        return body

    @classmethod
    def _wash_html(cls, body):
        body = re.compile('\t|  ').sub('', body)
        body = re.compile('\r\n').sub('', body)
        body = re.compile('\n').sub('', body)

        return body

    @classmethod
    def _get_proxies(cls, ip_pool_type=ip_proxy_pool, high_conceal=True):
        '''
        得到单个代理ip
        :return: 格式: {'http': ip+port}
        '''
        ip_obj = MyIpPools(type=ip_pool_type, high_conceal=high_conceal)
        proxies = ip_obj.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        try:
            proxy = proxies.get('http', None)[randint(0, len(proxies) - 1)]
        except TypeError:
            return {}

        tmp_proxies = {
            'http': proxy,
        }

        return tmp_proxies

    def __del__(self):
        gc.collect()

class Requests(MyRequests):
    '''改名'''
    pass