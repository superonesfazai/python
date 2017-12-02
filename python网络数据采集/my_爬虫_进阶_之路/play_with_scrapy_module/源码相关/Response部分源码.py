# coding = utf-8

'''
@author = super_fazai
@File    : Response部分源码.py
@Time    : 2017/9/2 17:16
@connect : superonesfazai@gmail.com
'''

# 部分代码
class Response(object_ref):
    def __init__(self, url, status=200, headers=None, body='', flags=None, request=None):
        self.headers = Headers(headers or {})
        self.status = int(status)
        self._set_body(body)
        self._set_url(url)
        self.request = request
        self.flags = [] if flags is None else list(flags)

    @property
    def meta(self):
        try:
            return self.request.meta
        except AttributeError:
            raise AttributeError("Response.meta not available, this response " \
                "is not tied to any request")


'''
大部分参数和Request的差不多：
    status: 响应码
    _set_body(body)： 响应体
    _set_url(url)：响应url
    self.request = request
'''