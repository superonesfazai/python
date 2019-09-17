# coding:utf-8

'''
@author = super_fazai
@File    : random_phone_num.py
@connect : superonesfazai@gmail.com
'''

"""
获取一个随机phone_num
"""

from random import randint
from pprint import pprint

phone_list = []
with open('../tools/phone.txt', 'r') as f:
    for line in f:
        try:
            phone_list.append(int(line.replace('\n', '')))
        except Exception:
            continue

# pprint(phone_list)
random_phone = phone_list[randint(0, len(phone_list) - 1)]
print('random_phone: {}'.format(random_phone))