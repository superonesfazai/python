# coding = utf-8

'''
@author = super_fazai
@File    : pprint_demo.py
@Time    : 2017/8/16 22:43
@connect : superonesfazai@gmail.com
'''

data = [
    (1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
    (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
         'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}),
    (3, ['m', 'n']),
    (4, ['o', 'p', 'q']),
    (5, ['r', 's', 't''u', 'v', 'x', 'y', 'z']),
]

from pprint import pprint

print('PRINT:')
print(data)
print()
print('PPRINT:')
pprint(data)