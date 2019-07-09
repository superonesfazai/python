# coding = utf-8

'''
@author = super_fazai
@File    : urllib_request_urlopen_post.py
@Time    : 2017/8/17 12:00
@connect : superonesfazai@gmail.com
'''

from urllib import parse
from urllib import request

query_args = {'q': 'query string', 'foo': 'bar'}
encoded_args = parse.urlencode(query_args).encode('utf-8')
# print(encoded_args)
url = 'http://localhost:8080/'
print(request.urlopen(url, encoded_args).read().decode('utf-8'))