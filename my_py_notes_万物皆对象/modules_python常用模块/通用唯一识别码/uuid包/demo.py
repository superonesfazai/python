# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/7/3 18:26
@connect : superonesfazai@gmail.com
'''

"""
UUID 是通用唯一识别码（Universally Unique Identifier）的缩写
"""

import uuid

# make a random UUID
print(uuid.uuid1())
print(uuid.uuid4())
# make a UUID using an MD5 hash of a namespace UUID and a name(这样生成的是唯一的识别码)
print(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))     # '6fa459ea-ee8a-3ca4-894e-db77e160355e'

# make a UUID using a SHA-1 hash of a namespace UUID and a name(这样生成的是唯一的识别码)
print(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))     # '886313e1-3b8a-5372-9b90-0c9aee199e5d'

# make a UUID from a string of hex digits (braces and hyphens ignored)(这样生成的是唯一的识别码)
x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
print(str(x))                                           # '00010203-0405-0607-0809-0a0b0c0d0e0f'

# get the raw 16 bytes of the UUID
print(x.bytes)
# make a UUID from a 16-byte string
print(uuid.UUID(bytes=x.bytes))