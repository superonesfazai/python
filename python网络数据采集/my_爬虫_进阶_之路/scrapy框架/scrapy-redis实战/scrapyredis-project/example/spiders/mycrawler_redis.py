from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider

"""
这个RedisCrawlSpider类爬虫继承了RedisCrawlSpider，能够支持分布式的抓取。
因为采用的是crawlSpider，所以需要遵守Rule规则，以及callback不能写parse()方法。

同样也不再有start_urls了，取而代之的是redis_key，
scrapy-redis将key从Redis里pop出来，成为请求的url地址
"""

class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'mycrawler_redis'
    redis_key = 'mycrawler:start_urls'

    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))

        # 修改这里的类名为当前域名
        super(MyCrawler, self).__init__(*args, **kwargs)

    def parse_page(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }

'''
注意:
    同样的，RedisCrawlSpider类不需要写allowd_domains和start_urls：

        1. scrapy-redis将从在构造方法__init__()里动态定义爬虫爬取域范围，也可以选择直接写allowd_domains。
        
        2. 必须指定redis_key，即启动爬虫的命令，参考格式：redis_key = 'myspider:start_urls'
        
        3. 根据指定的格式，start_urls将在 Master端的 redis-cli 里 lpush 到 Redis数据库里，RedisSpider 将在数据库里获取start_urls

执行方式：
    
    1. 通过runspider方法执行爬虫的py文件（也可以分次执行多条），爬虫（们）将处于等待准备状态：
    
        scrapy runspider mycrawler_redis.py
    
    2. 在Master端的redis-cli输入push指令，参考格式：
    
        $redis > lpush mycrawler:start_urls http://www.dmoz.org/
    
    3. 爬虫获取url，开始执行
'''