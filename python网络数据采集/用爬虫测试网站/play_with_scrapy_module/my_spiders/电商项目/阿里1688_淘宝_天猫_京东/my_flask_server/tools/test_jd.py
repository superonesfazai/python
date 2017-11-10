# coding:utf-8

'''
@author = super_fazai
@File    : test_jd.py
@Time    : 2017/11/10 13:36
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import requests
from time import sleep
from pprint import pprint

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'mitem.jd.hk',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',      # 随机一个请求头
}

# cookies = 'sid=e744b6e8ba5d52a15fdbb98afffb04d3'
print('--->>>初始化phantomjs驱动中<<<---')
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
cap['phantomjs.page.settings.loadImages'] = False
cap['phantomjs.page.settings.disk-cache'] = True
cap['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'  # 随机一个请求头
# cap['phantomjs.page.customHeaders.Cookie'] = cookies
tmp_execute_path = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
print('--->>>初始化phantomjs完毕<<<---')
url = 'https://mitem.jd.hk/cart/cartNum.json'
driver.get(url)
pprint(driver.get_cookie(name='sid'))
if driver.get_cookie(name='sid') is None:
    driver.get(url)
url = 'https://mitem.jd.hk/ware/detail.json?wareId=2443358'
driver.get(url)
print(driver.page_source)
driver.quit()

