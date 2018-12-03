# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Field, Item
from mongoengine import (
    Document,
    StringField,
    ListField,
    DateTimeField,
)

class VideoItem(Item):
    title = Field()
    author_name = Field()       # 作者名字
    author_id = Field()         # 作者id
    head_url = Field()          # 作者头像
    video_id = Field()          # 视频id
    fan_num = Field()           # 粉丝数
    download_url = Field()      # 视频下载地址
    share_url = Field()         # 分享的地址 or 原始网页地址
    praise_num = Field()        # 点赞数
    comment_num = Field()       # 评论数
    share_num = Field()         # 分享数

'''
# 查看集合唯一索引
> db.dou_yin_web.getIndexes()
# 创建唯一索引
> db.dou_yin_web.createIndex({cursor:1}, {unique: true})
'''

# 定义文档模式
class DouYinWeb(Document):
    cursor = StringField()
    content = ListField()
    create_time = DateTimeField()