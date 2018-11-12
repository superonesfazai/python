# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Item, Field

class PostItem(Item):
    '''帖子基本信息'''
    title = Field()
    author = Field()
    comment_num = Field()  # 评论数
    post_url = Field()  # 帖子url