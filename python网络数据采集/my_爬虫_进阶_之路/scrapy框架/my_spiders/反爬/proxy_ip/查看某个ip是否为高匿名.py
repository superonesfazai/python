# coding:utf-8

'''
@author = super_fazai
@File    : 查看某个ip是否为高匿名.py
@connect : superonesfazai@gmail.com
'''

from requests import session
from scrapy.selector import Selector
from fzutils.internet_utils import get_random_phone_ua

def judge_ip_is_anonymity(ip_address, port):
    '''
    返回当前IP地址(用于判断ip地址是否高匿)
    :param ip_address:
    :param port:
    :return:
    '''
    def _get_proxies():
        return {
            'https': ip_address + ':' + str(port)
        }

    url = 'https://www.whatismybrowser.com/'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_phone_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Referer': 'https://ask.csdn.net/questions/701923',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    with session() as s:
        with s.get(url=url, headers=headers, proxies=_get_proxies(), timeout=10) as response:
            now_ip = Selector(text=response.text).css('div#ip-address:nth-child(2) .detected-column a:nth-child(1) ::text').extract_first() or ''
            return now_ip

# ip_address = '115.237.148.28'
# port = 4267
# res = judge_ip_is_anonymity(ip_address=ip_address, port=port)
# print(res)

# http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=
body = session().get(url='http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=').text
print(body)
