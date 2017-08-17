# coding = utf-8

'''
@author = super_fazai
@File    : urllib_request_request_header.py
@Time    : 2017/8/17 12:01
@connect : superonesfazai@gmail.com
'''

from urllib import request

r = request.Request('http://localhost:8080/')
r.add_header(
    'User-agent',
    'PyMOTW (https://pymotw.com/)',
)

response = request.urlopen(r)
data = response.read().decode('utf-8')
print(data)