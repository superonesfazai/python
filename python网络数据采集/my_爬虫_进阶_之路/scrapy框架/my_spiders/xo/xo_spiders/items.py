# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Item
from scrapy import Field

class VideoListItem(Item):
    """
    电影列表item
    """
    video_name = Field()            # 电影名
    video_region = Field()          # 影片地区
    video_type = Field()            # 影片类别
    url = Field()                   # 电影介绍页url
    create_time = Field()           # 创建时间