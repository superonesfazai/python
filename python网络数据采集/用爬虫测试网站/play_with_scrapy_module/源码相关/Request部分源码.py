# coding = utf-8

'''
@author = super_fazai
@File    : Request部分源码.py
@Time    : 2017/9/2 17:14
@connect : superonesfazai@gmail.com
'''

# 部分代码
class Request(object_ref):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None):

        self._encoding = encoding  # this one has to be set first
        self.method = str(method).upper()
        self._set_url(url)
        self._set_body(body)
        assert isinstance(priority, int), "Request priority not an integer: %r" % priority
        self.priority = priority

        assert callback or not errback, "Cannot use errback without a callback"
        self.callback = callback
        self.errback = errback

        self.cookies = cookies or {}
        self.headers = Headers(headers or {}, encoding=encoding)
        self.dont_filter = dont_filter

        self._meta = dict(meta) if meta else None

    @property
    def meta(self):
        if self._meta is None:
            self._meta = {}
        return self._meta

'''
其中，比较常用的参数：
    url: 就是需要请求，并进行下一步处理的url
    
    callback: 指定该请求返回的Response，由那个函数来处理。
    
    method: 请求一般不需要指定，默认GET方法，可设置为"GET", "POST", "PUT"等，且保证字符串大写
    
    headers: 请求时，包含的头文件。一般不需要。内容一般如下：
            # 自己写过爬虫的肯定知道
            Host: media.readthedocs.org
            User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0
            Accept: text/css,*/*;q=0.1
            Accept-Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3
            Accept-Encoding: gzip, deflate
            Referer: http://scrapy-chs.readthedocs.org/zh_CN/0.24/
            Cookie: _ga=GA1.2.1612165614.1415584110;
            Connection: keep-alive
            If-Modified-Since: Mon, 25 Aug 2014 21:59:35 GMT
            Cache-Control: max-age=0
    
    meta: 比较常用，在不同的请求之间传递数据使用的。字典dict型
    
            request_with_cookies = Request(
                url="http://www.example.com",
                cookies={'currency': 'USD', 'country': 'UY'},
                meta={'dont_merge_cookies': True}
            )
    
    encoding: 使用默认的 'utf-8' 就行。
    
    dont_filter: 表明该请求不由调度器过滤。这是当你想使用多次执行相同的请求,忽略重复的过滤器。默认为False。
    
    errback: 指定错误处理函数
'''