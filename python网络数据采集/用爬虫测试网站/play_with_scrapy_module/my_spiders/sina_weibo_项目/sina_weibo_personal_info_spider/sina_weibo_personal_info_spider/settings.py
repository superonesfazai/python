# -*- coding: utf-8 -*-

# Scrapy settings for sina_weibo_personal_info_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sina_weibo_personal_info_spider'

SPIDER_MODULES = ['sina_weibo_personal_info_spider.spiders']
NEWSPIDER_MODULE = 'sina_weibo_personal_info_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina_weibo_personal_info_spider (+http://www.yourdomain.com)'

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
#    'sina_weibo_personal_info_spider.middlewares.SinaWeiboPersonalInfoSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sina_weibo_personal_info_spider.middlewares.MyCustomDownloaderMiddleware': None,
    'sina_weibo_personal_info_spider.middlewares.SinaUserAgentMiddleware': 60,
    'sina_weibo_personal_info_spider.middlewares.SinaProxyMiddleware': 80,
    'sina_weibo_personal_info_spider.middlewares.CustomMiddlewares': 90,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sina_weibo_personal_info_spider.pipelines.SinaWeiboPersonalInfoSpiderPipeline': 1,
    'sina_weibo_personal_info_spider.pipelines.SinaWeiboCompanyDealInfoSpiderPipeline': 3,
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

COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-V5-G0=52dad2141fc02c292fc30606953e43ef; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; _s_tentry=login.sina.com.cn; Apache=9131340312967.717.1506609903037; ULV=1506609903208:8:5:2:9131340312967.717.1506609903037:1506498709703; YF-Page-G0=ab26db581320127b3a3450a0429cde69; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; login_sid_t=9b45845aa1847e9045ed0dab201cdca2; cross_origin_proto=SSL; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506674650; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHEOOhEj6-APWydXz03IBKyK-HBIiQ4RwY7O4Udv_ZZSo.; SUB=_2A250yneKDeRhGeNM41sX8ybLzjmIHXVXvu5CrDV8PUNbmtAKLVfWkW8tBcGBwIOOdOrHd25ayHS5IiZK1g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=03oFyrPxCsfWs7; ALF=1538210649; un=15661611306; wvr=6; wb_cusLike_5289638755=N'
