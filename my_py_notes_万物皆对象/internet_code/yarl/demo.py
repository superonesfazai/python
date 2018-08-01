# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/7/28 11:38
@connect : superonesfazai@gmail.com
'''

"""
github: https://github.com/gruns/furl
"""

from yarl import URL

url = URL('https://www.python.org/~guido?arg=1#frag')
print(url)                  # URL('https://www.python.org/~guido?arg=1#frag')
print(url.scheme)           # https
print(url.host)             # www.python.org
print(url.fragment)         # frag
print(url.path)             # /~guido
print(url.query_string)     # arg=1
print(url.parent)           # https://www.python.org