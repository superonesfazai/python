# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2018/7/3 18:14
@connect : superonesfazai@gmail.com
'''

"""
实用: 给打印的文本添加颜色
"""

from colorama import init, Fore, Back, Style

init()

print(Fore.GREEN + 'green, '
    + Fore.RED + 'red, '
    + Fore.RESET + 'normal, '
    , end='')
print(Back.GREEN + 'green, '
    + Back.RED + 'red, '
    + Back.RESET + 'normal, '
    , end='')
print(Style.DIM + 'dim, '
    + Style.BRIGHT + 'bright, '
    + Style.NORMAL + 'normal'
    , end=' ')
print()

