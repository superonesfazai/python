# coding:utf-8

'''
@author = super_fazai
@File    : fz_driver.py
@connect : superonesfazai@gmail.com
'''

from .fz_phantomjs import (
    MyPhantomjs,
    CHROME,
    PHANTOMJS,
    FIREFOX,
    PC,
    PHONE,)

__all__ = [
    'BaseDriver',       # 驱动控制类
]

class BaseDriver(MyPhantomjs):
    pass
