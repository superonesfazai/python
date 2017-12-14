# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

"""
注意： 
    items数据直接存储在Redis数据库中，
    这个功能已经由scrapy-redis自行实现。
    除非单独做额外处理(比如直接存入本地数据库等)，
    否则不用编写pipelines.py代码
"""

class SinaItem(scrapy.Item):
    # 大类的标题 和 url
    parent_title = scrapy.Field()
    parent_urls = scrapy.Field()

    # 小类的标题 和 子url
    sub_title = scrapy.Field()
    sub_urls = scrapy.Field()

    # 小类目录存储路径
    # sub_file_name = scrapy.Field()

    # 小类下的子链接
    son_urls = scrapy.Field()

    # 文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()
