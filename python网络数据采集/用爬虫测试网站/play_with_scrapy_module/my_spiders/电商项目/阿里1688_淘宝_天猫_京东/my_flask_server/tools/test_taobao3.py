# coding:utf-8

'''
@author = super_fazai
@File    : test_taobao3.py
@Time    : 2017/10/24 20:58
@connect : superonesfazai@gmail.com
'''

import requests
import time
from random import randint
import re
import json
from pprint import pprint
from urllib.request import urlopen, urlparse

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'acs.m.taobao.com',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
}

cookies = {'UM_distinctid': '15f4454692b518-0555f1e7dd4c7e-31657c00-fa000-15f4454692c301',
 '_cc_': 'W5iHLLyFfA%3D%3D',
 '_l_g_': 'Ug%3D%3D',
 '_m_h5_tk': 'ba40d8148652aab780cd0a4676b7de78_1508939525308',
 '_m_h5_tk_enc': '657e3a29d2ed7960fc33a8f5eee71311',
 '_m_unitapi_v_': '1508566261407',
 '_m_user_unitinfo_': 'unit|unshyun',
 '_med': 'dw:1280&dh:800&pw:2560&ph:1600&ist:0',
 '_nk_': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
 '_tb_token_': 'f7737e987379e',
 'cna': 'djtzEjGArAoCAdpsYVInKSbN',
 'cookie1': 'UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D',
 'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
 'cookie2': '77360468af87aa9138fe41cba09c84e4',
 'ctoken': 'WqhCFrPazVHsaXEg4Ehiiceland',
 'hng': 'CN%7Czh-CN%7CCNY%7C156',
 'isg': 'ArGxbJIcTLCyS-C4Z7Kwy0ciwDuLNiWD6R-UZJPGpHiXutEM2O414F_Qrngn',
 'l': 'Alxc7z0vy02Xr2I-uw3Bx6KirHEOlgD/',
 'lgc': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
 'linezing_session': 'YxTaEiFp5PgcCDsDUpv72smj_15089162078677dhg_4',
 'miid': '5163267521302899128',
 'mt': 'np',
 'munb': '2242024317',
 'sg': '%E4%BA%BA73',
 'skt': '46e576256f2dba98',
 't': '39c31685a5f4ebc8b58fb9f880a2c9e9',
 'tg': '0',
 'thw': 'cn',
 'tk_trace': 'oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJyTiWtijRcgaFl%2Bt7JBsrd0YGyuPHsVkeAd5WwiCJZELXrV25ia3NSCCQoIRmoJcswnfVxFDZBU4yg42Wi%2B%2B227Cm3SJ38qWJwfE58EYj5sCqIiLyHliYlQ01CLLl6PZ25m2ii9zafRBPfSCEB1U9B3h11vSg89gGmhxMMPOu1jw2cje1%2BZM3Z0QviQAow%3D',
 'tkmb': 'e',
 'tracknick': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
 'uc1': 'cookie14',
 'uc3': 'sg2',
 'unb': '2242024317',
 'uss': 'WqJ%2BWRrAVClLpjGnzo4H1pA5ModQ2m%2BdZWZS3Had%2Blo508500XLOlKESsQ%3D%3D',
 'v': '0'}


'''
appKey:12574478
t:1508852656200
sign:24b2e987fce9c84d2fc0cebd44be49ef
api:mtop.taobao.detail.getdetail
v:6.0
ttid:2016@taobao_h5_2.0.0
isSec:0
ecode:0
AntiFlood:true
AntiCreep:true
H5Request:true
type:jsonp
dataType:jsonp
callback:mtopjsonp1
data:{"exParams":"{\"id\":\"546756179626\"}","itemNumId":"546756179626"}
'''

def get_goods_data(goods_id):
    '''
    模拟构造得到data的url
    :param goods_id:
    :return: data   类型dict
    '''
    """
    appKey = '12574478'
    t = str(time.time().__round__()) + str(randint(100, 999))    # time.time().__round__() 表示保留到个位
    # sign = '24b2e987fce9c84d2fc0cebd44be49ef'     # sign可以为空
    api = 'mtop.taobao.detail.getdetail'
    v = '6.0'
    ttid = '2016@taobao_h5_2.0.0'
    isSec = str(0)
    ecode = str(0)
    AntiFlood = 'true'
    AntiCreep = 'true'
    H5Request = 'true'
    type = 'jsonp'
    callback = 'mtopjsonp1'
    """

    appKey = '12574478'
    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

    '''
    下面是构造params
    '''
    goods_id = goods_id
    params_data_1 = {
        'id': goods_id
    }
    params_data_2 = {
        'exParams': json.dumps(params_data_1),  # 每层里面的字典都要先转换成json
        'itemNumId': goods_id
    }

    params = {
        'data': json.dumps(params_data_2)  # 每层里面的字典都要先转换成json
    }

    ### * 注意这是正确的url地址: right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
    # right_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508886442888&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22546756179626%5C%22%7D%22%2C%22itemNumId%22%3A%22546756179626%22%7D'
    # print(right_url)


    tmp_url = "https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey={}&t={}&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1".format(
        appKey, t
    )
    response = requests.get(tmp_url, headers=headers, params=params)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
    last_url = re.compile(r'\+').sub('', response.url)  # 转换后得到正确的url请求地址
    # print(last_url)
    response = requests.get(last_url, headers=headers)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
    data = response.content.decode('utf-8')
    # print(data)
    data = re.compile(r'mtopjsonp1\((.*)\)').findall(data)[0]  # 贪婪匹配匹配所有
    data = json.loads(data)
    if data != []:
        data['data']['rate'] = ''  # 这是宝贝评价
        data['data']['resource'] = ''  # 买家询问别人
        data['data']['vertical'] = ''  # 也是问和回答
        data['data']['seller']['evaluates'] = ''  # 宝贝描述, 卖家服务, 物流服务的评价值...
        result_data = data['data']

        # 处理result_data['apiStack'][0]['value']
        # print(result_data['apiStack'][0]['value'])
        result_data_apiStack_value = result_data['apiStack'][0]['value']
        result_data_apiStack_value = json.loads(result_data_apiStack_value)
        result_data_apiStack_value['vertical'] = ''
        result_data_apiStack_value['consumerProtection'] = ''   # 7天无理由退货
        result_data_apiStack_value['feature'] = ''
        result_data_apiStack_value['layout'] = ''
        result_data_apiStack_value['delivery'] = ''             # 发货地到收到地
        # pprint(result_data_apiStack_value)
        result_data['apiStack'][0]['value'] = result_data_apiStack_value

        # 将处理后的result_data['apiStack'][0]['value']重新赋值给result_data['apiStack'][0]['value']
        return result_data
    else:
        print('data为空!')

goods_id = '546756179626'
data = get_goods_data(goods_id=goods_id)
# pprint(data)
# https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508852656200&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data='{"exParams": "{\"id\": \"546756179626\"}", "itemNumId": "546756179626"}'

# https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1508852656200&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data='{"exParams": "{\"id\": \"546756179626\"}", "itemNumId": "546756179626"}'

goodsLink = 'https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w5003-17214421641.7.18523e33avyJ0I&id=560164926470&scene=taobao_shop'
if goodsLink:
    tmp_item = re.compile(r'(.*?)\?.*?').findall(goodsLink)  # 过滤筛选出唯一的阿里1688商品链接
    if tmp_item == []:
        wait_to_deal_with_url = goodsLink
    else:
        wait_to_deal_with_url = tmp_item[0]



