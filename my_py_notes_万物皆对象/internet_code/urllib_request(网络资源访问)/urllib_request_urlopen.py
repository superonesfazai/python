# coding = utf-8

'''
@author = super_fazai
@File    : urllib_request_urlopen.py
@Time    : 2017/8/17 11:17
@connect : superonesfazai@gmail.com
'''

from urllib import request

response = request.urlopen('http://localhost:8080/')
print('RESPONSE:', response)
print('URL     :', response.geturl())

headers = response.info()
print('DATE    :', headers['date'])
print('HEADERS :')
print('---------')
print(headers)

data = response.read().decode('utf-8')
print('LENGTH  :', len(data))
print('DATA    :')
print('---------')
print(data)