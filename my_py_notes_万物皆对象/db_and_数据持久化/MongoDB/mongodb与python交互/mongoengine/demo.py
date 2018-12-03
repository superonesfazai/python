# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from mongoengine import *

# 定义文档模式
class DouYinWeb(Document):
    cursor = StringField()
    content = ListField()

class BaseMongodbCli(object):
    def __init__(self):
        try:
            self.mongdb_cli = connect(db='fz_db', host='mongodb://127.0.0.1:27017/fz_db')
        except Exception as e:
            raise e

    def __del__(self):
        try:
            del self.mongdb_cli
        except:
            pass
        collect()