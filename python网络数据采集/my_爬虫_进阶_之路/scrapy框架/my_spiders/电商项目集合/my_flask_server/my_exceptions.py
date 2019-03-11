# coding:utf-8

'''
@author = super_fazai
@File    : my_exceptions.py
@connect : superonesfazai@gmail.com
'''

class GoodsShelvesException(Exception):
    """商品下架异常"""
    pass

class MiaSkusIsNullListException(Exception):
    """蜜芽skus参数为空list"""
    pass

class SqlServerConnectionException(Exception):
    """sql server连接异常!"""
    pass