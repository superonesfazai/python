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

class VideoItem(Item):
    """
    video item
    """
    video_name = Field()                # 电影名
    static_img_url = Field()            # 电影某帧画面的img_url
    video_url = Field()                 # 播放地址
    like_num = Field()                  # 喜欢数
    dislike_num = Field()               # 不喜欢数
    collected_num = Field()             # 收藏数
