# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
import re
import requests

goods_id = '17983261076'
url = 'https://m.1688.com/offer/556500145489.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'm.1688.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',      # 随机一个请求头
}

def get_requests_body(self, tmp_url, my_headers):
    '''
    根据url和请求头返回body
    :param tmp_url: 待请求的url
    :param my_headers: 请求头
    :return: list   ['xxxx']
    '''
    # 设置代理ip
    self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
    self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

    tmp_proxies = {
        'http': self.proxy,
    }
    # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

    tmp_headers = my_headers
    tmp_host = re.compile(r'https://(.*?)/.*').findall(tmp_url)[0]  # 得到host地址
    # print(tmp_host)
    tmp_headers['Host'] = str(tmp_host)
    try:
        response = requests.get(tmp_url, headers=tmp_headers, proxies=tmp_proxies,
                                timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        data = response.content.decode('utf-8')
        # print(data)
        data = re.compile(r'(.*)').findall(data)  # 贪婪匹配匹配所有
        # print(data)

    except Exception:
        print('requests.get()请求超时....')
        print('data为空!')
        return []

    return data

response = requests.get(url, headers=headers)
print(response.content.decode('utf-8'))
# print(str(response.cookies.get('sid')))