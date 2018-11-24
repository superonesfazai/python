# coding:utf-8

'''
@author = super_fazai
@File    : socks_demo.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_base_headers

import requests
from base64 import b64encode

socks_host = 'dyn.horocn.com'
socks_port = 50000
socks_username = ''
socks_pwd = ''

headers = get_base_headers()
_ = 'Basic {}'.format(b64encode('{}:{}'.format(socks_username, socks_pwd).encode()).decode())
print(_)
headers.update({
    'Proxy-Authorization': _,
})
proxies = {
    'http': 'socks5://{}:{}@{}:{}'.format(socks_username, socks_pwd, socks_host, socks_port),
    # 'https': 'socks5://{}:{}@{}:{}'.format(socks_username, socks_pwd, socks_host, socks_port),
}
# url = 'https://proxy.horocn.com/api/ip'
url = 'https://httpbin.org/get'
resp = requests.get(url=url, proxies=proxies)
print(resp.text)