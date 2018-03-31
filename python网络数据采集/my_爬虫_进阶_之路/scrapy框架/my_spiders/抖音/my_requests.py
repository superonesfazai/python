# coding:utf-8

'''
@author = super_fazai
@File    : my_requests.py
@Time    : 2017/3/22 10:13
@connect : superonesfazai@gmail.com
'''

import requests
from random import randint
from my_ip_pools import MyIpPools
import re, gc
from pprint import pprint
import time

__all__ = [
    'MyRequests',
]

class MyRequests(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_url_body(cls, url, headers:dict, params:dict=None, had_referer=False):
        '''
        根据url得到body
        :param tmp_url:
        :return: '' 表示出错退出 | body 类型str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        proxy = proxies['http'][randint(0, len(proxies) - 1)]

        tmp_proxies = {
            'http': proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        s = requests.session()
        try:
            if params is not None:
                response = s.get(url, headers=tmp_headers, params=params, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            else:
                response = s.get(url, headers=tmp_headers, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            body = response.content.decode('utf-8')

            body = re.compile('\t').sub('', body)
            body = re.compile('  ').sub('', body)
            body = re.compile('\r\n').sub('', body)
            body = re.compile('\n').sub('', body)
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            body = ''

        return body

    def __del__(self):
        gc.collect()

def test():
    # url = 'https://aweme.snssdk.com/aweme/v1/feed/?iid=28390621972&device_id=48592631504&os_api=18&app_name=aweme&channel=App%20Store&idfa=DA8C3A83-C08C-4881-86A8-1E67849F5BB2&device_platform=iphone&build_number=17603&vid=855FEC75-BEB7-45A5-BE6A-2699A6864BAC&openudid=c33813d872541f3bfc4ca174d9fbc5e708dd9ec5&device_type=iPhone7,1&app_version=1.7.6&version_code=1.7.6&os_version=11.0&screen_width=1242&aid=1128&ac=WIFI&count=6&feed_style=0&min_cursor=0&pull_type=1&type=0&user_id=93453836807&volume=0.12&mas=000ce38bea727f54ae8158b75752a0fe078fd9580a7637b4db5eb1&as=a1d5150be4e7da403e6109&ts=1522421876'
    url = 'https://aweme.snssdk.com/aweme/v1/feed/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'aweme.snssdk.com',
        'Referer': 'http://s.h5.jumei.com/yiqituan/detail?item_id=ht180321p2453550t4&type=global_deal',
        'User-Agent': 'Aweme/1.7.6 (iPhone; iOS 11.0; Scale/3.00)',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': '__utmz=154994554.1521857121.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);__utmc=154994554;__utmb=154994554.1.10.1521857121;__utma=154994554.1748749410.1521857121.1521857121.1521857121.1;__utmt=1;Hm_lpvt_884477732c15fb2f2416fb892282394b=1521857121;Hm_lvt_884477732c15fb2f2416fb892282394b=1521518580,1521857121;device_platform=other;has_download=1;guide_download_show=1;referer_site_cps=wap_touch_;referer_site=wap_touch_;sid=591dae285c6f5fba895afe3e8688247d;PHPSESSID=591dae285c6f5fba895afe3e8688247d;',
    }

    params = {
        'iid': '28390621972',
        'device_id': '48592631504',
        'os_api':    '18',
        'app_name':    'aweme',
        'channel':    'App Store',
        'idfa': 'DA8C3A83-C08C-4881-86A8-1E67849F5BB2',
        'device_platform':	'iphone',
        'build_number':	'17603',
        'vid':	'855FEC75-BEB7-45A5-BE6A-2699A6864BAC',
        'openudid':	'c33813d872541f3bfc4ca174d9fbc5e708dd9ec5',
        'device_type':	'iPhone7,1',
        'app_version':	'1.7.6',
        'version_code':	'1.7.6',
        'os_version':	'11.0',
        'screen_width':	'1242',
        'aid':	'1128',
        'ac':	'WIFI',
        'count':	'6',
        'feed_style':	'0',
        'min_cursor':	'0',
        'pull_type':	'1',
        'type':	'0',
        'user_id':	'93453836807',
        'volume':	'0.12',
        'mas':	'000ce38bea727f54ae8158b75752a0fe078fd9580a7637b4db5eb1',
        # 'as':	'a1d5150be4e7da403e6109',
        'ts':	'1522421876',
        # 'ts': str(int(time.time())),
    }
    print(str(int(time.time())))
    body = MyRequests().get_url_body(url=url, headers=headers, params=params)
    # print(body)
    try:
        import json
        data = json.loads(body)
        pprint(data)
        print(len(data.get('aweme_list')))
    except: pass

test()
