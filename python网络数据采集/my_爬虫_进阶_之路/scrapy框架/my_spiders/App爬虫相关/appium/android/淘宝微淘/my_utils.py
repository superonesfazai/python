# coding:utf-8

'''
@author = super_fazai
@File    : my_utils.py
@Time    : 2018/5/26 10:45
@connect : superonesfazai@gmail.com
'''

import execjs
import json
import time
from random import randint
import re
import requests
from my_ip_pools import MyIpPools
import pytz
import datetime

def get_shanghai_time():
    '''
    时区处理，得到上海时间
    :return: datetime类型
    '''
    # 时区处理，时间处理到上海时间
    # pytz查询某个国家时区
    country_timezones_list = pytz.country_timezones('cn')
    # print(country_timezones_list)

    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time

async def calculate_right_sign(_m_h5_tk: str, data: json):
    '''
    根据给的json对象 data 和 _m_h5_tk计算出正确的sign
    :param _m_h5_tk:
    :param data:
    :return: sign 类型str, t 类型str
    '''
    with open('./js/get_h_func.js', 'r') as f:  # 打开js源文件
        js = f.read()

    js_parser = execjs.compile(js)  # 编译js得到python解析对象
    t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

    # 构造参数e
    appKey = '12574478'
    # e = 'undefine' + '&' + t + '&' + appKey + '&' + '{"optStr":"{\"displayCount\":4,\"topItemIds\":[]}","bizCode":"tejia_003","currentPage":"1","pageSize":"4"}'
    e = _m_h5_tk + '&' + t + '&' + appKey + '&' + data

    sign = js_parser.call('h', e)

    return sign, t

async def get_taobao_sign_and_body(base_url, headers:dict, params:dict, data:json, timeout=13, _m_h5_tk='undefine', session=None, logger=None):
    '''
    得到淘宝带签名sign接口数据
    :param base_url:
    :param headers:
    :param params:
    :param data:
    :param timeout:
    :param _m_h5_tk:
    :param session:
    :return: (_m_h5_tk, session, body)
    '''
    sign, t = await calculate_right_sign(data=data, _m_h5_tk=_m_h5_tk)
    headers['Host'] = re.compile(r'://(.*?)/').findall(base_url)[0]
    params.update({  # 添加下面几个query string
        't': t,
        'sign': sign,
        'data': data,
    })

    # 设置代理ip
    ip_object = MyIpPools()
    proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
    proxy = proxies['http'][randint(0, len(proxies) - 1)]

    tmp_proxies = {
        'http': proxy,
    }

    if session is None:
        session = requests.session()
    else:
        session = session
    try:
        response = session.get(url=base_url, headers=headers, params=params, proxies=tmp_proxies, timeout=timeout)
        _m_h5_tk = response.cookies.get('_m_h5_tk', '')
        _m_h5_tk = _m_h5_tk.split('_')[0]
        # print(s.cookies.items())
        # print(_m_h5_tk)

        body = response.content.decode('utf-8')
        # print(body)

    except Exception as e:
        logger.exception(e)
        _m_h5_tk = ''
        body = ''

    return (_m_h5_tk, session, body)
