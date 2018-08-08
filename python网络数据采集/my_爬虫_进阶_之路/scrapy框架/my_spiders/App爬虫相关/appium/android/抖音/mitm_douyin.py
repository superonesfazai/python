# coding:utf-8

'''
@author = super_fazai
@File    : mitm_douyin.py
@Time    : 2017/8/7 16:12
@connect : superonesfazai@gmail.com
'''

"""
启动方式:
    mitmproxy -s mitm_douyin.py
    或者
    mitmweb -s mitm_douyin.py
"""

from mitmproxy import flow
from mitmproxy import ctx
from mitmproxy import http
from mitmproxy import flowfilter

import random
from mitmproxy import io, http
import typing
import os

class Writer:
    def __init__(self, path: str) -> None:
        self.f: typing.IO[bytes] = open(path, "wb")
        self.w = io.FlowWriter(self.f)

    def response(self, flow: http.HTTPFlow) -> None:
        response = flow.response
        info = ctx.log.info
        info(str(response.text))
        info(response.headers)
        if random.choice([True, False]):
            self.w.add(flow)

    def done(self):
        self.f.close()

path = '/Users/afa/myFiles/tmp/douyin_ops.txt'
# addons = [Writer(path=path)]

# with open(path, 'rb') as f:
#     for line in f:
#         print(line.decode())

# https://aweme.snssdk.com/aweme/v1/feed
# def request(flow: http.HTTPFlow):
#     # redirect to different host
#     if flow.request.pretty_host == "aweme.snssdk.com":
#         # flow.request.host = "mitmproxy.org"
#         with open('/Users/afa/myFiles/tmp/tmp_flow.txt', 'w') as f:
#             f.write(flow.response.text)
#
#     # answer from proxy
#     # elif flow.request.path.endswith("/brew"):
#     #     flow.response = http.HTTPResponse.make(
#     #         418, b"I'm a teapot",
#     #     )
#

def response(flow):
    response = flow.response
    request = flow.request
    # info = ctx.log.info
    # info(str(response.status_code))
    # info(str(response.headers))
    # info(str(response.cookies))
    # info(str(response.text))
    # info(request)
    if request.host == 'aweme.snssdk.com':     # 锁定抓取接口
        with open(path, 'a+') as file:
            file.write(response.text + '\n')   # 这样能一行一行写, 避免读取断层



