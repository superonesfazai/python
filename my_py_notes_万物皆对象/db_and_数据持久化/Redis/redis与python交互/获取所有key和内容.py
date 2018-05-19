# coding:utf-8

'''
@author = super_fazai
@File    : 获取所有key和内容.py
@Time    : 2018/5/20 00:01
@connect : superonesfazai@gmail.com
'''

import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

keys = r.keys()
print(type(keys))
print(keys)

'''获取所有内容'''
pipe = r.pipeline()
pipe_size = 100000

len = 0
key_list = []
print(r.pipeline())
keys = r.keys()
for key in keys:
    key_list.append(key)
    pipe.get(key)
    print()
    print(r.get(key).decode())

    if len < pipe_size:
        len += 1
    else:
        for (k, v) in zip(key_list, pipe.execute()):
            print(k, v)
        len = 0
        key_list = []

for (k, v) in zip(key_list, pipe.execute()):
    print(k, v)