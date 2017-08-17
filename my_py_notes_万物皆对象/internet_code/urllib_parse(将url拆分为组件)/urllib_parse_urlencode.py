# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_urlencode.py
@Time    : 2017/8/17 10:47
@connect : superonesfazai@gmail.com
'''

"""
在arguments被加入到url前, 它们需要先被encode
"""

from urllib.parse import urlencode

query_args = {
    'q': 'query string',
    'foo': 'bar',
}
encoded_args = urlencode(query_args)
print('Encoded:', encoded_args)

'''
测试结果:
Encoded: q=query+string&foo=bar
'''