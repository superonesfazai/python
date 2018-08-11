# coding:utf-8

'''
@author = super_fazai
@File    : 模拟登录淘宝.py
@Time    : 2018/4/14 19:11
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')
from selenium import webdriver
from time import sleep
from settings import TAOBAO_USERNAME, TAOBAO_PASSWD

chrome_options = webdriver.ChromeOptions()

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)

try:
    driver.get('https://detail.m.tmall.com/item.htm?id=541107920538')

    print('要求淘宝登录...')
    # 要求淘宝登录就先登录
    print(TAOBAO_USERNAME, TAOBAO_PASSWD)
    driver.find_element_by_name('TPL_username').send_keys(TAOBAO_USERNAME)
    driver.find_element_by_name('TPL_password').send_keys(TAOBAO_PASSWD)

    driver.find_element_by_css_selector('button#btn-submit').click()
    driver.find_element_by_css_selector('span.km-dialog-btn').click()
    driver.find_element_by_css_selector('div.icon.nc-iconfont.icon-notclick').click()
    print('淘宝登录完成!')
    sleep(3)
    driver.find_element_by_name('TPL_password').send_keys(TAOBAO_PASSWD)
    driver.find_element_by_css_selector('button#btn-submit').click()

    print(driver.page_source)
except Exception as e:
    print(e)
finally:
    sleep(2*60)
    driver.quit()

driver.quit()