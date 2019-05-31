# coding:utf-8

'''
@author = super_fazai
@File    : live_room_spider.py
@connect : superonesfazai@gmail.com
'''

"""
直播室spider
"""

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

# pc tb 目标直播室地址
def get_tb_live_info_by_live_url(live_room_url: str) -> dict:
    """
    通过live_url获取tb直播信息
    :return:
    """
    try:
        # 获取live_id
        live_id = re.compile('feedId=(\w+-\w+-\w+-\w+-\w+)').findall(live_room_url)[0]
        print('live_id: {}'.format(live_id))
    except IndexError as e:
        raise e

    referer = 'https://taobaolive.taobao.com/room/index.htm?spm=a21tn.8216370.2278281.2.4e7e5722udgyyX&feedId={}'.format(live_id)
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'user-agent': get_random_pc_ua(),
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': referer,
        'authority': 'taobaolive.taobao.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    s = Requests.get_url_body(
        url=live_room_url,
        headers=headers,
        ip_pool_type=tri_ip_pool,
        num_retries=3,
        get_session=True,)
    s_cookies_dict = s.cookies.get_dict()
    MIDWAY_SESS = s_cookies_dict.get('MIDWAY_SESS', '')
    assert MIDWAY_SESS != ''
    print('MIDWAY_SESS: {}'.format(MIDWAY_SESS))

    # 必须参数
    cookies = {
        'MIDWAY_SESS': MIDWAY_SESS,
    }
    params = (
        ('creatorId', ''),
        ('liveId', live_id),
    )
    url = 'https://taobaolive.taobao.com/api/live_detail/1.0'
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        cookies=cookies,
        ip_pool_type=tri_ip_pool,
        num_retries=3,)
    assert body != ''
    # print(body)
    data = json_2_dict(
        json_str=body,
        default_res={}).get('result', {})
    pprint(data)

    return data

live_room_url = 'https://taobaolive.taobao.com/room/index.htm?spm=a21tn.8216370.2278281.6.1d3e5722mwAgi8&feedId=291c2dba-36fb-45c2-954d-183f8b5e3fdb'
get_tb_live_info_by_live_url(live_room_url=live_room_url)