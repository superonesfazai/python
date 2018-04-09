# coding:utf-8

'''
@author = super_fazai
@File    : 解析抖音接口数据.py
@Time    : 2018/4/7 17:11
@connect : superonesfazai@gmail.com
'''

from my_requests import MyRequests
import json
from pprint import pprint

def get_aweme_api_videos_info():
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cache-control': 'max-age=0',
        'authority': 'www.douyin.com',
        'cookie': '_ba=BA0.2-20180330-5199e-OeUxtvwJvy5ElpWGFLId; _ga=GA1.2.390071767.1522391891; sso_login_status=1; tt_webid=6540458660484122126; __tea_sdk__user_unique_id=10_; __tea_sdk__ssid=e88eef4a-ec1f-497d-b2c7-301239bfdc67; login_flag=d6ee54ffebe3021c3fb67ff863970736; sessionid=7bdfd0e36df78f38c25abd13f0eff3cc; uid_tt=644e532b271dae498b62c659de17afdf; sid_tt=7bdfd0e36df78f38c25abd13f0eff3cc; sid_guard="7bdfd0e36df78f38c25abd13f0eff3cc|1522819290|2591999|Fri\\054 04-May-2018 05:21:29 GMT"',
    }

    params = (
        ('user_id', '94470216810'),
        ('max_cursor', '0'),
        ('count', '20'),
    )

    url = 'https://www.douyin.com/aweme/v1/aweme/post/'
    body = MyRequests.get_url_body(url=url, headers=headers, params=params)
    # print(body)

    deal_with_data(body=body)

def deal_with_data(body):
    try:
        data = json.loads(body)
        pprint(data)
    except:
        data = {}
        return {}

get_aweme_api_videos_info()
