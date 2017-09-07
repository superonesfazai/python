# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
BOT_NAME = 'itjuzi'

SPIDER_MODULES = ['itjuzi.spiders']
NEWSPIDER_MODULE = 'itjuzi.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# REDIS_START_URLS_AS_SET = True

COOKIES_ENABLED = False

DOWNLOAD_DELAY = 1.5

# 支持随机下载延迟
RANDOMIZE_DOWNLOAD_DELAY = True

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

DOWNLOADER_MIDDLEWARES = {
    # 该中间件将会收集失败的页面，并在爬虫完成后重新调度。（失败情况可能由于临时的问题，例如连接超时或者HTTP 500错误导致失败的页面）
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 80,

    # 该中间件提供了对request设置HTTP代理的支持。您可以通过在 Request 对象中设置 proxy 元数据来开启代理。
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,

    'itjuzi.middlewares.RotateUserAgentMiddleware': 200,
}

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
