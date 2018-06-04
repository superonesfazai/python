# coding:utf-8

'''
@author = super_fazai
@File    : chrome驱动设置代理.py
@Time    : 2017/11/1 10:18
@connect : superonesfazai@gmail.com
'''

"""
测试未通过
"""

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://183.136.218.253:80')
chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
chrome_options.add_argument('--disable-gpu')
# 设置无图模式
prefs = {
    'profile.managed_default_content_settings.images': 2
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--proxy-server={0}'.format('101.96.10.5:80'))

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
# driver.get('http://httpbin.org/ip')
# driver.get('https://www.taobao.com')
driver.get('https://www.baidu.com')
print(driver.page_source)

driver.quit()
