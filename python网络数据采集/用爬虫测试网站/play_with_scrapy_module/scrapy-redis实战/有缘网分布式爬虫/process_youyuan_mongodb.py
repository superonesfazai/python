# coding = utf-8

'''
@author = super_fazai
@File    : process_youyuan_mongodb.py
@Time    : 2017/9/7 17:22
@connect : superonesfazai@gmail.com
'''

"""
处理redis里的数据库

存入mongodb
    1. 启动mongodb数据库 sudo mongod
    2. 执行下面这个程序
"""

import json
import redis
import pymongo

def main():

    # 指定Redis数据库信息
    rediscli = redis.StrictRedis(
        host='192.168.199.108',
        port=6379,
        db=0
    )
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='localhost', port=27017)

    # 创建数据库名
    db = mongocli['youyuan']
    # 创建表名
    sheet = db['beijing_18_25']

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["youyuan:items"])

        item = json.loads(data)
        sheet.insert(item)

        try:
            print("Processing: %(name)s <%(link)s>" % item)
        except KeyError:
            print("Error procesing: %r" % item)

if __name__ == '__main__':
    main()