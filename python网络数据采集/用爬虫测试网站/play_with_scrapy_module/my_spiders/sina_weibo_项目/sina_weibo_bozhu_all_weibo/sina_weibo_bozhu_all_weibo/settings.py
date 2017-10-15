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

MONTH = 4       # 设置爬取到的截止月份, 比如截止到今年4月份的就为4

COOKIES = 'YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; login_sid_t=6afc0650d7568dc9e7396b28a7a63c29; YF-V5-G0=2a21d421b35f7075ad5265885eabb1e4; WBStorage=569d22359a08e178|undefined; _s_tentry=-; Apache=8637646027450.7295.1507553323976; SINAGLOBAL=8637646027450.7295.1507553323976; ULV=1507553323985:1:1:1:8637646027450.7295.1507553323976:; SSOLoginState=1507553452; SCF=Aqy9qBtl4GEVZo303b8vix6GL1NzFeoBU4sGMK5TilQdI54G16i2MlQ13RgzAjMa-1Lbzo32QmFr2l7MEK8N_X0.; SUB=_2A2503wCQDeThGeBP7VYZ9ijEzDqIHXVXrXVYrDV8PUNbmtBeLRKtkW89JM3Ka_i1KxgwYm07BhLXQzpHjQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Uz0_hIcQwJ5PszwoqpIGl5JpX5K2hUgL.FoqpSoBRSoqRS0q2dJLoIEQLxKqL1h-L1K-LxKqL1h2L12zLxKqL1h2L1K5LxKqL1heLBKUkSK5ESoMt; SUHB=03oVABe-CsGb-1; ALF=1539089471; un=rq93152975chuang@163.com; wvr=6; wb_cusLike_6164866876=N; YF-Page-G0=19f6802eb103b391998cb31325aed3bc'