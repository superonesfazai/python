# -*- coding: utf-8 -*-

# Scrapy settings for sina_weibo_bozhu_all_weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sina_weibo_bozhu_all_weibo'

SPIDER_MODULES = ['sina_weibo_bozhu_all_weibo.spiders']
NEWSPIDER_MODULE = 'sina_weibo_bozhu_all_weibo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina_weibo_bozhu_all_weibo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sina_weibo_bozhu_all_weibo.middlewares.SinaWeiboBozhuAllWeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'sina_weibo_bozhu_all_weibo.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sina_weibo_bozhu_all_weibo.pipelines.SinaWeiboBozhuAllWeiboPipeline': None,
    'sina_weibo_bozhu_all_weibo.pipelines.SinaWeiboArticlesItemPipeline': 1,
    # 'sina_weibo_bozhu_all_weibo.pipelines.SinaWeiboReviewsItemPipeline': 3,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

MONTH = 5       # 设置爬取到的截止月份, 比如截止到今年5月份的就为5

COOKIES = '_s_tentry=www.51testing.com; Apache=9731564567140.1509156407342; SINAGLOBAL=9731564567140.1509156407342; ULV=1509156407356:1:1:1:9731564567140.1509156407342:; UOR=www.51testing.com,widget.weibo.com,www.cnblogs.com; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; login_sid_t=2c4eac6521e48486369db54d22c4be28; YF-V5-G0=b4445e3d303e043620cf1d40fc14e97a; WBStorage=d0b15edc6ddab7a4|undefined; SSOLoginState=1509283006; wvr=6; YF-Page-G0=ed0857c4c190a2e149fc966e43aaf725; wb_cusLike_6164884717=N; cross_origin_proto=SSL; WBtopGlobal_register_version=b81eb8e02b10d728; SCF=AhlI1fIIew3qxgtQeK5WYz2CNbmDUnlK2Rxd-AtlWDk76_KPenY5pZ7aB5ZhbRRv_s-8DLqc_ymqpQK0_XVhH-g.; SUB=_2A2508aVQDeThGeBP7VYZ-CrLyjuIHXVXhpGYrDV8PUNbmtBeLXXckW9i4BblgkoRBc_Cu9U3XhpKFrHyKw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFnCUfIwQh3Usm8xNPAMySy5JpX5K2hUgL.FoqpSoBR1hBNeKM2dJLoIEQLxKML1K-L1h-LxK-LB.qLB-zLxKML1-zLB.eLxKqL1-eL1-ikSozReoqt; SUHB=0vJY-Gy-bOqDy2; ALF=1509887872; un=jc09893445wei@163.com'