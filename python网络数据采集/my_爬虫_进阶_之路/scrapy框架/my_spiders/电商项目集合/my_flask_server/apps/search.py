# coding:utf-8

'''
@author = super_fazai
@File    : search.py
@Time    : 2017/8/11 10:41
@connect : superonesfazai@gmail.com
'''

from elasticsearch_dsl import (
    DocType,
    Index,)
from scrapy import Field

class Post():
    id = Field()

posts = Index('posts')

@posts.doc_type
class PostDocument(DocType):
    class Meta:
        model = Post

        fields = [
            'id',
        ]
