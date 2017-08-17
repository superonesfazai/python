# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_parse_qs.py
@Time    : 2017/8/17 10:56
@connect : superonesfazai@gmail.com
'''

"""
为了去解码查询指令的string, 使用parse_qs()或者parse_qsl()
"""

from urllib.parse import parse_qs, parse_qsl

encoded = 'foo=foo1&foo=foo2'

print('parse_qs :', parse_qs(encoded))      # parse_qs()返回的是一个字典
print('parse_qsl:', parse_qsl(encoded))     # parse_qsl()返回的是一个list, 里面有元组组成, 包含一个name和一个value

'''
测试结果:
parse_qs : {'foo': ['foo1', 'foo2']}
parse_qsl: [('foo', 'foo1'), ('foo', 'foo2')]
'''

