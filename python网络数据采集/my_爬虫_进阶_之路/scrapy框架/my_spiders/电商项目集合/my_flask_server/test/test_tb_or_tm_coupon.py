# coding:utf-8

'''
@author = super_fazai
@File    : test_tb_or_tm_coupon.py
@connect : superonesfazai@gmail.com
'''

"""
测试淘宝or天猫优惠券
"""

from sys import path as sys_path
sys_path.append('..')

from settings import IP_POOL_TYPE

from fzutils.cp_utils import block_get_tb_sign_and_body
from fzutils.common_utils import _print
from fzutils.spider.async_always import *

def get_tm_coupon_by_goods_id(goods_id: str, seller_id: str, seller_type: str, logger=None,) -> dict:
    """
    获取tb or tm 的店铺优惠券
    :param goods_id: 商品id
    :param seller_id: 商家id
    :param seller_type: 商家类型
    :return:
    """
    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,
        upgrade_insecure_requests=False,
        cache_control='',)
    cookies_dict2 = {
        # '_cc_': 'UIHiLt3xSw%3D%3D',
        # '_fbp': 'fb.1.1569654479622.763934285',
        # '_l_g_': 'Ug%3D%3D',
        '_m_h5_tk': '181e4a67e2ecd06869bcdcf64cdc812d_1571310516801',
        '_m_h5_tk_enc': 'e87c0d7deb46fc9f124bcfc0e24d5e1c',
        # '_nk_': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        # '_tb_token_': '359136e938395',
        # '_w_app_lg': '17',
        # 'cna': 'wRsVFTj6JEoCAXHXtCqXOzC7',
        # 'cookie1': 'UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D',
        # 'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
        'cookie2': '18c1dde2a4ca9c7a22eb485c34b50301',
        'csg': 'f45590d8',
        'dnk': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        'enc': 'NMn7zFLrgU6nMXwgPWND42Y2H3tmKu0Iel59hu%2B7DFx27uPqGw349h4yvXidY3xuFC6%2FjozpnaTic5LC7jv8CA%3D%3D',
    }
    data = dumps({
        'itemId': goods_id,
        'sellerType': seller_type,
        'sellerId': seller_id,
        'from': 'detail',
        'ttid': '2017@htao_h5_1.0.0'
    })
    params = tuple_or_list_params_2_dict_params((
        ('jsv', '2.4.11'),
        ('appKey', '12574478'),
        # ('t', '1571303059099'),
        # ('sign', '78b5d79d658c5dce2b800b937a3ab2f5'),
        ('api', 'mtop.tmall.detail.couponpage'),
        ('v', '1.0'),
        ('ttid', '2017@htao_h5_1.0.0'),
        ('type', 'jsonp'),
        ('dataType', 'jsonp'),
        ('callback', 'mtopjsonp8'),
    ))
    params['data'] = data
    url = 'https://h5api.m.taobao.com/h5/mtop.tmall.detail.couponpage/1.0/'

    result_1 = block_get_tb_sign_and_body(
        base_url=url,
        headers=headers,
        params=params,
        data=data,
        timeout=15,
        logger=logger,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=PROXY_TYPE_HTTP,
    )
    _m_h5_tk = result_1[0]
    assert _m_h5_tk != ''

    result_2 = block_get_tb_sign_and_body(
        base_url=url,
        headers=headers,
        params=params,
        data=data,
        timeout=15,
        _m_h5_tk=_m_h5_tk,
        session=result_1[1],
        logger=logger,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=PROXY_TYPE_HTTP,
    )

    body = result_2[2]
    assert body != ''

    coupon_info = json_2_dict(
        json_str=re.compile('\((.*)\)').findall(body)[0],
        logger=logger,
        default_res={},)
    # pprint(coupon_info)

    return coupon_info

# goods_id = '593805583737'
# seller_id = '2219509495'
# seller_type = 'B'
# res = get_tm_coupon_by_goods_id(
#     goods_id=goods_id,
#     seller_id=seller_id,
#     seller_type=seller_type,
# )
# pprint(res)

# method 1, pass
# 天猫m站
# headers = {
#     'authority': 'h5api.m.tmall.com',
#     'cache-control': 'max-age=0',
#     'upgrade-insecure-requests': '1',
#     'user-agent': get_random_phone_ua(),
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-user': '?1',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'sec-fetch-site': 'none',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
# }
#
# # cookie, 必传, 但不需登录, 下面是必传参数, 但是会出现cookie中令牌过期情况, 暂不能解决, pass
# cookie = {
#     '_m_h5_tk': '9c5bd7c8460a8d65c4a6e1f4a3db68e0_1571308865607',
#     '_m_h5_tk_enc': 'df1eba2106dcb737a41f02d9d79482b9',
#     '_tb_token_': '359136e938395',
#     'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
#     'cookie2': '18c1dde2a4ca9c7a22eb485c34b50301',
#     'csg': '97d2688d',
#     'login': 'true',
#     't': '593a350382a4f28aa3e06c16c39febf2',
# }
#
# params = (
#     ('jsv', '2.4.8'),
#     ('appKey', '12574478'),
#     ('t', '1571307211506'),
#     ('sign', 'a73e91bd57f69c7a27e9cc5cb423466c'),
#     ('api', 'mtop.tmall.detail.couponpage'),
#     ('v', '1.0'),
#     ('ttid', 'tmalldetail'),
#     ('type', 'jsonp'),
#     ('dataType', 'jsonp'),
#     ('callback', 'mtopjsonp4'),
#     ('data', '{"itemId":593805583737,"source":"tmallH5"}'),
# )
#
# body = Requests.get_url_body(
#     url='https://h5api.m.tmall.com/h5/mtop.tmall.detail.couponpage/1.0/',
#     headers=headers,
#     params=params,
#     cookies=cookie,
#     ip_pool_type=IP_POOL_TYPE,
#     num_retries=5,)
# print(body)

# method2 pass
# 天猫id 在tb m站打开的
# 天猫m打开方式为: https://m.intl.taobao.com/detail/detail.html?id=593805583737
# cookie必传, 且一会就报session过期要求重新登录, pass

def get_tb_or_tm_shop_coupon_list(shop_id: str, user_id: str, proxy_type=PROXY_TYPE_HTTP, num_retries=5, logger=None,):
    """
    获取tb or tm 店铺的优惠券
    :param shop_id: eg: '370588431'
    :param user_id: eg: '2201637318258'
    :return:
    """
    # 根据手淘app获取店铺信息接口
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Host': 'alisitecdn.m.taobao.com',
        # 'User-Agent': 'iPad7,3(iOS/12.1.4) AliApp(TB/8.4.10) Weex/0.20.0 1536x2048',
        'User-Agent': get_random_phone_ua(),
        'Accept-Language': 'zh-cn',
    }
    params = (
        ('pathInfo', 'shop/index'),
        ('userId', user_id),
        ('shopId', shop_id),
        # ('pageId', '209891880'),
    )
    body = Requests.get_url_body(
        url='https://alisitecdn.m.taobao.com/pagedata/shop/index',
        headers=headers,
        params=params,
        ip_pool_type=IP_POOL_TYPE,
        num_retries=num_retries,
        proxy_type=proxy_type,)
    assert body != ''
    # print(body)

    data = json_2_dict(
        json_str=body,
        default_res={})
    # pprint(data)
    ori_all_module_list = data.get('module', {}).get('moduleList', [])
    # 包含优惠券的list
    ori_module_list_where_contain_coupon = [
        item for item in ori_all_module_list if '优惠券' in item.get('moduleInstantsName', '')]
    # pprint(ori_module_list_where_contain_coupon)

    ori_coupon_list = []
    for item in ori_module_list_where_contain_coupon:
        tmp_ori_coupon_list = item.get('moduleData', {}).get('couponList', [])
        # todo 不处理店铺新客户or会员优惠券
        # 老客户优惠券
        ori_old_buyer_coupon_list = item.get('moduleData', {}).get('oldBuyerCoupon', [])
        # pprint(ori_old_buyer_coupon_list)
        if tmp_ori_coupon_list != []\
                or ori_old_buyer_coupon_list != []:
            for i in (tmp_ori_coupon_list+ori_old_buyer_coupon_list):
                ori_coupon_list.append(i)
        else:
            continue

    # pprint(ori_coupon_list)

    return ori_coupon_list

# shop_id = '113624523'
# user_id = '2219509495'

shop_id = '102574736'
user_id = '1613092465'

# res = get_tb_or_tm_shop_coupon_list(
#     shop_id=shop_id,
#     user_id=user_id,
# )
# pprint(res)

# tmall m站店铺页接口
# cookies = {
#     'isg': 'BPz8CouMjSeoiLn79VJem4qVx52u9aAfq1Y1xdZ9COfKoZwr_gVwr3KXhQ988th3',
#     '_tb_token_': '39b0713e9150e',
#     'cookie2': '1f531228f1eedf067babc5531f83abf8',
#     't': 'd5190c7c310f546afef4c590c7ffe062',
#     '_m_h5_tk': '3e0b554d0fd513b9f8927b49f34792af_1571329719874',
#     '_m_h5_tk_enc': 'c6704024054cc2f8aea4128b70c696d2',
#     'cna': 'W3scFisww1kCASe7yNDxdGFU',
# }
#
# headers = {
#     'Accept': '*/*',
#     'Connection': 'keep-alive',
#     # 'Referer': 'https://yaomai.m.tmall.com/?spm=a222m.7628550.1998338745.2',
#     'Accept-Encoding': 'br, gzip, deflate',
#     'Host': 'h5api.m.tmall.com',
#     'User-Agent': get_random_phone_ua(),
#     'Accept-Language': 'zh-cn',
# }
#
# params = (
#     ('jsv', '2.4.8'),
#     ('appKey', '12574478'),
#     ('t', '1571322369194'),
#     ('sign', '78f58c5e9c28fa21fa4b3b207f37ac84'),
#     ('api', 'mtop.shop.render.getpageview'),
#     ('v', '1.0'),
#     ('type', 'jsonp'),
#     ('dataType', 'jsonp'),
#     ('callback', 'mtopjsonp1'),
#     ('data', '{"userId":"2201637318258","shopId":"370588431","pageId":"209891880","pathInfo":"shop/index","extendParams":"spm:a222m.7628550.1998338745.2;hideHeader:true;"}'),
# )
#
# body = Requests.get_url_body(
#     url='https://h5api.m.tmall.com/h5/mtop.shop.render.getpageview/1.0/',
#     headers=headers,
#     params=params,
#     cookies=cookies,
#     ip_pool_type=IP_POOL_TYPE,
#     num_retries=5,
#     proxy_type=PROXY_TYPE_HTTP,)
# print(body)

def get_tm_ali_pay_small_program_coupon_list(goods_id: str,
                                             seller_id: str,
                                             num_retries=5,
                                             proxy_type=PROXY_TYPE_HTTP,
                                             logger=None) -> list:
    """
    获取tm 支付宝tm小程序优惠券接口
    :param goods_id:
    :param seller_id: eg: '1613092465'
    :return:
    """
    # 支付宝中天猫小程序获取优惠券接口1(测试可行)
    # 下面cookie为必传cookie
    cookies = {
        'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
    }
    headers = {
        'Host': 'detailskip.taobao.com',
        'Accept': '*/*',
        'User-Agent': get_random_phone_ua(),
        'Accept-Language': 'zh-CN,en-US;q=0.8',
    }
    params = (
        ('itemId', goods_id),
        ('sellerId', seller_id),
        ('isPreview', 'false'),
        ('callback', 'jsonp_7768536'),
    )
    body = Requests.get_url_body(
        url='https://detailskip.taobao.com/json/wap/tmallH5Desc.do',
        headers=headers,
        params=params,
        cookies=cookies,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=proxy_type,
        num_retries=num_retries,)
    assert body != ''
    # _print(msg=str(body), logger=logger)

    data = json_2_dict(
        json_str=re.compile('\((.*)\)').findall(body)[0],
        default_res={},)
    # pprint(data)

    return data

# goods_id = '568496189602'
# seller_id = '1613092465'

# goods_id = '593805583737'
# seller_id = '113624523'
#
# res = get_tm_ali_pay_small_program_coupon_list(
#     goods_id=goods_id,
#     seller_id=seller_id,
# )
# pprint(res)

# 支付宝中天猫小程序获取优惠券接口2(测试也行, 先用第一种)
# goods_id = '568496189602'
# # goods_id = '593805583737'
# # cookie必传参数
# cookies = {
#     '_m_h5_tk': 'feed15f6d22dbb91933cf4d82a3be995_1571374867740',
#     '_m_h5_tk_enc': '977f319be8387c4688c1488f5c04885a',
#     't': 'af6e8c161c52768c4525b92996e00559',
#     '_tb_token_': '5836311515469',
#     'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
#     'cookie2': '1b2f953c5054db6218622a3f001e96c2',
# }
# headers = {
#     'Host': 'h5api.m.tmall.com',
#     'Accept': '*/*',
#     'User-Agent': get_random_phone_ua(),
#     'Accept-Language': 'zh-CN,en-US;q=0.8',
# }
# # replace替换必须
# # eg: '{"itemId":568496189602,"source":"tmallH5"}'
# data = dumps({
#     'itemId': int(goods_id),
#     'source': 'tmallH5',
# }).replace(' ', '')
# params = (
#     ('jsv', '2.4.8'),
#     ('appKey', '12574478'),
#     # ('t', '1571368313620'),
#     # ('sign', '8b8bb0053213ec02ea928db251573f73'),
#     ('api', 'mtop.tmall.detail.couponpage'),
#     ('v', '1.0'),
#     ('ttid', 'tmalldetail'),
#     ('type', 'jsonp'),
#     ('dataType', 'jsonp'),
#     ('callback', 'mtopjsonp4'),
#     ('data', data),
# )
#
# body = Requests.get_url_body(
#     url='https://h5api.m.tmall.com/h5/mtop.tmall.detail.couponpage/1.0/',
#     headers=headers,
#     params=params,
#     cookies=cookies,
#     ip_pool_type=IP_POOL_TYPE,
#     num_retries=5,)
# print(body)

def get_tm_ali_pay_small_program_coupon_list2(goods_id: str,
                                              logger=None,
                                              proxy_type=PROXY_TYPE_HTTP) -> list:
    """
    获取tb or tm 的店铺优惠券信息(支付宝tm小程序获取优惠券接口2)
    :param goods_id: 商品id
    :param seller_id: 商家id
    :return:
    """
    headers = {
        'Host': 'h5api.m.tmall.com',
        'Accept': '*/*',
        'User-Agent': get_random_phone_ua(),
        'Accept-Language': 'zh-CN,en-US;q=0.8',
    }
    # replace替换必须
    # eg: '{"itemId":568496189602,"source":"tmallH5"}'
    data = dumps({
        'itemId': int(goods_id),
        'source': 'tmallH5',
    }).replace(' ', '')
    params = tuple_or_list_params_2_dict_params((
        ('jsv', '2.4.8'),
        ('appKey', '12574478'),
        # ('t', '1571368313620'),
        # ('sign', '8b8bb0053213ec02ea928db251573f73'),
        ('api', 'mtop.tmall.detail.couponpage'),
        ('v', '1.0'),
        ('ttid', 'tmalldetail'),
        ('type', 'jsonp'),
        ('dataType', 'jsonp'),
        ('callback', 'mtopjsonp4'),
        ('data', data),
    ))
    params['data'] = data
    url = 'https://h5api.m.tmall.com/h5/mtop.tmall.detail.couponpage/1.0/'

    # https模式下会导致大量的请求失败!!
    result_1 = block_get_tb_sign_and_body(
        base_url=url,
        headers=headers,
        params=params,
        data=data,
        timeout=15,
        logger=logger,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=proxy_type,
    )
    _m_h5_tk = result_1[0]
    assert _m_h5_tk != ''

    result_2 = block_get_tb_sign_and_body(
        base_url=url,
        headers=headers,
        params=params,
        data=data,
        timeout=15,
        _m_h5_tk=_m_h5_tk,
        session=result_1[1],
        logger=logger,
        ip_pool_type=IP_POOL_TYPE,
        proxy_type=proxy_type,
    )
    body = result_2[2]
    assert body != ''
    print(body)

    ori_coupon_info = json_2_dict(
        json_str=re.compile('\((.*)\)').findall(body)[0],
        logger=logger,
        default_res={}, ).get('data', {}).get('coupons', [])
    pprint(ori_coupon_info)

    res = []
    for item in ori_coupon_info:
        item_coupon_list = item.get('couponList', [])
        for i in item_coupon_list:
            if i.get('enabled', 'false') == 'true':
                use_method = ''
                try:
                    # 一个账户优惠券只能使用一次
                    # 优惠券展示名称, eg: '店铺优惠券'
                    coupon_display_name = i.get('couponDisplayName', '')
                    assert coupon_display_name != ''
                    # 优惠券的值, eg: 3(即优惠三元)
                    coupon_value = str(float(i.get('title', '')).__round__(2))
                    assert coupon_value != ''
                    sub_titles = i.get('subtitles', [])
                    assert sub_titles != []
                    # 用法
                    use_method = sub_titles[0]
                    # 使用门槛
                    threshold = str(float(re.compile('满(.*?)元').findall(use_method)[0]).__round__(2))
                    begin_time = str(date_parse(
                        target_date_str=re.compile('有效期(.*?)-').findall(sub_titles[1])[0]))
                    end_time = str(date_parse(
                        target_date_str=re.compile('-(.*)').findall(sub_titles[1])[0]))

                    if string_to_datetime(end_time) <= get_shanghai_time():
                        # 已过期的
                        continue

                    res.append({
                        'coupon_display_name': coupon_display_name,
                        'coupon_value': coupon_value,
                        'use_method': use_method,
                        'threshold': threshold,
                        'begin_time': begin_time,
                        'end_time': end_time,
                    })
                except AssertionError:
                    continue
                except Exception:
                    logger.error('遇到错误[use_method: {}]:'.format(use_method), exc_info=True)
                    continue

    # pprint(res)

    return res

# goods_id = '568496189602'
# get_tm_ali_pay_small_program_coupon_list2(
#     goods_id=goods_id,
# )

def get_tm_coupon_url_from_lq5u(goods_id='',
                                goods_name_or_m_url: str='',
                                proxy_type=PROXY_TYPE_HTTP,
                                num_retries=5,
                                logger=None,) -> str:
    """
    从领券无忧根据goods_name搜索tm优惠券
    :param goods_id: 推荐使用商品id来查券
    :param goods_name_or_m_url: 商品名 or 商品地址
    :return:
    """
    # todo 测试发现无需搜索, 只需把goods_id 改为领券无忧的对应的url即可查询是否有券
    # 基于领券无忧来根据商品名获取其优惠券
    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,
    )
    headers.update({
        'Proxy-Connection': 'keep-alive',
        'Origin': 'http://www.lq5u.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.lq5u.com/',
    })
    # # 只搜索天猫的
    # data = {
    #   'p': '1',
    #   'cid': '0',
    #   'sort': '0',
    #   'b2c': '1',           # '0'为搜索tb, tm | '1'为只搜索tm
    #   'coupon': '1',
    #   'k': goods_name_or_m_url,
    # }
    # body = Requests.get_url_body(
    #     method='post',
    #     url='http://www.lq5u.com/',
    #     headers=headers,
    #     # cookies=cookies,
    #     data=data,
    #     verify=False,
    #     ip_pool_type=IP_POOL_TYPE,
    #     num_retries=num_retries,
    #     proxy_type=proxy_type,)
    # assert body != ''
    # # print(body)
    #
    # lq5u_url_list_sel = {
    #     'method': 'css',
    #     'selector': 'li a ::attr("onmousedown")',
    # }
    # ori_lq5u_url_list = parse_field(
    #     parser=lq5u_url_list_sel,
    #     target_obj=body,
    #     is_first=False,)
    # lq5u_url_list = []
    # for item in ori_lq5u_url_list:
    #     try:
    #         url = re.compile('this.href=\'(.*?)\'').findall(item)[0]
    #         assert url != ''
    #     except Exception:
    #         continue
    #
    #     lq5u_url_list.append('http://www.lq5u.com' + url)
    #
    # assert lq5u_url_list != []
    # pprint(lq5u_url_list)

    # 领券无忧对应页面如下
    # url = 'http://www.lq5u.com/item/index/iid/{}.html'.format(goods_id)
    # body = Requests.get_url_body(
    #     method='get',
    #     url=url,
    #     headers=headers,
    #     verify=False,
    #     ip_pool_type=IP_POOL_TYPE,
    #     num_retries=num_retries,
    #     proxy_type=proxy_type, )
    # assert body != ''
    # print(body)
    #
    # coupon_info_sel = {
    #     'method': 'css',
    #     'selector': 'span.b.red ::text',
    # }
    # coupon_info = parse_field(
    #     parser=coupon_info_sel,
    #     target_obj=body,
    # )
    # if '很遗憾，该商品没有优惠券' in coupon_info:
    #     return []
    # else:
    #     _print(msg='goods_id: {}, 存在优惠券'.format(goods_id), logger=logger)
    #     return []

    # 根据领券无忧接口
    from random import uniform as random_uniform

    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,
    )
    headers.update({
        'Origin': 'http://www.lq5u.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.lq5u.com/item/index/iid/{}.html'.format(goods_id),
        'X-Requested-With': 'XMLHttpRequest',
    })
    params = (
        ('rnd', str(random_uniform(0, 1))),      # eg: '0.4925945510743117'
    )
    data = {
        'iid': goods_id
    }
    body = Requests.get_url_body(
        method='post',
        url='http://www.lq5u.com/item/ajax_get_auction_code.html',
        headers=headers,
        params=params,
        data=data,
        verify=False,
        ip_pool_type=IP_POOL_TYPE,
        num_retries=num_retries,
        proxy_type=proxy_type,)
    assert body != ''
    # print(body)

    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=logger,).get('data', {})
    # pprint(data)

    coupon_url = data.get('coupon_click_url', '')

    if coupon_url != '':
        _print(msg='该goods_id: {} 含 有优惠券'.format(goods_id), logger=logger)
    else:
        _print(msg='该goods_id: {} 不含 有优惠券'.format(goods_id), logger=logger)

    return coupon_url

# 支持地址, goods_name查询
# https://detail.m.tmall.com/item.htm?id=568496189602
# goods_name_or_m_url = 'ADIDAS阿迪达斯NEO卫衣男19秋季新品休闲连帽套衫EI6285 EI6283'
# goods_id = '568496189602'
goods_id = '562016826663'
coupon_url = get_tm_coupon_url_from_lq5u(
    goods_id=goods_id,
)
print('coupon_url: {}'.format(coupon_url))