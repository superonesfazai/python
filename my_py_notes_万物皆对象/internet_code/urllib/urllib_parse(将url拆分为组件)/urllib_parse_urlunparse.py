# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_urlunparse.py
@Time    : 2017/8/17 10:23
@connect : superonesfazai@gmail.com
'''

"""
通过urlunparse()方法重新组合被urlparse()方法拆分的对象, 来得到原始url
因为urlparse()方法的操作结果是一个ParseResult对象, 
实际可以通过[:]将其转换为一个元组对象
urlunparse()方法则是通过这个元组重新组合成一个原始url
"""

from urllib.parse import urlparse, urlunparse

original = 'http://netloc/path;param?query=arg#frag'
print('ORIG  : ', original)
parsed = urlparse(original)
print('PARSED: ', type(parsed), parsed)
t = parsed[:]
print('TUPLE : ', type(t), t)
print('NEW   : ', urlunparse(t))

print('分割线'.center(40, '-'))

# 如果原始url包括多余的部分, 这些多余的部分可能在重建url的时候被抛弃
# 在这种情况下, parameters, query, and fragment都会消失的从原始的url
# 这个新的url看起来是跟原始url不像的, 但是它是等价于原始url的
from urllib.parse import urlparse, urlunparse

original = 'http://netloc/path;?#'
print('ORIG  :', original)
parsed = urlparse(original)
print('PARSED:', type(parsed), parsed)
t = parsed[:]
print('TUPLE :', type(t), t)
print('NEW   :', urlunparse(t))


'''
测试结果:
ORIG  :  http://netloc/path;param?query=arg#frag
PARSED:  <class 'urllib.parse.ParseResult'> ParseResult(scheme='http', netloc='netloc', path='/path', params='param', query='query=arg', fragment='frag')
TUPLE :  <class 'tuple'> ('http', 'netloc', '/path', 'param', 'query=arg', 'frag')
NEW   :  http://netloc/path;param?query=arg#frag
------------------分割线-------------------
ORIG  : http://netloc/path;?#
PARSED: <class 'urllib.parse.ParseResult'> ParseResult(scheme='http', netloc='netloc', path='/path', params='', query='', fragment='')
TUPLE : <class 'tuple'> ('http', 'netloc', '/path', '', '', '')
NEW   : http://netloc/path
'''