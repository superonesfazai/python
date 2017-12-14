# coding:utf-8

'''
@author = super_fazai
@File    : test_微博认证.py
@Time    : 2017/9/27 15:58
@connect : superonesfazai@gmail.com
'''

import requests
from pprint import pprint
import json
import re
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=utf-8',
    'Host': 'd.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'cookie': 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; wvr=6; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=6c2521139641765552eaeffdc3bc61bb; cross_origin_proto=SSL; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; _s_tentry=login.sina.com.cn; UOR=developer.51cto.com,widget.weibo.com,www.google.com.hk; Apache=5561465425422.705.1506498709692; ULV=1506498709703:7:4:1:5561465425422.705.1506498709692:1506162530082; SSOLoginState=1506498732; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHYuqSfdfkuLvgn1Aleex5zsmmnegsTlkWruzgTjSBrPw.; SUB=_2A250zyj_DeRhGeNM41sX8ybLzjmIHXVXvR03rDV8PUNbmtBeLWfskW9ZsO0IUPFMAeSGgnp47TqH60IC6g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=0RyqLwWNEb6XCS; ALF=1538034730; un=15661611306; wb_cusLike_5289638755=N; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295'
}

a = ['<strong class="W_f16">131</strong>',
 '<strong class="W_f16">432593</strong>',
 '<strong class="W_f16">51854</strong>']

tmp = re.compile(r'<strong .*?>(.*?)</strong>').findall(str(a))
print(tmp)

# 认证类型一般个人认证都是加的黄“V”，企业与政府类认证是蓝“V”

# verify_type_url = 'http://club.weibo.com/intro?from=profile&wvr=6&loc=darenicon'  # 微博达人
# verify_type_url = 'http://verified.weibo.com/verify?from=profile'     # 个人
verify_type_url = 'http://company.verified.weibo.com/verify/orgapply?from=profile'  # 企业
result = re.compile(r'http://(.*?).weibo.com.*?').findall(verify_type_url)[0]
if len(result) == 8:
    verify_type = '个人黄V认证'
    print('=' * 12 + '| 个人黄V认证 |')
elif len(result) == 4:
    verify_type = '微博达人认证'      # 微博达人自2017年5月15日停止申请，达人产品同日下线
    print('=' * 12 + '| 微博达人认证 |')
elif len(result) == 16:
    print('=' * 12 + '| 企业蓝V认证 |')
    verify_type = '企业蓝V认证'

level_before = 'Lv.0'
level = re.compile(r'Lv.(*?)').findall(level_before)[0]
print(level)

tmp_personal_deal_info_url = '/p/1005056040160273/info?mod=pedit_more'
# tmp_personal_deal_info_url = '//weibo.com/1618051664/about'

tmp_url = re.compile(r'//weibo.com/').findall(tmp_personal_deal_info_url)
print(tmp_url)
if tmp_url == []:
    personal_deal_info_url = 'https://weibo.com' + tmp_personal_deal_info_url
else:
    personal_deal_info_url = 'https:' + tmp_personal_deal_info_url
print(personal_deal_info_url)


# response = requests.get(url, headers=headers)

# pprint(response.text)
# pprint(response.text)

