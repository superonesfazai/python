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
chrome_options.add_argument('--proxy-server={0}'.format('183.136.218.253:80'))

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
# driver.get('http://httpbin.org/ip')
driver.get('http://www.baidu.com')
# print(driver.page_source)

# driver.quit()
