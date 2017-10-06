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

COOKIES = 'SINAGLOBAL=1920862274319.4636.1502628639473; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; YF-Ugrow-G0=ea90f703b7694b74b62d38420b5273df; YF-V5-G0=3d0866500b190395de868745b0875841; _s_tentry=login.sina.com.cn; Apache=5535716871036.658.1506825662817; ULV=1506825662957:9:1:1:5535716871036.658.1506825662817:1506609903208; YF-Page-G0=b35da6f93109faa87e8c89e98abf1260; TC-V5-G0=ac3bb62966dad84dafa780689a4f7fc3; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; login_sid_t=7512e659ecf2f4cf12080ce37d716b1d; WBtopGlobal_register_version=1844f177002b1566; cross_origin_proto=SSL; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506955740; un=rlzeam07@163.com; wvr=6; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcH6ekYMJ_9vkzZLyueJJVbFUqFhKX4gpugo1IA7lkBlYI.; SUB=_2A25019iaDeThGeBP7VYY8SzNwzmIHXVXpU1SrDV8PUJbmtAKLXngkW-eciawg0sKAweobhKHAe08nyUGiw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFqTWuN4lGrED1Loh_Jr2Gs5JpX5K-hUgL.FoqpSoB4eKzp1h-2dJLoIEQLxKqL1h5L1-BLxK.L1h5LBonLxKqL1h5L1-BLxKnLB.qL1-Sk1hMceKet; SUHB=0eb98WoRtKCUkR; ALF=1538579524'
