# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

# from pymssql import *
from _mssql import *

try:
    raise MSSQLDatabaseException
except Exception as e:
    print(type(e.number))