# coding:utf-8

'''
@author = super_fazai
@File    : 截获response_demo.py
@Time    : 2017/4/27 10:04
@connect : superonesfazai@gmail.com
'''

"""
移动端https抓取: mitm.it下载认证插件
fn+鼠标左键来copy
启动方式:
    mitmproxy -s 截获response_demo.py
"""

from mitmproxy import flow
from mitmproxy import ctx
from mitmproxy import http
from mitmproxy import flowfilter

import random
import sys, os
from mitmproxy import io, http
import typing  # noqa

class Writer:
    def __init__(self, path: str) -> None:
        self.f: typing.IO[bytes] = open(path, "wb")
        self.w = io.FlowWriter(self.f)

    def response(self, flow: http.HTTPFlow) -> None:
        if random.choice([True, False]):
            self.w.add(flow)

    def done(self):
        self.f.close()

# path = os.path.dirname(__file__) + '/tmp_flow.txt'
# # print(path)
# addons = [Writer(path=path)]

class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

addons = [
    Counter(),
]

def request(flow: http.HTTPFlow):
    # redirect to different host
    if flow.request.pretty_host == "log.snssdk.com":
        # flow.request.host = "mitmproxy.org"
        with open('/Users/afa/myFiles/my_spider_logs/tmp/tmp_flow.txt', 'w') as f:
            f.write(flow.response.text)

    # answer from proxy
    # elif flow.request.path.endswith("/brew"):
    #     flow.response = http.HTTPResponse.make(
    #         418, b"I'm a teapot",
    #     )

def response(flow):
    response = flow.response
    info = ctx.log.info
    # info(str(response.status_code))
    # info(str(response.headers))
    # info(str(response.cookies))
    info(str(response.text))


