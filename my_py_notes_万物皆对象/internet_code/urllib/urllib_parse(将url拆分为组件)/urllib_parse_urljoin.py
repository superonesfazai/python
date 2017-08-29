# coding = utf-8

'''
@author = super_fazai
@File    : urllib_parse_urljoin.py
@Time    : 2017/8/17 10:38
@connect : superonesfazai@gmail.com
'''

"""
urljoin()可以从相对的fragments构造一个绝对而言的url
如果第二个参数的path以'/'开始, 它将在顶级重建这个url
如果path不是以'/'开始的, 它将被作为到这个url的path的子路径
"""

from urllib.parse import urljoin

print(urljoin('http://www.example.com/path/file.html',
              'anotherfile.html'))
print(urljoin('http://www.example.com/path/file.html',
              '../anotherfile.html'))
print(urljoin('http://www.example.com/path/',
              '/subpath/file.html'))
print(urljoin('http://www.example.com/path/',
              'subpath/file.html'))

'''
测试结果:
http://www.example.com/path/anotherfile.html
http://www.example.com/anotherfile.html
http://www.example.com/subpath/file.html
http://www.example.com/path/subpath/file.html
'''