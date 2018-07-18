# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')
from fzutils.spider.fz_requests import MyRequests

# img_url 在e里
# var e = this.props.el;
# arguments里面

import time
from fzutils.common_utils import get_random_int_number
from fzutils.internet_utils import get_random_pc_ua

url = "https://www.xiaohongshu.com/wx_mp_api/sns/v1/homefeed"

t = str(time.time())[:10] + '.' + str(get_random_int_number(start_num=90, end_num=99)) + '00'
print(t)
querystring = {
    "sid":"session.1210427606534613282",    # 定值
    "oid":"homefeed_recommend",
    # "cursor_score":"1531871080.9900",
    "cursor_score": t,
}

headers = {
    'Accept': "*/*",
    'Accept-Encoding': "br, gzip, deflate",
    'Connection': "keep-alive",
    'Referer': "https://servicewechat.com/wxffc08ac7df482a27/55/page-frame.html",
    'Content-Type': "application/json",
    'Host': "www.xiaohongshu.com",
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/6.7.0 NetType/WIFI Language/zh_CN",
    'Accept-Language': "zh-cn",
    'Cache-Control': "no-cache",
    # 'Postman-Token': "d7e74720-8271-42ac-8ff2-8f621d84cf83"
    }

# response = requests.request("GET", url, headers=headers, params=querystring)
# print(response.text)
body = MyRequests.get_url_body(url=url, headers=headers, params=querystring)
# print(body)

share_id = '5b4de55c910cf646dba851a9'
# share_id = '5b46ca07910cf60eb7031af7'
url = "https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/" + share_id

querystring = {
    "sid":"session.1210427606534613282",    # 对方服务器用来判断登录是否过期
}

headers = {
    'Accept': "*/*",
    'Accept-Encoding': "br, gzip, deflate",
    'Connection': "keep-alive",
    # 'Referer': "https://servicewechat.com/wxffc08ac7df482a27/55/page-frame.html",
    'Content-Type': "application/json",
    'Host': "www.xiaohongshu.com",
    # 'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/6.7.0 NetType/WIFI Language/zh_CN",
    'user-agent': get_random_pc_ua(),
    'Accept-Language': "zh-cn",
    'Cache-Control': "no-cache",
    # 'Postman-Token': "505b2e24-bd72-4c28-8b67-ff166e2b24e2"
}

body = MyRequests.get_url_body(url=url, headers=headers, params=querystring)
print(body)