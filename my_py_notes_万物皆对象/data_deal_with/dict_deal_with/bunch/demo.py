# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import yaml
from bunch import Bunch
from json import dumps

b = Bunch()
b.hello = 'world'
print(b.hello)

b.hello += '!'
print(b.hello)

b.foo = Bunch(lol=True)
print(b.foo.lol)

# dict 与 Bunch转换
b = Bunch({'a': True})
print('--> dict 与 Bunch转换')
print('dict_2_Bunch: {}'.format(b))
print('Bunch_2_dict: {}'.format(dict(b)))
print('---')

# 序列化
b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
print(dumps(b))

print(yaml.dump(b))
print(yaml.safe_dump(b))