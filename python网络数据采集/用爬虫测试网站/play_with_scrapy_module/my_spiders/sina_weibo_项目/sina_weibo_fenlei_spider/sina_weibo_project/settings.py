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
#USER_AGENT = 'sina_weibo_project (+http://www.yourdomain.com)'

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
#    'sina_weibo_project.middlewares.SinaWeiboProjectSpiderMiddleware': 543,
#}

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
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sina_weibo_project.pipelines.SinaWeiboProjectPipeline': None,
    'sina_weibo_project.pipelines.BoZhuUserPipeline': 1,
    # 'sina_weibo_project.pipelines.HomeInfoPipeline': 5,
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

# 在此处替换你自己登陆浏览器后获取到的cookie值
COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; un=rlzeam07@163.com; wvr=6; SSOLoginState=1507187445; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=020421dd535a1c903e89d913fb8a2988; YF-Page-G0=35f114bf8cf2597e9ccbae650418772f; _s_tentry=-; Apache=2476847061324.536.1507209430567; ULV=1507209430679:10:2:2:2476847061324.536.1507209430567:1506825662957; TC-V5-G0=26e4f9c4bdd0eb9b061c93cca7474bf2; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7; UOR=developer.51cto.com,widget.weibo.com,blog.csdn.net; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHqHvgSurJe1jVSuk0x6XuuAiektTfiAB3Yfp9QfZtpvU.; SUB=_2A25000AbDeThGeBP7VYY8SzNwzmIHXVXqTbTrDV8PUNbmtBeLRCjkW9M3GoTIheGqqrhCK2CtWpgOGU8ew..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFqTWuN4lGrED1Loh_Jr2Gs5JpX5KMhUgL.FoqpSoB4eKzp1h-2dJLoIEQLxKqL1h5L1-BLxK.L1h5LBonLxKqL1h5L1-BLxKnLB.qL1-Sk1hMceKet; SUHB=0OM0vtaO-A252T; ALF=1538810825; wb_cusLike_6164912185=N'