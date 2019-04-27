# coding:utf-8

'''
@author = super_fazai
@File    : test_tb_weitao_api.py
@connect : superonesfazai@gmail.com
'''

"""
test: 新版微淘接口!
"""

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

headers = {
    'authority': 'h5api.m.taobao.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': get_random_pc_ua(),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
# 必传参数(无cookies, sign正确也无结果!)
# 而且登录后的cookies, 但是继续采集, tb会报: 亲,访问被拒绝了哦!请检查是否使用了代理软件或VPN哦~
cookies = None
params = (
    ('jsv', '2.5.1'),
    ('appKey', '12574478'),
    # ('t', '1556346986566'),
    # ('sign', '7d02de5b8f8aa106f02dbde9c50b24a5'),
    ('api', 'mtop.taobao.beehive.detail.contentservicenewv2'),
    ('v', '1.0'),
    ('AntiCreep', 'true'),
    ('AntiFlood', 'true'),
    ('type', 'jsonp'),
    ('dataType', 'jsonp'),
    ('callback', 'mtopjsonp1'),
)
content_id = '224209295958'
# 此处可替换 也可不替换' '为''值, 尽管sign 会把' '也加密进去, 可能会与js端有点不同(sign)!
data = dumps({
    'contentId': content_id,
    'source': 'weitao_2017_cover',
    'type': 'h5',
    'params': '',
    'business_spm': '',
    'track_params': '',
})
params = tuple_or_list_params_2_dict_params(params)
base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/'
res1 = block_get_tb_sign_and_body(
    base_url=base_url,
    headers=headers,
    params=params,
    data=data,
    cookies=cookies,
    ip_pool_type=tri_ip_pool,)
_m_h5_tk = res1[0]
# print(_m_h5_tk)

res2 = block_get_tb_sign_and_body(
    base_url=base_url,
    headers=headers,
    params=params,
    data=data,
    cookies=cookies,
    _m_h5_tk=_m_h5_tk,
    session=res1[1],
    ip_pool_type=tri_ip_pool,)
# print(res2)
body = res2[2]
data = json_2_dict(
    json_str=re.compile('\((.*)\)').findall(body)[0],
)
pprint(data)