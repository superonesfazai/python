# coding = utf-8

'''
@author = super_fazai
@File    : mongodb_find_demo.py
@Time    : 2017/9/14 17:19
@connect : superonesfazai@gmail.com
'''

from pymongo import *

try:
    client=MongoClient('localhost', 27017)
    db=client.py3
    # doc=db.stu.find_one()     # 查询一条数据
    # print('%s--%s' % (doc['name'], doc['hometown']))
    cursor = db.stu.find()      # 查询多条数据, 然后通过for 来循环读取
    for doc in cursor:
        print('%s--%s' % (doc['name'], doc['home']))

except Exception as e:
    print(e)
