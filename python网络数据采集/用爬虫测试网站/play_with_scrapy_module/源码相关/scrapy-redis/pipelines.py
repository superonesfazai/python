# coding = utf-8

'''
@author = super_fazai
@File    : pipelines.py
@Time    : 2017/9/6 12:26
@connect : superonesfazai@gmail.com
'''

"""
这是用来实现分布式处理的作用,它将Item存储在redis中以实现分布式处理
由于在这里需要读取配置, 所以就用到了from_crawler()函数
"""

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

from . import connection


default_serialize = ScrapyJSONEncoder().encode


class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue"""

    def __init__(self, server,
                 key='%(spider)s:items',
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.
        Override this function to use a different key depending on the item
        and/or spider.
        """
        return self.key % {'spider': spider.name}

'''
pipelines文件实现了一个item pipieline类，和scrapy的item pipeline是同一个对象，
通过从settings中拿到我们配置的REDIS_ITEMS_KEY作为key，
把item串行化之后存入redis数据库对应的value中（这个value可以看出是个list，
我们的每个item是这个list中的一个结点），这个pipeline把提取出的item存起来，
主要是为了方便我们延后处理数据
'''