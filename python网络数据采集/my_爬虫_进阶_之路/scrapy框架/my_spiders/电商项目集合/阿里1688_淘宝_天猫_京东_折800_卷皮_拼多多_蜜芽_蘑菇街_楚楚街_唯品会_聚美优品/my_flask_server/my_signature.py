# coding:utf-8

'''
@author = super_fazai
@File    : my_signature.py
@Time    : 2017/6/15 15:55
@connect : superonesfazai@gmail.com
'''

"""
    Signature
    ~~~~~~~~~~~~~~

    Api签名认证
"""

from functools import wraps
from flask import request, jsonify
import hashlib, time, datetime
from my_utils import get_shanghai_time
from my_utils import datetime_to_timestamp
from pprint import pprint

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
# get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))
# 国际化
get_current_timestamp = lambda: datetime_to_timestamp(get_shanghai_time())

class Signature(object):
    """ 接口签名认证 """
    def __init__(self):
        self._version = "v1"
        self._accessKeys = [
            {"access_key_id": "yiuxiu", "access_key_secret": "yiuxiu6688"}
        ]
        # 时间戳有效时长，单位秒
        self._timestamp_expiration = 30

    def _check_req_timestamp(self, req_timestamp):
        """ 校验时间戳
        @pram req_timestamp str, int: 请求参数中的时间戳(10位)
        """
        if len(str(req_timestamp)) == 10:
            req_timestamp = int(req_timestamp)
            now_timestamp = get_current_timestamp()
            if req_timestamp <= now_timestamp and req_timestamp + self._timestamp_expiration >= now_timestamp:
                return True

        return False

    def _check_req_accesskey_id(self, req_accesskey_id):
        """ 校验accesskey_id
        @pram req_accesskey_id str: 请求参数中的用户标识id
        """
        if req_accesskey_id in [ i['access_key_id'] for i in self._accessKeys if "access_key_id" in i ]:
            return True

        return False

    def _get_accesskey_secret(self, accesskey_id):
        """ 根据accesskey_id获取对应的accesskey_secret
        @pram accesskey_id str: 用户标识id
        """
        return [i['access_key_secret'] for i in self._accessKeys if i.get('access_key_id') == accesskey_id][0]

    def _sign(self, parameters):
        """ MD5签名
        @param parameters dict: 除signature外请求的所有查询参数(公共参数和私有参数)
        """
        # pprint(parameters)
        if "sign" in parameters:
            parameters.pop("sign")
        accesskey_id = parameters["access_key_id"]
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k, v) in sortedParameters:
            canonicalizedQueryString += k + "=" + v + "&"

        canonicalizedQueryString += self._get_accesskey_secret(accesskey_id)
        signature = md5(canonicalizedQueryString.encode('utf-8')).lower()

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

