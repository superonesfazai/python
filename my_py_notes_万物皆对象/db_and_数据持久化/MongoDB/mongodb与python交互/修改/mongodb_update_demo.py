# coding = utf-8

'''
@author = super_fazai
@File    : mongodb_update_demo.py
@Time    : 2017/9/14 17:57
@connect : superonesfazai@gmail.com
'''

from pymongo import *

try:
    client=MongoClient('localhost', 27017)
    db=client.py3
    db.stu.update_one({'gender':False},{'$set':{'name':'hehe'}})
    # 更新多条
    # db.stu.update_many({'gender': True}, {'$set': {'name': 'haha'}})
    print('ok')
except Exception as e:
    print(e)