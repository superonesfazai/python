# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


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

# 要求采集页面下所有创业公司的信息, 包括以下但不限于:

import scrapy

class CompanyItem(scrapy.Item):

    # 公司id (url数字部分)
    info_id = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司口号
    slogan = scrapy.Field()
    # 分类
    scope = scrapy.Field()
    # 子分类
    sub_scope = scrapy.Field()

    # 所在城市
    city = scrapy.Field()
    # 所在区域
    area = scrapy.Field()
    # 公司主页
    home_page = scrapy.Field()
    # 公司标签
    tags = scrapy.Field()

    # 公司简介
    company_intro = scrapy.Field()
    # 公司全称：
    company_full_name = scrapy.Field()
    # 成立时间：
    found_time = scrapy.Field()
    # 公司规模：
    company_size = scrapy.Field()
    # 运营状态
    company_status = scrapy.Field()

    # 投资情况列表：包含获投时间、融资阶段、融资金额、投资公司
    tz_info = scrapy.Field()
    # 团队信息列表：包含成员姓名、成员职称、成员介绍
    tm_info = scrapy.Field()
    # 产品信息列表：包含产品名称、产品类型、产品介绍
    pdt_info = scrapy.Field()