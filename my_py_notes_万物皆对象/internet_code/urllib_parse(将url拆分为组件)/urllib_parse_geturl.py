# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_geturl.py
@Time    : 2017/8/17 10:16
@connect : superonesfazai@gmail.com
'''

"""
通过geturl()来返回urlparse()或urlsplit()方法操作前的原始url
"""

from urllib.parse import urlparse

original = 'http://netloc/path;param?query=arg#frag'
print('ORIG  :', original)
parsed = urlparse(original)
print('PARSED:', parsed.geturl())   # geturl() 返回一个urlparse()或者urlsplit()
                                    # 即返回的是拆分前的原始url

'''
测试结果:
ORIG  : http://netloc/path;param?query=arg#frag
PARSED: http://netloc/path;param?query=arg#frag
'''
