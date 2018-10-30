# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2018/7/3 18:26
@connect : superonesfazai@gmail.com
'''

"""
UUID 是通用唯一识别码（Universally Unique Identifier）的缩写
    uuid1()——基于时间戳
    uuid2()——基于分布式计算环境DCE（Python中没有这个函数）
    uuid3()——基于名字的MD5散列值
    uuid4()——基于随机数
    uuid5()——基于名字的SHA-1散列值
"""

import uuid

# make a random UUID
print(uuid.uuid1())
print(uuid.uuid4())
print()
# make a UUID using an MD5 hash of a namespace UUID and a name(这样生成的是唯一的识别码)
# url = 'python.org'
# url = 'https://www.kaola.com/activity/detail/8476.shtml?tag=cf5274c0ff456df92e385fabd1c58301&__da_Vu0MCs_OVtqR9&fc=u1.c6897.g6898.k1445920816175.pz'
url = r'黑色|32码| 3t/'
_uuid3 = uuid.uuid3(uuid.NAMESPACE_DNS, url)
print(_uuid3)     # '6fa459ea-ee8a-3ca4-894e-db77e160355e'

# make a UUID using a SHA-1 hash of a namespace UUID and a name(这样生成的是唯一的识别码)
print(uuid.uuid5(uuid.NAMESPACE_DNS, url))     # '886313e1-3b8a-5372-9b90-0c9aee199e5d'

# make a UUID from a string of hex digits (braces and hyphens ignored)(这样生成的是唯一的识别码)
x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
print(str(x))                                           # '00010203-0405-0607-0809-0a0b0c0d0e0f'

# get the raw 16 bytes of the UUID
print(x.bytes)
# make a UUID from a 16-byte string
print(uuid.UUID(bytes=x.bytes))