# -*- coding: utf-8 -*-

# Scrapy settings for sina_weibo_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sina_weibo_project'

SPIDER_MODULES = ['sina_weibo_project.spiders']
NEWSPIDER_MODULE = 'sina_weibo_project.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'sina_weibo_project (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'sina_weibo_project.middlewares.SinaWeiboProjectSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sina_weibo_project.middlewares.MyCustomDownloaderMiddleware': None,
    # 'sina_weibo_project.middlewares.CustomMiddlewares': 100,
    'sina_weibo_project.middlewares.SinaUserAgentMiddleware': 80,
    # 'sina_weibo_project.middlewares.SinaProxyMiddleware': 60,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sina_weibo_project.pipelines.SinaWeiboProjectPipeline': None,
    'sina_weibo_project.pipelines.BoZhuUserPipeline': 1,
    # 'sina_weibo_project.pipelines.HomeInfoPipeline': 5,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 在此处替换你自己登陆浏览器后获取到的cookie值
COOKIES = 'SINAGLOBAL=8637646027450.7295.1507553323976; un=rq93152975chuang@163.com; wvr=6; SSOLoginState=1507774729; _s_tentry=-; UOR=,,cuiqingcai.com; Apache=5334132326721.058.1507798089392; ULV=1507798089561:2:2:2:5334132326721.058.1507798089392:1507553323985; SCF=Aqy9qBtl4GEVZo303b8vix6GL1NzFeoBU4sGMK5TilQdSnkftExSaSjcYpu_qHvCV5Wn-WM9gFXKzO0lFg2dX4I.; SUB=_2A2505FphDeThGeBP7VYZ9ijEzDqIHXVXkMyprDV8PUNbmtBeLVPykW8j_h5vdf_UfrxfqZeX1SY0kRvMLw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Uz0_hIcQwJ5PszwoqpIGl5JpX5KMhUgL.FoqpSoBRSoqRS0q2dJLoIEQLxKqL1h-L1K-LxKqL1h2L12zLxKqL1h2L1K5LxKqL1heLBKUkSK5ESoMt; SUHB=0KAhjL1zZTmUFi; ALF=1539399089; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; TC-V5-G0=05e7a45f4d2b9f5b065c2bea790496e2; wb_cusLike_6164866876=N; TC-Page-G0=1bbd8b9d418fd852a6ba73de929b3d0c'