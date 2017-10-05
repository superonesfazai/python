# -*- coding: utf-8 -*-

# Scrapy settings for sina_weibo_home_info_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sina_weibo_home_info_spider'

SPIDER_MODULES = ['sina_weibo_home_info_spider.spiders']
NEWSPIDER_MODULE = 'sina_weibo_home_info_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sina_weibo_home_info_spider (+http://www.yourdomain.com)'

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
#    'sina_weibo_home_info_spider.middlewares.SinaWeiboHomeInfoSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sina_weibo_home_info_spider.middlewares.MyCustomDownloaderMiddleware': None,
    'sina_weibo_home_info_spider.middlewares.CustomMiddlewares': 100,
    'sina_weibo_home_info_spider.middlewares.SinaUserAgentMiddleware': 80,
    'sina_weibo_home_info_spider.middlewares.SinaProxyMiddleware': 60,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sina_weibo_home_info_spider.pipelines.SinaWeiboHomeInfoSpiderPipeline': None,
    'sina_weibo_home_info_spider.pipelines.HomeInfoPipeline': 1,
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

COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; YF-Ugrow-G0=ea90f703b7694b74b62d38420b5273df; YF-V5-G0=3d0866500b190395de868745b0875841; _s_tentry=login.sina.com.cn; Apache=5535716871036.658.1506825662817; ULV=1506825662957:9:1:1:5535716871036.658.1506825662817:1506609903208; YF-Page-G0=b35da6f93109faa87e8c89e98abf1260; TC-V5-G0=ac3bb62966dad84dafa780689a4f7fc3; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; login_sid_t=7512e659ecf2f4cf12080ce37d716b1d; WBtopGlobal_register_version=1844f177002b1566; wb_cusLike_6164884717=N; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; cross_origin_proto=SSL; SSOLoginState=1506927626; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHVNDXUCWSXb7k4dX9w_aTiXMYBXSFauMzPysMtlwBk4E.; SUB=_2A2501ZRaDeThGeBP7lsV-SrNyjqIHXVXooKSrDV8PUNbmtAKLUvskW82s2VbEHfX7yToHv0npXd1vkW8mw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFUyRNpvowEcWG5r5qzeMoo5JpX5K2hUgL.FoqpSK.X1KBpeKq2dJLoIEXLxKqLBoqLBKBLxKnL12BLBK2LxK-LB.eL1h5LxK-L1h-LBoeLxKMLBK-L1-Bt; SUHB=0jBYVAurGFt8GI; ALF=1538463626; un=jf89170747shu@163.com; wvr=6; wb_cusLike_6159494116=N'