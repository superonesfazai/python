# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@connect : superonesfazai@gmail.com
'''

# 文章可扩展抽取
ARTICLE_ITEM_LIST = [
    {
        'obj_origin': 'mp.weixin.qq.com',
        'title': {
            'method': 'css',
            'selector': 'div#img-content h2 ::text',
        },
        'author': {
            'method': 'css',
            'selector': 'div#meta_content span a ::text',
        },
        'create_time': {
            'method': 're',
            'selector': 'var publish_time = \"(.*?)\" ',
        },
        'content': {
            'method': 'css',
            'selector': 'div.rich_media_content',
        },
        'comment_num': None,
        'fav_num': None,
        'praise_num': None,
        'tags_list': None,
    }
]