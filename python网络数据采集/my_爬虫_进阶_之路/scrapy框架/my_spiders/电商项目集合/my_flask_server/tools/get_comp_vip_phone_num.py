# coding:utf-8

'''
@author = super_fazai
@File    : get_comp_vip_phone_num.py
@Time    : 2018/5/2 11:59
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')
import requests
from scrapy.selector import Selector
import re

from fzutils.spider.fz_requests import MyRequests

cookies = {
    'gdxidpyhxdE': 'u5aa66T4Nx0KOJ621ZrYYxtam%2BA3Ql4vKG%2BkEl4q3GH29HkPjkCV23BcZb5pZ1NgCWC5MhUhZ9ktB%2FoT702EVn4fCG1HR0NLSJ6HA5MyE7NY01MgoRT1%5CK2D14lyKcjz8jQuak%5Cf%5Cn0baQN4qZ1TsLKEIK6BvO7DREAWTzHm789nzpX7%3A1525231023364',
    '_9755xjdesxxd_': '32',
    '.ASPXAUTH': '71E37172862AE358ADD70D28D75DC242351091D4D2151F15C4B762A9956301C22E368BE890AA25AA8B57AD66A0EAD1F7F1DC6D9C18A7C71F1F8980580BE59D3375C10CCD852A149F5FDD32B4EC25A23896B7771886D761650E99861948A9DAC729BB1C123403C29FEAB3EA7BCC8DE4688907AA71FA86FE8223DCC240DAABEC4CF7FC20E9BF200173D5AFC596D2198E2DE2F779A135291AC5CEEAEDC571163C533061047E1F7137DE74EC18F3A28A47A73C549ABFB39AAA1B35FE05136E22BFAD76675E90',
}

headers = {
    'Proxy-Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://admin.k85u.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://admin.k85u.com/Member/MemList.aspx',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

_result = []

def _set_params(page):
    data = [
        ('__EVENTTARGET', 'ctl00$ContentPlaceHolder1$pager'),
        # ('__EVENTARGUMENT', '4'),
        ('__EVENTARGUMENT', str(page)),
        ('__VIEWSTATE',
         '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'),
        ('__EVENTVALIDATION',
         '/wEdAEm409yNfT0Mh6AeJGpBHEihl3dsNNwvaIOcM9O85pmdrwU/dxlpr4xaPeC4tmgJSkXNF4sFxOyerkXP0xK1St5JnhcJdDWByyx3XjQoOzBhU0SpK+9wAHU7pCpmNtLQ9X1NPgWQs8iKXjgD0reG+ZECaPXIdhR43W1o1ku40VUX9+eT7ujWUwBcwNnq7wtHbvTqQ/ivv3AZNf96W8FFgi8E1Kh/yl3egIdt5QIrovDv67EHyjO0TQLd7tTP00kZpAZ9Cn0eO52zltFN5KoBKdaDAEKsCC8a1jVaQDwq2lBzcKa7lksFdhJ+FwXCQTBgakILSVpxAtnxS9j7oQW7ykAVOJ38R35ARgdv8AJb6tp43Y5fZQPiuXEeDqcDIERqA95CTDibU4CrYoGuKzlLiaQTZB7pIUVbj9KJcnpEeyfsotvNPGeDCouUfBsqf8mAAZXr+L1yo0o9qQWwYxWFWqy3RAqYCQS7RuoD156VttsYth9OqL36qxb0zi3EV74veRDEUw3Tsoga1A3rUMuYy7GI6yumREmYS5FkTU3fXLFnCnwbHug5/7CRLXGY30FojE0k30j0KDJonuO5rF9X4tLhF3eWSTLtyRkUCL+6KUdJf52QC4GtMIwjrph2Zz+wiy4NFV+6RH7QHdutNeJJKJZZjH9RZQIWzGrfO0ubKwzLW+MZ0N2WwFtp/RAteP1TTbt6c0ojrtKE3dthibOJxMG6IcaEVkQ0L0xgFqeczzh4Vxh0siPWLYXC5fxdRr2LoaEZxycrw+CRn0aF7bQK+shsV8f0JdJ7rE6ZyGkPt2yVZDcxdeTFDyIV8ZUJX8SSD2ChG1ecDiKLoKQ9nIAZ5ebSZnSoo8K3036AWuCVV0cktLS6AGtKSRMCcEPHvsfoful2uCTm1MBECx5opBE1enN/O9TkYbuyoXvSjqIZG+SfSIQr7Rb3hx7bdN9PTCSAdHhB9MuB6tiVML/P69z0D3Iba8yg0Yjqm0HtRuLCt6f1R15CgHMCKD5j5yfbkXh1xQ248w1QQX0WPNJNhNniX/4orZJlj3tcqx6Of9ePiikLWPtFuCvumOw/4xiSl5W1ybChnXvB4rxBm4T8MmhMehrQmIfg5K5LSZx5QTOORrRKlONtg3dNltngt1Ov6JyccT4ilY+bkCBVwLXhhp9S//v9tVNH/E7TTZjJgdcMJHdhzGkjJhdBjueGJvnkgtsCqDV4EVo3PVIR7JUFWUSXrTBs318bza4cbQkv/RHdFLum+s2Qsn+G+dbupcVos8bFi4dywkdemLq7j5NKNjyqBR/VSzCHFvl+NMKeDeMusft7i0/jrJfrQcC4bfk5q7I0KKDz1jyTlhODmbTmGrAKXR1+sk1JS7Y4q5Mom+WQSOeWI/BtC8S6pbPRAlj5EQagiDQGJ296qAOIhzTJmAW6GkEdBTHAjHaIemujv7XL2QUN69srKYCcYodHviM7ReR4XbWVgRwWXkAIaeCMJfkpx+TQGDFLCkgI79xEQZXjDU9Afa82XxLyvyjui8ryScQqmQI3oORO8McqUc37Vky2ZDXx2rLdDqmyhAE8dH6Szc4KRahvG8g='),
        ('ctl00$ContentPlaceHolder1$txtMobile', ''),
        ('ctl00$ContentPlaceHolder1$txtUserID', ''),
        ('ctl00$ContentPlaceHolder1$ddlType', ''),
        ('ctl00$ContentPlaceHolder1$ddlFromType', ''),
        ('ctl00$ContentPlaceHolder1$txtRealName', ''),
        ('ctl00$ContentPlaceHolder1$txtIDCard', ''),
        ('ctl00$ContentPlaceHolder1$txtParentID', ''),
        ('ctl00$ContentPlaceHolder1$txtNickName', ''),
        ('ctl00$ContentPlaceHolder1$txtBalanceMin', ''),
        ('ctl00$ContentPlaceHolder1$txtBalanceMax', ''),
        ('ctl00$ContentPlaceHolder1$txtIntergralMin', ''),
        ('ctl00$ContentPlaceHolder1$txtIntergralMax', ''),
        ('ctl00$ContentPlaceHolder1$applStartDate', ''),
        ('ctl00$ContentPlaceHolder1$applEndDate', ''),
        ('ctl00$ContentPlaceHolder1$ddlIsAuthenticate', ''),
        ('ctl00$ContentPlaceHolder1$txtStartAuthenticateDate', ''),
        ('ctl00$ContentPlaceHolder1$txtEndAuthenticateDate', ''),
        ('ctl00$ContentPlaceHolder1$ddlIsSvip', ''),
        # ('ctl00$ContentPlaceHolder1$pager_input', '3'),
        ('ctl00$ContentPlaceHolder1$pager_input', str(page-1)),
    ]

    return data

def _wash_data(data):
    data = re.compile('\r').sub('', data)
    data = re.compile('\n|  ').sub('', data)

    return data

def _get_data():
    # for page in range(1, 22218):
    for page in range(1, 200):
        print('正在抓取第 {0} 页'.format(page))
        url = 'http://admin.k85u.com/Member/MemList.aspx'
        response = requests.post(url=url, headers=headers, cookies=cookies, data=_set_params(page))
        body = response.text

        # body = MyRequests.get_url_body(url=url, params=data, headers=headers)
        # print(body)

        phone_num = Selector(text=body).css('tbody tr td:nth-child(3)::text').extract()
        # print(phone_num)

        for item in phone_num:
            item = _wash_data(data=item)
            if len(item) == 11 and item != '':
                _result.append(item)

            print(item)

        if page == 1000:
            break

_get_data()
print('\n\n\n\n')

_result = list(set(_result))
with open('./phone.txt', 'a') as f:
    for item in _result:
            f.write(str(item) + '\n')

