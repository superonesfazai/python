# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_urldefrag.py
@Time    : 2017/8/17 10:08
@connect : superonesfazai@gmail.com
'''

"""
为了从url简单的除去frag(即fragment)
例如: 当从url查找一个基础页面时, 使用urldefrag()
"""

from urllib.parse import urldefrag

original = 'http://netloc/path;param?query=arg#frag'
print('original: ', original)

d = urldefrag(original)     # 返回一个DefragResult对象, 它包含:基础url, 和fragment
print('url     : ', d.url)
print('fragment: ', d.fragment)

'''
测试结果:
original:  http://netloc/path;param?query=arg#frag
url     :  http://netloc/path;param?query=arg
fragment:  frag
'''
