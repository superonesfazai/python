# coding:utf-8

'''
@author = super_fazai
@File    : get_pyppeteer_chrome_download_info.py
@connect : superonesfazai@gmail.com
'''

"""
获取pyppeteer chrome 下载路径信息
"""

from pyppeteer import (
    chromium_downloader,
    __chromium_revision__,)

# 下载速度很慢, 可在服务器(wget xxx)上下好再回传本地
print('chromium_revision默认版本是：{}'.format(__chromium_revision__))
print('可执行文件默认路径：{}'.format(chromium_downloader.chromiumExecutable.get('mac')))
print('mac平台下载链接为：{}'.format(chromium_downloader.downloadURLs.get('mac')))
print('linux平台下载链接为：{}'.format(chromium_downloader.downloadURLs.get('linux')))