# coding:utf-8

'''
@author = super_fazai
@File    : douyin_hot_auto_action.py
@Time    : 2017/8/7 13:22
@connect : superonesfazai@gmail.com
'''

"""
在不逆向获取签名算法情况下
* appium+mitmproxy实现抓取抖音
"""

import gc
from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class DouYinAutoAction(object):
    def __init__(self):
        # 驱动配置
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "fz_5_0_0",
            'appPackage': 'com.ss.android.ugc.aweme',
            'appActivity': '.main.MainActivity',
        }
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=desired_caps)
        self.wait = WebDriverWait(self.driver, 30)

    def _run(self):
        print('运行开始...')
        sleep(6)

        index = 1
        while True:
            if index == 1000:
                break

            print('正在滑动第{0}页...'.format(index))
            self.driver.swipe(0, 1000, 0, 1)
            sleep(2)
            index += 1

        print('运行完毕!')

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    _ = DouYinAutoAction()
    _._run()