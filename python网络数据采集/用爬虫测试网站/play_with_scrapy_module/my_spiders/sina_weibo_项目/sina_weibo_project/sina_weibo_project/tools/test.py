# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/9/26 12:00
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import time
from pprint import pprint

class test():
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/afa/myFiles/tools/chromedriver')

    def run(self):
        login_url = 'https://weibo.com/'

        username = 15661611306
        passwd = 'lrf654321'

        self.driver.get(login_url)
        time.sleep(3)

        # pprint(self.driver.page_source)

        self.driver.find_element_by_id('loginname').send_keys(username)
        self.driver.find_element_by_css_selector('.password input').send_keys(passwd)

        self.driver.find_element_by_css_selector('.W_btn_a span').click()

        time.sleep(4)

        # pprint(self.driver.page_source)
        self.driver.save_screenshot('1.png')
a = test()
a.run()