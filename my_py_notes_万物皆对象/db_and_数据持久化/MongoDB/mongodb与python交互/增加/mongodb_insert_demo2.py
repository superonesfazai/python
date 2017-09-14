# coding = utf-8

'''
@author = super_fazai
@File    : mongodb_insert_demo2.py
@Time    : 2017/9/14 17:16
@connect : superonesfazai@gmail.com
'''

"""
增加多条文档对象
"""

from pymongo import *

try:
    # 构造json对象
    doc1={'name':'hr','home':'thd'}
    doc2={'name':'mnc','home':'njc'}
    doc=[doc1,doc2]

    #调用mongo对象，完成insert
    client=MongoClient('localhost',27017)
    db=client.py3
    db.stu.insert_many(doc)
    print('ok')
except Exception as e:
    print(e)