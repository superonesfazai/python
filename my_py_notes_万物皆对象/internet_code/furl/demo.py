# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/7/28 11:46
@connect : superonesfazai@gmail.com
'''

"""
github: https://github.com/gruns/furl
"""

from furl import furl
from pprint import pprint

f = furl('http://www.google.com/?one=1&two=2')
f.args['three'] = 3
del f.args['one']
print(f.url)        # http://www.google.com/?two=2&three=3

print(furl('http://www.google.com/?one=1').add({'two':'2'}).url)            # http://www.google.com/?one=1&two=2
print(furl('http://www.google.com/?one=1&two=2').set({'three':'3'}).url)    # http://www.google.com/?three=3
print(furl('http://www.google.com/?one=1&two=2').remove(['one']).url)       # http://www.google.com/?two=2

f = furl('http://www.google.com/search?q=query#1')
pprint(f.copy().remove(path=True).set(host='taco.com').join('/pumps.html').add(fragment_path='party').asdict())
