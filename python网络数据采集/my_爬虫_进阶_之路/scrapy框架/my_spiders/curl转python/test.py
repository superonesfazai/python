# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from __future__ import unicode_literals

from ftfy import fix_text
from fzutils.ip_pools import (
    fz_ip_pool,
    ip_proxy_pool,
    sesame_ip_pool,
    tri_ip_pool,)
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_driver import (
    BaseDriver, 
    CHROME,)
from fzutils.spider.fz_phantomjs import CHROME_DRIVER_PATH
from fzutils.url_utils import unquote_plus
from fzutils.img_utils import save_img_through_url
from fzutils.spider.fz_driver import PHONE
from fzutils.common_utils import _print
from fzutils.data.excel_utils import read_info_from_excel_file
from fzutils.spider.selector import *
from fzutils.spider.async_always import *

phone_headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_random_phone_ua(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
# company_id = '13250586855'
# info_url = 'https://3g.made-in-china.com/company-{}/info.html'.format(company_id)
# contact_url = 'https://3g.made-in-china.com/company-{}/contact.html'.format(company_id)
# info_body = Requests.get_url_body(url=info_url, headers=phone_headers, ip_pool_type=tri_ip_pool)
# print(info_body)
# contact_body = Requests.get_url_body(url=contact_url, headers=phone_headers, ip_pool_type=tri_ip_pool)
# print(contact_body)


