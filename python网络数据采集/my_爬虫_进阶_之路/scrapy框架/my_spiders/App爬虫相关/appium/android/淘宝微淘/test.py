# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/5/26 09:47
@connect : superonesfazai@gmail.com
'''

import requests
from pprint import pprint
from json import loads, dumps
import re
import asyncio
from my_logging import set_logger
from logging import INFO, ERROR
from my_utils import (
    get_shanghai_time,
    get_taobao_sign_and_body,
)

MY_SPIDER_LOGS_PATH = '/Users/afa/myFiles/my_spider_logs/电商项目'

my_lg = set_logger(
    log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/微淘/' + str(get_shanghai_time())[0:10] + '.txt',
    console_log_level=INFO,
    file_log_level=ERROR
)

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'accept': '*/*',
    'referer': 'https://market.m.taobao.com/apps/market/content/index.html?ut_sk=1.VmYadv9DXkkDAFZm0VV4JBNq_21380790_1527298517854.Copy.33&params=%7B%22csid%22%3A%2254a52aea54b7c29d289a0e36b2bf2f51%22%7D&wh_weex=true&contentId=200668154273&source=weitao_2017_nocover&data_prefetch=true&suid=3D763077-A7BF-43BC-9092-C17B35E896F9&wx_navbar_transparent=false&wx_navbar_hidden=false&sourceType=other&un=bc80c9f324602d31384c4a342af87869&share_crt_v=1&sp_tk=o6R2Q0ZDMHZvaDBlS6Ok&cpp=1&shareurl=true&spm=a313p.22.68.948703884987&short_name=h.WAjz5RP&app=chrome',
    'authority': 'h5api.m.taobao.com',
    # cookie得注释掉, 否则为非法请求
    # 'cookie': 't=70c4fb481898a67a66d437321f7b5cdf; cna=nbRZExTgqWsCAXPCa6QA5B86; l=AkFBuFEM2rj4GbU8Mjl3KsFo0YZa/7Vg; thw=cn; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _cc_=UIHiLt3xSw%3D%3D; tg=0; enc=OFbfiyN19GGi1GicxsjVmrZoFzlt9plbuviK5OuthXYfocqTD%2BL079G%2BIt4OMg6ZrbV4veSg5SQEpzuMUgLe0w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=763730917900964122; mt=ci%3D-1_1; cookie2=16c0da3976ab60d7c87ef7cea1e83cb2; v=0; _tb_token_=dd9fe0edb4b3; tk_trace=oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJyRfZ0FH5AEyz0CWtQgYlWnUAkbLeBYDpeNMwsdmBZ5GYwOAPdU1B2IUBU8G0MXGQCqFCjZt1pjb2TJN2uXIiZePpK9SWkwA%2FlD1sTTfYGTmnCo0YJ7IAG%2BnJtbITMYZ3mzYjFZtYlGojOqye861%2FNFDJbTR41FruF%2BHJRnt%2BHJNgFj3F7IDGXJCs8K; linezing_session=4ic7MPhjlPi65fN5BzW36xB7_1527299424026Fe7K_1; isg=BDo6U2SENb2uULiLxiJ4XA6ri2ZWbZPa3G9M1kQz602YN9pxLHsO1QBGg8PrpzZd; _m_h5_tk=53d85a4f43d72bc623586c142f0c5293_1527305714711; _m_h5_tk_enc=cc75764d122f72920ae715c9102701a8'
}

# _short_url = 'http://m.tb.cn/h.WAjz5RP'
# _short_url = 'http://m.tb.cn/h.WA6JGoC'
_short_url = 'http://m.tb.cn/h.WA6Hp6H'
response = requests.get(_short_url, headers=headers)

try:
    # 获取短连接的目标地址
    target_url = re.compile('var url = \'(.*?)\';').findall(response.text)[0]
    print(target_url)
except IndexError:
    print('获取target_url的时候IndexError!')
    target_url = ''

try:
    # 得到contentId
    content_id = re.compile('contentId=(\d+)').findall(target_url)[0]
    print(content_id)
except IndexError:
    print('获取content_id时IndexError!')
    content_id = ''

try:
    # 得到csid
    csid = re.compile('csid%22%3A%22(.*?)%22%7D').findall(target_url)[0]
    print(csid)
except IndexError:
    print('获取csid时IndexError')
    csid = ''

async def _get_body():
    base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/'

    data = dumps({
        'businessSpm': '',
        'business_spm': '',
        'contentId': content_id,
        'params': dumps({
            "csid": csid,
        }),
        'source': 'weitao_2017_nocover',
        'track_params': '',
        'type': 'h5',
    })

    params = {
        'AntiCreep': 'true',
        'AntiFlood': 'true',
        'api': 'mtop.taobao.beehive.detail.contentservicenewv2',
        'appKey': '12574478',
        'callback': 'mtopjsonp1',
        # 'data': '{"contentId":"200668154273","source":"weitao_2017_nocover","type":"h5","params":"{\\"csid\\":\\"54a52aea54b7c29d289a0e36b2bf2f51\\"}","businessSpm":"","business_spm":"","track_params":""}',
        'data': data,
        'dataType': 'jsonp',
        'data_2': '',
        'jsv': '2.4.11',
        # 'sign': 'e8cb623e58bab0ceb10e9edffdacd5b2',
        # 't': '1527300457911',
        'type': 'jsonp',
        'v': '1.0'
    }

    result_1 = await get_taobao_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        logger=my_lg
    )
    _m_h5_tk = result_1[0]

    if _m_h5_tk == '':
        print('获取到的_m_h5_tk为空str!')

    # 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
    result_2 = await get_taobao_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        _m_h5_tk=_m_h5_tk,
        session=result_1[1],
        logger=my_lg
    )
    body = result_2[2]

    return body

async def _deal_with_result():
    data = await _get_body()
    if content_id != '' and csid != '':
        try:
            data = re.compile('mtopjsonp1\((.*)\)').findall(data)[0]
        except IndexError:
            print('IndexError')
            data = {}

        try:
            data = loads(data)
            pprint(data)
        except Exception as e:
            print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(_deal_with_result())

