# coding:utf-8

'''
@author = super_fazai
@File    : ip_utils.py
@connect : superonesfazai@gmail.com
'''

"""
ip utils
"""

from .common_utils import json_2_dict
from .spider.fz_requests import Requests

__all__ = [
    'get_ip_address_info',              # 获取ip的address信息
    'get_local_external_network_ip',    # 获取本机外网ip地址
]

def get_ip_address_info(ip) -> dict:
    '''
    获取ip的address信息(国家), 可根据需求分装成异步的请求
    :param ip: eg: '123.13.244.44'
    :return:
    '''
    base_url = 'http://ip.taobao.com/service/getIpInfo.php'
    params = (
        ('ip', ip),
    )
    try:
        body = Requests.get_url_body(url=base_url, use_proxy=False, params=params)
        _ = json_2_dict(body).get('data', {})
        country = _.get('country', '')
        assert country != '', '获取到的country为空值!'

        return {
            'ip': ip,
            'country': country,
            'city': _.get('city', ''),
            'isp': _.get('isp', ''),
        }
    except Exception as e:
        raise e

def get_local_external_network_ip() -> str:
    '''
    获取本机外网ip地址
    :return: '' 表示获取失败!
    '''
    url = 'http://httpbin.org/get'
    local_ip = json_2_dict(Requests.get_url_body(use_proxy=False, url=url)).get('origin', '')

    return local_ip

