# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SinaWeiboBozhuAllWeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SinaWeiboArticlesItem(scrapy.Item):
    id = Field()                        # 该微博文章的id
    nick_name = Field()                 # 博主微博名
    created_at = Field()                # 该微博文章创建时间
    text = Field()                      # 该微博的内容
    image_url_list = Field()            # 原创微博的图片链接地址
    m_media_url = Field()               # 原创微博的视频url
    retweeted_text = Field()            # 该微博转发的内容
    retweeted_image_url_list = Field()  # 转发内容的图片链接
    media_url = Field()                 # 转发内容的视频链接地址
    reposts_count = Field()             # 转载数
    comments_count = Field()            # 评论数
    attitudes_count = Field()           # 赞数

class SinaWeiboReviewsItem(scrapy.Item):
    review_id = Field()                 # 评论内容的id
    wb_id = Field()                     # 对应微博文章的id
    username = Field()                  # 评论者微博号名
    comment = Field()                   # 评论的文字内容
    review_created_at = Field()         # 评论内容的创建时间
    is_reply_comment = Field()          # 判断是否为博主回复内容, 如果是值为True
    like_counts = Field()               # 评论内容点赞数
    review_pics = Field()               # 评论的图片内容