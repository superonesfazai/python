# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/5/12 10:12
@connect : superonesfazai@gmail.com
'''

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'Droid4X_MAC',
    'appPackage': 'com.tencent.mm',
    'appActivity': '.ui.LauncherUI'
}

driver = webdriver.Remote(server, desired_caps)     # 启动

wait = WebDriverWait(driver, 30)
login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
phone.set_text('18888888888')

driver.quit()