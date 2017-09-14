# coding = utf-8

'''
@author = super_fazai
@File    : mongodb_insert_demo1.py
@Time    : 2017/9/14 17:10
@connect : superonesfazai@gmail.com
'''

"""
增加一条文档对象
"""

from pymongo import *

try:
    name = input('请输入姓名：')
    home = input('请输入家乡：')

    # 构造json对象
    doc = {
        'name': name,
        'home': home,
    }

    # 调用mongodb对象 完成insert
    client = MongoClient('localhost', 27017)
    db = client.py3
    db.stu.insert_one(doc)
    print('ok')
except Exception as e:
    print(e)