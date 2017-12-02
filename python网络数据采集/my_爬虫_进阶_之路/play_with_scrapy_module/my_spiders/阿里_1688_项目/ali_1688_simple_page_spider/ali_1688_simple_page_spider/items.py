# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class Ali1688SimplePageSpiderItem(Item):
    # 商品标题
    title = Field()
    # 商品价格
    price = Field()
    # 商品起批量
    trade_number = Field()

    # 颜色
    color = Field()
    # 颜色的图片url(需要一一对应)
    color_img_url = Field()

    # 适合尺寸
    size_info = Field()

    # 对应颜色或者尺寸的价格(需要一一对应)
    detail_price = Field()

    # 对应颜色或者尺寸的库存量(需要一一对应)
    rest_number = Field()

    # 主显示的图片url
    center_img_url = Field()

    # 所有图片url
    all_img_url = Field()



