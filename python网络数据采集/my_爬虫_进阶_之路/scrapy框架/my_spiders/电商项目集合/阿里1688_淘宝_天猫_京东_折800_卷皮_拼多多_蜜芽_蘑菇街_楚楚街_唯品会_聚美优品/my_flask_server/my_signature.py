# coding:utf-8

'''
@author = super_fazai
@File    : my_signature.py
@Time    : 2017/6/15 15:55
@connect : superonesfazai@gmail.com
'''

"""
    Signature by super_fazai
    ~~~~~~~~~~~~~~

    Api签名认证
"""

from functools import wraps
from flask import request, jsonify
import hashlib, time, datetime
from pprint import pprint

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,
)

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()

class Signature(object):
    """ 接口签名认证 """
    def __init__(self, logger=None):
        self._version = "v1"
        self._access_keys = [
            {"access_key_id": "yiuxiu", "access_key_secret": "yiuxiu6688"}
        ]
        self._timestamp_expiration = 40     # 时间戳有效时长，单位秒
        self.my_lg = logger

    def _check_req_timestamp(self, req_timestamp):
        """ 校验时间戳
        @pram req_timestamp str, int: 请求参数中的时间戳(10位)
        """
        if len(str(req_timestamp)) == 10:
            req_timestamp = int(req_timestamp)
            self.now_timestamp = datetime_to_timestamp(get_shanghai_time())
            if self.now_timestamp-req_timestamp == 28805:   # 单独处理相差8 hour的请求(加拿大服务器问题)
                req_timestamp += 28805

            if req_timestamp <= self.now_timestamp and req_timestamp+self._timestamp_expiration >= self.now_timestamp:
                return True

        return False

    def _check_req_accesskey_id(self, req_accesskey_id):
        """ 校验accesskey_id
        @pram req_accesskey_id str: 请求参数中的用户标识id
        """
        if req_accesskey_id in [ i['access_key_id'] for i in self._access_keys if "access_key_id" in i ]:
            return True

        return False

    def _get_accesskey_secret(self, accesskey_id):
        """ 根据accesskey_id获取对应的accesskey_secret
        @pram accesskey_id str: 用户标识id
        """
        return [i['access_key_secret'] for i in self._access_keys if i.get('access_key_id') == accesskey_id][0]

    def _sign(self, parameters):
        """ MD5签名
        @param parameters dict: 除signature外请求的所有查询参数(公共参数和私有参数)
        """
        # pprint(parameters)
        if 'sign' in parameters:
            parameters.pop("sign")

        access_key_id = parameters.get('access_key_id')
        sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        self.my_lg.info(str(sorted_parameters))
        canonicalized_query_str = ''
        for (k, v) in sorted_parameters:
            canonicalized_query_str += k + "=" + v + "&"

        canonicalized_query_str += self._get_accesskey_secret(access_key_id)
        self.my_lg.info(str(canonicalized_query_str))
        signature = md5(canonicalized_query_str.encode('utf-8')).lower()

        return signature

    def _verification(self, req_params):
        """ 校验请求是否有效
        @param req_params dict: 请求的所有查询参数(公共参数和私有参数)
        """
        res = dict(msg=None, success=False)
        try:
            req_version = req_params["version"]
            req_timestamp = req_params["timestamp"]
            req_accesskey_id = req_params["access_key_id"]
            req_signature = req_params["sign"]
        except KeyError as e:
            res.update(msg="Invalid public params")

        except Exception as e:
            res.update(msg="Unknown server error")

        else:
            # NO.1 校验版本
            if req_version == self._version:
                # NO.2 校验时间戳
                if self._check_req_timestamp(req_timestamp):
                    # NO.3 校验accesskey_id
                    if self._check_req_accesskey_id(req_accesskey_id):
                        # NO.4 校验签名
                        if req_signature == self._sign(req_params):
                            res.update(msg="Verification pass", success=True)

                        else:
                            res.update(msg="Invalid query string")
                    else:
                        res.update(msg="Invalid accesskey_id")
                else:
                    self.my_lg.error('当前系统时间戳为: {0}[{1}], 而请求的时间戳为: {2}[{3}]'.format(
                        self.now_timestamp,
                        str(timestamp_to_regulartime(self.now_timestamp)),
                        req_timestamp,
                        str(timestamp_to_regulartime(req_timestamp))))
                    res.update(msg="Invalid timestamp")
            else:
                res.update(msg="Invalid version")

        return res

    def signature_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            params = request.args.to_dict()
            res = self._verification(params)
            if res["success"] is True:
                return f(*args, **kwargs)
            else:
                return jsonify(res)

        return decorated_function

