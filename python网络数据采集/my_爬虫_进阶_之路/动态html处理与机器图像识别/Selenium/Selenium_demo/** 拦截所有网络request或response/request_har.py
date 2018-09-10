# coding:utf-8

'''
@author = super_fazai
@File    : request_har.py
@Time    : 2018/3/13 16:28
@connect : superonesfazai@gmail.com
'''

"""
拦截所有网络请求或者网络请求结果

使用须知: (具体操作可见: https://github.com/lightbody/browsermob-proxy)
    先启动browsermob-proxy eg: ./browsermob-proxy -port 8080 --use-littleproxy false
"""

import json, time
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
from pprint import pprint

# bmp can downloaded from: https://github.com/lightbody/browsermob-proxy/releases
server = Server("/Users/afa/myFiles/tools/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

proxy.blacklist(".*gov.cn.*", 404)      # 拦截这个re的请求，返回404
proxy.new_har(options={
    'captureContent': True
})
# print(proxy.proxy)

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)

# 测试途牛的数据
# browser.get('http://www.tuniu.com/flight/intel/sha-bkk')
# Wait(browser, 60).until(
#     Expect.text_to_be_present_in_element((By.ID, "loadingStatus"), u"共搜索")
# )
#
# for entry in proxy.har['log']['entries']:
#     if 'remote/searchFlights' in entry['request']['url']:
#         result = json.loads(entry['response']['content']['text'])
#         for key, item in result['data']['flightInfo'].items():
#             print(key)

# 测试淘宝头条的数据
browser.get('https://market.m.taobao.com/apps/market/toutiao/portal.html?wh_weex=true&data_perfetch=true')

# print(proxy.har)
for entry in proxy.har['log']['entries']:
    # print(entry['request']['url'])
    if 'jsv=2.4.2' in entry['request']['url']:
        result = entry['response']['content']['text']
        print(result)

server.stop()
browser.quit()
