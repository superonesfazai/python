# coding = utf-8

'''
@author = super_fazai
@File    : spider.py
@Time    : 2017/9/6 12:41
@connect : superonesfazai@gmail.com
'''

"""
设计的这个spider从redis中读取要爬的url,然后执行爬取，
若爬取过程中返回更多的url，那么继续进行直至所有的request完成。
之后继续从redis中读取url，循环这个过程。

分析：在这个spider中通过connect signals.spider_idle信号实现对crawler状态的监视。
当idle时，返回新的make_requests_from_url(url)给引擎，进而交给调度器调度。
"""

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider, CrawlSpider

from . import connection


# Default batch size matches default concurrent requests setting.
DEFAULT_START_URLS_BATCH_SIZE = 16
DEFAULT_START_URLS_KEY = '%(name)s:start_urls'


class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    # Per spider redis key, default to DEFAULT_START_URLS_KEY.
    redis_key = None
    # Fetch this amount of start urls when idle. Default to DEFAULT_START_URLS_BATCH_SIZE.
    redis_batch_size = None
    # Redis client instance.
    server = None

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        return self.next_requests()

    def setup_redis(self, crawler=None):
        """Setup redis connection and idle signal.
        This should be called after the spider has set its crawler object.
        """
        if self.server is not None:
            return

        if crawler is None:
            # We allow optional crawler argument to keep backwards
            # compatibility.
            # XXX: Raise a deprecation warning.
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        settings = crawler.settings

        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', DEFAULT_START_URLS_KEY,
            )

        self.redis_key = self.redis_key % {'name': self.name}

        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")

        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE', DEFAULT_START_URLS_BATCH_SIZE,
            )

        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")

        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s)", self.__dict__)

        self.server = connection.from_settings(crawler.settings)
        # The idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET')
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)

    def make_request_from_data(self, data):
        # By default, data is an URL.
        if '://' in data:
            return self.make_requests_from_url(data)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, data)

    def schedule_next_requests(self):
        """Schedules a request if available"""
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        raise DontCloseSpider


class RedisSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(RedisSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class RedisCrawlSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue when idle."""

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(RedisCrawlSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj

'''
spider的改动也不是很大，主要是通过connect接口，给spider绑定了spider_idle信号，
spider初始化时，通过setup_redis函数初始化好和redis的连接，
之后通过next_requests函数从redis中取出strat url，
使用的key是settings中REDIS_START_URLS_AS_SET定义的
（注意了这里的初始化url池和我们上边的queue的url池不是一个东西，
queue的池是用于调度的，初始化url池是存放入口url的，他们都存在redis中，
但是使用不同的key来区分，就当成是不同的表吧），spider使用少量的start url，
可以发展出很多新的url，这些url会进入scheduler进行判重和调度。
直到spider跑到调度池内没有url的时候，会触发spider_idle信号，
从而触发spider的next_requests函数，再次从redis的start url池中读取一些url。
'''