# coding:utf-8

'''
@author = super_fazai
@File    : captcha_3.0.py
@connect : superonesfazai@gmail.com
'''

"""
极验的第三代验证码破解, 成功!
"""

from time import sleep
from gc import collect
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

class CrackCaptcha(object):
    def __init__(self):
        self.url = 'http://www.geetest.com/exp.html'
        self.driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    def _cracker(self):
        self.driver.get(self.url)

        self.driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='普惠版样式查看'])[1]/following::span[2]").click()

        sleep(60)

    def __call__(self, *args, **kwargs):
        return self._cracker()

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        collect()

if __name__ == '__main__':
    CrackCaptcha()()