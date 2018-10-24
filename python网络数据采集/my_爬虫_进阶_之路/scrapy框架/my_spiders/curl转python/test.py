# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
import re
from scrapy.selector import Selector
from time import sleep

from fzutils.spider.fz_requests import Requests
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_driver import BaseDriver, CHROME
from fzutils.spider.fz_phantomjs import CHROME_DRIVER_PATH
from fzutils.internet_utils import get_random_phone_ua, get_random_pc_ua, _get_url_contain_params
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import get_shanghai_time, datetime_to_timestamp
from fzutils.common_utils import get_random_int_number
