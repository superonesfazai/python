# coding:utf-8

'''
@author = super_fazai
@File    : xiuke_list_api_hook.py
@connect : superonesfazai@gmail.com
'''

from requests import session
from requests_toolbelt import MultipartEncoder
from fzutils.spider.fz_requests import Requests

cookies = {
    'yd_cookie': '2369844f-fc3f-42742d88d5deabc0ec65d866d61526e32347',
}
data = MultipartEncoder(
    fields={
        'PageIndex': '1',
        'PageSize': '20',
        'TimesTamp': '1547813627151',
        'UserId': '259146',
        'sign': '42531e765ce3055f25f369db3505db8f'
    }
)
headers = {
    'Host': 'api.yiuxiu.com',
    'accept': 'application/json',
    # 'content-type': 'multipart/form-data; boundary=Boundary+C98168C62FD125E1',
    'content-type': data.content_type,
    # 'token': '',      # jwt token
    'user-agent': 'UUBaoKu/2.2.2 (iPhone; iOS 11.0; Scale/3.00)',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}
url = 'https://api.yiuxiu.com/XiuKe/GetNewXiuKeList'
# body = Requests.get_url_body(
#     method='post',
#     url=url,
#     headers=headers,
#     cookies=None,
#     data=data)
# print(body)

with session() as s:
    resp = s.post(
        url=url,
        headers=headers,
        cookies=None,
        data=data)
    print(resp.text)