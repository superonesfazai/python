# -*- coding: utf-8 -*-
# from MySQLdb import *
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
# SPIDER_MIDDLEWARES = {
#    'sina_weibo_personal_info_spider.middlewares.SinaWeiboPersonalInfoSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sina_weibo_personal_info_spider.middlewares.MyCustomDownloaderMiddleware': None,
    'sina_weibo_personal_info_spider.middlewares.SinaUserAgentMiddleware': 20,
    'sina_weibo_personal_info_spider.middlewares.SinaProxyMiddleware': 25,
    'sina_weibo_personal_info_spider.middlewares.CustomMiddlewares': 30,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

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
    'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'd.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

"""
* 注意：(一次只能开一个对应的管道, 否则无法存储数据)
    - 运行personal_info_spider时, 先把下面第二个注释掉, 不注释第一个
    - 运行company_info_spider时, 先把下面的第一个注释掉, 不注释第二个
"""
ITEM_PIPELINES = {
    # 爬取个人微博信息时，打开，关闭企业管道
    'sina_weibo_personal_info_spider.pipelines.SinaWeiboPersonalInfoSpiderPipeline': 1,
    # 爬取企业微博信息时，打开，关闭个人管道
    # 'sina_weibo_personal_info_spider.pipelines.SinaWeiboCompanyDealInfoSpiderPipeline': 3,
}

# 先自己登陆到新浪微博, 然后把cookie值直接拷到下面替换即可(注意把内容用单引号括起来)
COOKIES = '_s_tentry=blog.csdn.net; UOR=blog.csdn.net,widget.weibo.com,blog.csdn.net; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=3b9f325cbcf992283b90354cffbe46c1; TC-V5-G0=40eeee30be4a1418bde327baf365fcc0; WBStorage=d0b15edc6ddab7a4|undefined; Apache=1283790175605.939.1508919226577; SINAGLOBAL=1283790175605.939.1508919226577; ULV=1508919226585:1:1:1:1283790175605.939.1508919226577:; SSOLoginState=1508919300; wvr=6; wb_cusLike_6164884717=N; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; cross_origin_proto=SSL; WBtopGlobal_register_version=b81eb8e02b10d728; SCF=Aja3CIFGwvx1LASQb6DlJEASKftWgIjXOdptQgofbuxPdEkhIMw2YF44Hf_2KEA83p8GpQxIp4bGaM_8A5a-0xc.; SUB=_2A2509DhoDeThGeBP7VYZ-CrLyjuIHXVXgC6grDV8PUNbmtBeLXT4kW-bcVbg8NW7s9EHDF0hNP9OqYoF7w..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFnCUfIwQh3Usm8xNPAMySy5JpX5K2hUgL.FoqpSoBR1hBNeKM2dJLoIEQLxKML1K-L1h-LxK-LB.qLB-zLxKML1-zLB.eLxKqL1-eL1-ikSozReoqt; SUHB=08Jr6QQxExM0TU; ALF=1509524151; un=jc09893445wei@163.com'

# 下面这个是phantomjs的绝对路径(在自己电脑上下载这个phantomjs)，配置成自己的
EXECUTABLE_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'