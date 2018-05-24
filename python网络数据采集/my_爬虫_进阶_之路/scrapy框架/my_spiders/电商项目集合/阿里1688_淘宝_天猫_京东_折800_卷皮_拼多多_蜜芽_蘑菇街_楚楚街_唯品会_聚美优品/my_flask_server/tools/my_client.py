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

import hashlib, datetime, time
import requests
from json import dumps

from my_utils import get_shanghai_time
from my_utils import datetime_to_timestamp

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
# get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))
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

        # NO.3 加密返回签名: signature
        return md5(canonicalized_query_string.encode('utf-8')).lower()

    def make_url(self, params=None):
        """生成请求参数
        @param params dict: uri请求参数(不包含公共参数)
        """
        if not isinstance(params, dict):
            raise TypeError("params is not a dict")

        # 获取当前时间戳
        timestamp = get_current_timestamp() - 5
        # 设置公共参数
        public_params = {
            'access_key_id': self._access_key_id,
            'version': self._version,
            'timestamp': timestamp,
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
        # link中不能呆&否则会被编码在sign中加密
        goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198'

        params = {
            'goods_link': goods_link,
        }

        print(self.make_url(params))
        # url = 'http://127.0.0.1:5000/basic_data_2?' + self.make_url(params)
        url = 'http://127.0.0.1:5000/api/goods?' + self.make_url(params)

        result = requests.get(url)
        print(result.text)

        return result

m = RequestClient()
m.request()