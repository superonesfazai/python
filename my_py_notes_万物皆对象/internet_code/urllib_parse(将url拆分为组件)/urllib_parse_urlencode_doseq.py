# coding = utf-8

'''
@author = super_fazai
@File    : urlib_parse_urlencode_doseq.py
@Time    : 2017/8/17 10:52
@connect : superonesfazai@gmail.com
'''

"""
当调用urlencode()时:
通过一系列的查询字符串中
使用的变量的值设置doseq单独出现
"""

from urllib.parse import urlencode

query_args = {
    'foo': ['foo1', 'foo2'],
}
print('Single  :', urlencode(query_args))
print('Sequence:', urlencode(query_args, doseq=True))

'''
测试结果:
Single  : foo=%5B%27foo1%27%2C+%27foo2%27%5D
Sequence: foo=foo1&foo=foo2
'''