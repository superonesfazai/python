from scrapy_redis.spiders import RedisSpider


"""
这个爬虫继承了RedisSpider， 它能够支持分布式的抓取，
采用的是basic spider，需要写parse函数。

其次就是不再有start_urls了，取而代之的是redis_key，
scrapy-redis将key从Redis里pop出来，成为请求的url地址
"""

class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'

    # 注意redis-key的格式
    redis_key = 'myspider:start_urls'

    # 可选：等效于allowd_domains(), __init__方法按规定格式写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))

        # 修改这里的类名为当前类名
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }

'''
注意：
    RedisSpider类 不需要写allowd_domains和start_urls：
        1. scrapy-redis将从在构造方法__init__()里动态定义爬虫爬取域范围，也可以选择直接写allowd_domains。

        2. 必须指定redis_key，即启动爬虫的命令，参考格式：redis_key = 'myspider:start_urls'
        
        3. 根据指定的格式，start_urls将在 Master端的 redis-cli 里 lpush 到 Redis数据库里，RedisSpider 将在数据库里获取start_urls。  
        
执行方式：
    1. 通过runspider方法执行爬虫的py文件（也可以分次执行多条），爬虫（们）将处于等待准备状态：
    
        scrapy runspider myspider_redis.py
    
    2. 在Master端的redis-cli输入push指令，参考格式：
    
        $redis > lpush myspider:start_urls http://www.dmoz.org/
    
    3. Slaver端爬虫获取到请求，开始爬取。
'''