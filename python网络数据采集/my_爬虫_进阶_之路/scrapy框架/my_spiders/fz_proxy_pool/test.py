# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.internet_utils import get_random_phone_ua
import requests

URL = 'http://m.gx8899.com/'
headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_random_phone_ua(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# response = requests.request("GET", url=URL, headers=headers, proxies={'http': 'http://' + '121.232.147.222:9000'})
# status_code = response.status_code
# body = response.content.decode('gb2312')
# print(body)
# print(status_code)

import requests

cookies = {
    '__cfduid': 'dc9f8c63a3f3293f73f71e781fa1bbe251535712684',
    '_ga': 'GA1.2.1608332475.1535712686',
    '_gid': 'GA1.2.168302170.1535712686',
    '_gat': '1',
}

cookies = {
    'api_uid': 'rBQRnVt84IUW7CwrPBm6Ag==',
    'msec': '1800000',
    'ua': 'Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_13_6)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F68.0.3440.106%20Safari%2F537.36',
    'rec_list_index': 'rec_list_index_jZ2fE1',
    'webp': '1',
    'rec_list': 'rec_list_o1jzS7',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

proxies = {
    'http': 'http://{}:{}'.format('121.232.147.222', 9000),
    'https': 'http://{}:{}'.format('121.232.147.222', 9000),
}
response = requests.get('http://yangkeduo.com/', headers=headers, cookies=cookies, proxies=proxies)
print(response.text)
