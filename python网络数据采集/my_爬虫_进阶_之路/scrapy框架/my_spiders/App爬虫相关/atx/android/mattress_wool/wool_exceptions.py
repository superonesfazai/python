# coding:utf-8

'''
@author = super_fazai
@File    : wool_exceptions.py
@connect : superonesfazai@gmail.com
'''

class ReadTimeOutException(Exception):
    """
    阅读超时异常
    """
    pass

class AppInstalledBeforeException(Exception):
    """
    app曾被注入过
    """
    pass

class NoMoreArticlesException(Exception):
    """
    没有更多文章异常
    """
    pass