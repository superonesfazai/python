# coding:utf-8

'''
@author = super_fazai
@File    : async_always.py
@connect : superonesfazai@gmail.com
'''

"""
预导入异步高并发爬虫常用的包

使用只需: from fzutils.spider.async_always import *
"""

import re
from asyncio import get_event_loop
from time import sleep
from pprint import pprint
from scrapy.selector import Selector

from ..internet_utils import *
from .fz_requests import Requests
from ..common_utils import *
from ..aio_utils import (
    async_wait_tasks_finished,)
from ..time_utils import *
from ..js_utils import *