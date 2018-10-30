# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2018/7/7 09:58
@connect : superonesfazai@gmail.com
'''

"""
base64的编码与解码
"""

from base64 import (
    b64encode,
    b64decode,
)

url = 'https://www.kaola.com/activity/detail/8476.shtml?tag=cf5274c0ff456df92e385fabd1c58301&__da_Vu0MCs_OVtqR9&fc=u1.c6897.g6898.k1445920816175.pz'
编码 = b64encode(s=url.encode('utf-8'))
解码 = b64decode(s=编码).decode('utf-8')

print(编码)
print(解码 + '\n')

print(url)


