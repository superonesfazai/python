# coding = utf-8

'''
@author = super_fazai
@File    : 网站模拟登录_douban_test.py
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.PhantomJS()
driver.get('http://www.douban.com')

# 输入账号和密码
driver.find_element_by_name('from_emai').send_keys('xxx@xxx.com')
driver.find_element_by_name('from_password').send_keys('xxxxxx')

# 模拟点击登录
driver.find_element_by_xpath('//input[@class="bn-submit"]').click()     # 注意: 点击要具体到哪个input, 而不是其父元素

time.sleep(3)

# 生成登录后快照
driver.save_screenshot('douban.png')

with open('douban.html', 'w') as file:
    file.wirte(driver.page_source)

driver.quit()