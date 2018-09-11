# coding = utf-8

'''
@author = super_fazai
@File    : 改版_知乎_login.py
@Time    : 2017/9/1 15:00
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.request import urlretrieve
# import subprocess
import pytesseract
from PIL import Image
import os
import sys

class ZhiHuSelenium(object):
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/afa/myFiles/tools/chromedriver')

    def run(self):
        self.driver.get('https://www.zhihu.com/#signin')
        tmp_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        self.driver.find_element_by_class_name('signin-switch-password').click()
        time.sleep(1)
        # print(self.driver.page_source)
        self.driver.save_screenshot('密码login.png')
        # 发送邮箱, 账号
        self.driver.find_element_by_name('account').send_keys('superonesfazai@gmail.com')
        self.driver.find_element_by_name('password').send_keys('')
        self.driver.save_screenshot('密码login2.png')

        very_code = self.driver.find_element_by_class_name('Captcha-image').get_attribute('src')
        # print(very_code)  # https://www.zhihu.com/captcha.gif?r=1504254505979&type=login&lang=cn
        # 验证码图片下载
        time.sleep(1)
        urlretrieve(very_code, 'very_code_image.jpg')

        # test1: 验证码处理test1
        # tmp = subprocess.Popen(['tesseract', 'very_code_image.png', 'very_code_image_txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # time.sleep(1)
        # f = open('very_code_image_txt.txt', 'r')
        # time.sleep(1)
        # print(f.read())

        # test2: 验证码处理test2
        # image = Image.open('very_code_image.png')
        # text = pytesseract.image_to_string(image)
        # print(text)

        # test3: 验证码处理test3
        # command = 'convert ~/myFiles/codeDoc/PythonDoc/python网络数据采集/用爬虫测试网站/动态html处理与机器图像识别/机器视觉与Tesseract介绍/尝试处理知乎网验证码/very_code_image.jpg tmp.jpg && tesseract ~/myFiles/codeDoc/PythonDoc/python网络数据采集/用爬虫测试网站/动态html处理与机器图像识别/机器视觉与Tesseract介绍/尝试处理知乎网验证码/very_code_image.jpg tmp -l chi_sim'
        # os.system(command)
        # f = open('tmp.txt', 'r')
        # print(f.read())

        # test4：人工处理.... 成功！
        time.sleep(8)
        self.driver.find_element_by_class_name('sign-button').click()
        time.sleep(4)
        self.driver.save_screenshot('成功登录.png')

        # test5：使用已登录的cookies 成功!



if __name__ == '__main__':
    zhihu = ZhiHuSelenium()
    zhihu.run()

    # passwd:lrf654321



