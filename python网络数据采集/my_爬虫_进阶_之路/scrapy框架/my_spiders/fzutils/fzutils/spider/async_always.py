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
from time import sleep
from pprint import pprint
from scrapy.selector import Selector

from asyncio import get_event_loop, wait
from asyncio import sleep as async_sleep
from async_timeout import timeout as async_timeout
from asyncio import TimeoutError as AsyncTimeoutError

from ..internet_utils import *
from .fz_requests import Requests
from ..common_utils import *
from ..aio_utils import *
from ..time_utils import *
from ..js_utils import *
from ..sms_utils import *
from ..safe_utils import *