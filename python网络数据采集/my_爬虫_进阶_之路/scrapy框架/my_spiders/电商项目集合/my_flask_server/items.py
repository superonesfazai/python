# coding:utf-8

'''
@author = super_fazai
@File    : items.py
@connect : superonesfazai@gmail.com
'''

from scrapy import Item, Field

class ArticleItem(Item):
    title = Field()
    create_time = Field()
    article_url = Field()
    author = Field()
    article_md5_id = Field()    # 可以对url做一个md5,让它的长度变成固定的长度
    comment_num = Field()       # 评论数
    fav_num = Field()           # 收藏数
    praise_num = Field()        # 点赞数
    tags_list = Field()         # 标签
    content = Field()           # 内容