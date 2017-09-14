# coding = utf-8

'''
@author = super_fazai
@File    : mongodb_delete_demo.py
@Time    : 2017/9/14 18:03
@connect : superonesfazai@gmail.com
'''

from pymongo import *

try:
    client=MongoClient('localhost',27017)
    db=client.py3
    db.stu.delete_one({'gender':True})      # 删除一条文档信息
    # 删除多条文档信息
    # db.stu.delete_many({'gender': False})
    print('ok')
except Exception as e:
    print(e)