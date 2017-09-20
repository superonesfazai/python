# coding = utf-8

'''
@author = super_fazai
@File    : redis_pipeline.py
@Time    : 2017/9/12 20:28
@connect : superonesfazai@gmail.com
'''

"""
StrictPipeline调用
    * 所有的操作并不立即到服务器上执行，而是先将命令存在本地，
      调用execute()方法会将所有命令发给服务器，返回列表，元素是每个命令的返回值
"""

from redis import *

try:
    sr=StrictRedis()
    pl=sr.pipeline()

    pl.set('py1','gj')
    pl.get('py1')
    pl.keys()

    result=pl.execute()
    print(result)
except Exception as e:
    print(e)

'''
测试结果：
[True, b'gj', [b'py1']]
'''