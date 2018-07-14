# coding:utf-8

'''
@author = super_fazai
@File    : my_client.py
@Time    : 2017/6/15 16:08
@connect : superonesfazai@gmail.com
'''

"""
测试server端的接口签名
"""

import sys
sys.path.append('..')

import hashlib
import time
import requests

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,
)

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
# 国际化
get_current_timestamp = lambda: datetime_to_timestamp(get_shanghai_time())

class RequestClient(object):
    """ 接口签名客户端示例 """
    def __init__(self):
        self._version = "v1"
        self._access_key_id = "yiuxiu"
        self._access_key_secret = "yiuxiu6688"

    def _sign(self, parameters):
        """ 签名
        @param parameters dict: uri请求参数(包含除signature外的公共参数)
        """
        if "sign" in parameters:
            parameters.pop("sign")

        # NO.1 参数排序
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])

        # NO.2 排序后拼接字符串
        canonicalized_query_string = ''
        for (k, v) in _my_sorted:
            canonicalized_query_string += '{}={}&'.format(k,v)

        canonicalized_query_string += self._access_key_secret
        # print(canonicalized_query_string)

        # NO.3 加密返回签名: signature
        return md5(canonicalized_query_string.encode('utf-8')).lower()

    def make_url(self, params=None):
        """生成请求参数
        @param params dict: uri请求参数(不包含公共参数)
        """
        if not isinstance(params, dict):
            raise TypeError("params is not a dict")

        # 设置公共参数
        public_params = {
            'access_key_id': self._access_key_id,
            'version': self._version,
            'timestamp': get_current_timestamp() - 5,
        }
        # 添加公共参数
        for k, v in public_params.items():
            params[k] = v

        uri = ''
        for k, v in params.items():
            uri += '{}={}&'.format(k, v)
        uri += 'sign=' + self._sign(params)

        return uri

    def request(self):
        """测试用例"""
        # goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198&umpChannel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&u_channel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&spm=a2141.8147851.1.1'
        # link中不能带&否则会被编码在sign中加密

        # tb
        # goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198'
        # tm
        goods_link = 'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-16816054130.101.3e6227dfLIwIrR&id=555709593338&rn=2563b85d76e776e4dd26a13103df62bd&abbucket=6'
        # jd
        # goods_link = 'https://item.m.jd.com/ware/view.action?wareId=3713001'
        # goods_link = 'https://item.jd.com/5025518.html'

        from base64 import b64encode

        now_timestamp = get_current_timestamp()-5
        print('请求时间戳为: {0}[{1}]'.format(now_timestamp, str(timestamp_to_regulartime(now_timestamp))))
        params = {
            'access_key_id': self._access_key_id,
            'version': self._version,
            'timestamp': now_timestamp,
            'goods_link': b64encode(s=goods_link.encode('utf-8')).decode('utf-8'),  # 传str, 不传byte
        }

        params.update({
            'sign': self._sign(params)
        })

        # print(self.make_url(params))
        # url = 'http://127.0.0.1:5000/basic_data_2?' + self.make_url(params)
        # url = 'http://127.0.0.1:5000/api/goods'
        url = 'http://spider.taobao_tmall.k85u.com/api/goods'
        # url = 'http://spider.other.k85u.com/api/goods'

        # result = requests.get(url)
        result = requests.get(url, params=params)

        print(result.text)

        return result

m = RequestClient()
m.request()
