# coding = utf-8

'''
@author = super_fazai
@File    : redis_set1.py
@Time    : 2017/9/12 20:15
@connect : superonesfazai@gmail.com
'''

"""
写set
读get
改set
    上面set和get，如果返回值为True表示写成功，返回False表示写失败
删delete
    返回值为操作成功的条数，例如删除一个键成功则返回1
查看所有键keys
    返回值为列表，每个元素都是键的名称，如果没有键则返回空列表
"""

from redis import *

try:
    sr = StrictRedis()
    result = sr.set('py1', 'gj')    # 写set
    print(result)

    print(sr.get('py1'))            # 读get

    result = sr.set('py1', 'aa')    # 改set
    print(result)
    print(sr.get('py1'))

    result = sr.keys()              # 查看所有键keys
    print(result)

    result = sr.delete('py1')       # 删delete
    print(result)
except Exception as e:
    print(e)

'''
测试结果：
True
b'gj'
True
b'aa'
[b'py1']
1
'''