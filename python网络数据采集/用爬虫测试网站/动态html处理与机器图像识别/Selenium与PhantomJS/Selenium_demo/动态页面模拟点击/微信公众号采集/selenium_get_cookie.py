# coding:utf-8

'''
@author = super_fazai
@File    : selenium_get_cookie.py
@Time    : 2017/1/23 19:34
@connect : superonesfazai@gmail.com
'''

import time
import json
from pprint import pprint
from selenium import webdriver

post = {}

driver = webdriver.Chrome(executable_path='/Users/afa/myFiles/tools/chromedriver')
driver.get('https://mp.weixin.qq.com/')
time.sleep(2)

driver.find_element_by_name('account').clear()
driver.find_element_by_name('account').send_keys('你的微信公众号')
driver.find_element_by_name('password').clear()
driver.find_element_by_name('password').send_keys('你的微信公众号平台密码')


# 在自动输完密码之后记得点一下记住我
time.sleep(5)
driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
# 拿手机扫二维码！
time.sleep(20)
driver.get('https://mp.weixin.qq.com/')
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('cookie.txt', 'w+', encoding='utf-8') as f:
    f.write(cookie_str)