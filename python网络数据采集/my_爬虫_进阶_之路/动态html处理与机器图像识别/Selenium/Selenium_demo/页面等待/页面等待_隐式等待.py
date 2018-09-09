# coding = utf-8

'''
@author = super_fazai
@File    : 页面等待_隐式等待.py
@Time    : 2017/8/31 11:41
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 秒
driver.get('http://www.xxxx.com/loading')
myDynamicElement = driver.find_element_by_id('myDynamicElement')

# 当然如果不设置, 默认等待时间为0