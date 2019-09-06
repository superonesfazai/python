# coding:utf-8

'''
@author = super_fazai
@File    : t_goods.py
@connect : superonesfazai@gmail.com
'''

"""
测试goods
"""

from sys import path as sys_path
sys_path.append('..')

from settings import IP_POOL_TYPE
from multiplex_code import get_tm_m_body_data
from tmall_parse_2 import TmallParse
from taobao_parse import TaoBaoLoginAndParse
from fzutils.spider.async_always import *

def test_tm_m():
    # todo 注意部分商品预售，当前无法购买, 不更新, 待其状态正常后会更新
    goods_id = '43988580669'
    # data = get_tm_m_body_data(goods_id=goods_id)
    # pprint(data)
    pc_url = 'https://detail.tmall.com/item.htm?id={}'.format(goods_id)
    phone_url = 'https://detail.m.tmall.com/item.htm?id={}'.format(goods_id)
    print('pc_url: {}, phone_url: {}'.format(pc_url, phone_url))

    tm = TmallParse(is_real_times_update_call=True)
    goods_id = tm.get_goods_id_from_url(tmall_url=pc_url)
    ori_data = tm.get_goods_data(goods_id=goods_id)
    # pprint(ori_data)
    data = tm.deal_with_data()
    pprint(data)

    try:del tm
    except:pass

def test_tb():
    goods_id = '533127076450'
    pc_url = 'https://item.taobao.com/item.htm?id={}'.format(goods_id)
    phone_url = 'https://h5.m.taobao.com/awp/core/detail.htm?id={}'.format(goods_id)
    print('pc_url: {}, phone_url: {}'.format(pc_url, phone_url))

    tb = TaoBaoLoginAndParse(is_real_times_update_call=True)
    goods_id = tb.get_goods_id_from_url(pc_url)
    ori_data = tb.get_goods_data(goods_id=goods_id)
    # pprint(ori_data)
    data = tb.deal_with_data(goods_id=goods_id)
    pprint(data)

    try:
        del tb
    except:
        pass

def get_tb_m_cookies(goods_id: str) -> dict:
    """
    获取tb m url cookies: 测试发现其值为空
    :param goods_id:
    :return:
    """
    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,)
    headers.update({
        'authority': 'h5.m.taobao.com',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-site': 'none',
    })
    params = (
        ('id', goods_id),
    )
    # 必须
    cookies = {
        # '_m_h5_tk': '18d7e97da9f5c7a9865ea49e46ce461d_1567496859709',
        # '_m_h5_tk_enc': '5b40dd9750869a928ce9d15d01a29d4d',
        '_tb_token_': '35f3ee3da748',
        # 'cna': '',
        'cookie2': '180810809b5c95e08a6c2f3a496fada6',
        # 'enc': '',
        # 'hng': '',
        # 'isg': '',
        # 'l': 'c',
        # 'lid': '',
        't': '593a350382a4f28aa3e06c16c39febf2',
        # 'tracknick': '',
    }
    url = 'https://h5.m.taobao.com/awp/core/detail.htm'
    _s = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        cookies=cookies,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=PROXY_TYPE_HTTPS,
        num_retries=3,
        get_session=True)
    cookies_dict = _s.cookies.get_dict()
    pprint(cookies_dict)

    return cookies_dict

def oo_tb_m(goods_id):
    """
    tb 基础数据接口
    :param goods_id:
    :return:
    """
    headers = {
        'Sec-Fetch-Mode': 'no-cors',
        'Referer': 'https://h5.m.taobao.com/awp/core/detail.htm?id={}'.format(goods_id),
        'User-Agent': get_random_phone_ua(),
    }
    data = dumps({
        'id': goods_id,
         'itemNumId': goods_id,
         'exParams': dumps({
             'id': goods_id,
         }),
         'detail_v': '8.0.0',
         'utdid': '1',
    })
    params = (
        ('jsv', '2.5.1'),
        ('appKey', '12574478'),
        ('t', get_now_13_bit_timestamp()),
        # ('t', '1567673270701'),
        # ('sign', '29e00f8c26cf0598f74147f763148b3a'),
        ('api', 'mtop.taobao.detail.getdetail'),
        ('v', '6.0'),
        ('isSec', '0'),
        ('ecode', '0'),
        ('AntiFlood', 'true'),
        ('AntiCreep', 'true'),
        ('H5Request', 'true'),
        ('ttid', '2018@taobao_h5_9.9.9'),
        ('type', 'jsonp'),
        ('dataType', 'jsonp'),
        ('callback', 'mtopjsonp1'),
        ('data', data),
    )
    url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/'
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=PROXY_TYPE_HTTPS,
        num_retries=5,)
    print(body)

    # _m_h5_tk, _session, body = block_get_tb_sign_and_body(
    #     base_url=url,
    #     headers=headers,
    #     params=tuple_or_list_params_2_dict_params(params),
    #     data=data,
    #     timeout=15,
    #     ip_pool_type=tri_ip_pool,
    #     proxy_type=PROXY_TYPE_HTTPS,
    # )
    # _m_h5_tk, _session, body = block_get_tb_sign_and_body(
    #     base_url=url,
    #     headers=headers,
    #     params=tuple_or_list_params_2_dict_params(params),
    #     data=data,
    #     timeout=15,
    #     _m_h5_tk=_m_h5_tk,
    #     session=_session,
    #     ip_pool_type=tri_ip_pool,
    #     proxy_type=PROXY_TYPE_HTTPS,
    # )
    # print(body)

# test_tm_m()
# test_tb()

# 测试tb m
goods_id = '549903923911'
# get_tb_m_cookies(goods_id=goods_id)
oo_tb_m(goods_id=goods_id)