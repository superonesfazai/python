# coding:utf-8

'''
@author = super_fazai
@File    : my_client.py
@connect : superonesfazai@gmail.com
'''

"""
测试server端的接口签名
"""

import sys
sys.path.append('..')

import hashlib
from base64 import b64encode
from requests import get

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,)

class RequestClient(object):
    """ 接口签名client示例 """
    def __init__(self):
        self._version = "v1"
        self._access_key_id = "yiuxiu"
        self._access_key_secret = "22879be192793e9d80289b58a451f857"
        self.md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
        self.get_current_timestamp = lambda: datetime_to_timestamp(get_shanghai_time())

    def _sign(self, parameters:dict) -> str:
        '''
        签名
        :param parameters: url请求参数(包含除signature外的公共参数)
        :return:
        '''
        if "sign" in parameters:
            parameters.pop("sign")

        # NO.1 参数排序(正序)
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])

        # NO.2 排序后拼接字符串
        canonicalized_query_string = ''
        for (k, v) in _my_sorted:
            canonicalized_query_string += '{}={}&'.format(k, v)

        canonicalized_query_string += self._access_key_secret   # eg: access_key_id=yiuxiu&goods_link=aHR0cHM6Ly9oNS5tLnRhb2Jhby5jb20vYXdwL2NvcmUvZGV0YWlsLmh0bT9pZD01NTEwNDc0NTQxOTg=&t=1536802300&v=v1&22879be192793e9d80289b58a451f857

        # NO.3 加密返回签名: sign(小写, md5加密)
        return self.md5(canonicalized_query_string.encode('utf-8')).lower()

    def _request(self) -> str:
        '''
        测试用例
        :return:
        '''
        # NOTICE:
        # goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198&umpChannel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&u_channel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&spm=a2141.8147851.1.1'
        # 由于: link中不能带&否则会被编码在sign中加密, 因此先进行b64encode格式化再decode

        # tb
        # goods_link = 'https://item.taobao.com/item.htm?spm=a219r.lmn002.14.1.3b7e12d56SCJjf&id=575507061506&ns=1&abbucket=16'
        # tm
        goods_link = 'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-16816054130.101.3e6227dfLIwIrR&id=555709593338&rn=2563b85d76e776e4dd26a13103df62bd&abbucket=6'
        # jd
        # goods_link = 'https://item.m.jd.com/ware/view.action?wareId=3713001'
        # goods_link = 'https://item.jd.com/5025518.html'

        now_timestamp = self.get_current_timestamp() - 5
        print('请求时间戳为: {}[{}]'.format(now_timestamp, str(timestamp_to_regulartime(now_timestamp))))
        params = {
            'access_key_id': self._access_key_id,
            'v': self._version,
            't': now_timestamp,
            'goods_link': b64encode(s=goods_link.encode('utf-8')).decode('utf-8'),  # 传str, 不传byte, pc地址或m地址都可, server会识别
        }

        params.update({
            'sign': self._sign(params)
        })

        # url = 'http://127.0.0.1:5000/api/goods'

        # rpc 远程过程调用
        # 淘宝天猫调这个
        url = 'http://spider.taobao_tmall.k85u.com/api/goods'
        # 京东调这个
        # url = 'http://spider.other.k85u.com/api/goods'

        with get(url, params=params) as response:
            res = response.text

        return res

    def __call__(self, *args, **kwargs):
        return self._request()

print(RequestClient()())
