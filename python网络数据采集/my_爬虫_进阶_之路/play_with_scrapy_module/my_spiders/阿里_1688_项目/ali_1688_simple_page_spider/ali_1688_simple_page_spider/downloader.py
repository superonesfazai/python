# coding:utf-8

'''
@author = super_fazai
@File    : downloader.py
@Time    : 2017/9/26 15:47
@connect : superonesfazai@gmail.com
'''

import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from pprint import pprint
from .settings import EXECUTABLE_PATH

import sys
import os
sys.path.append(os.getcwd())
# print(os.getcwd())

class CustomDownloader(object):
    def __init__(self):
        """
        初始化带cookie的驱动
        """
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000   # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.customHeaders.Cookie'] = self.get_cookies_from_cookies_txt()
        print('============| phantomjs即将执行 |')
        tmp_execute_path = EXECUTABLE_PATH
        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
        print('============| phantomjs执行成功 |')
        self.driver.set_window_size(1200, 2000)      # 设置默认大小，避免默认大小显示
        wait = ui.WebDriverWait(self.driver, 10)   # 显示等待n秒, 每过0.5检查一次页面是否加载完毕

    def visit_page(self, url):
        """
        动态js模拟网页下拉
        :param url:
        :return:
        """
        print('============| 正在加载网站...... |')
        self.driver.get(url)
        self.driver.implicitly_wait(15)

        # self.driver.save_screenshot('./截图.png')       # 下拉截图方便调试
        content = self.driver.page_source.encode('utf-8')
        print('============| 网页加载完毕.......... |')
        # pprint(content.decode())
        return content

    def get_cookies_from_cookies_txt(self):
        with open('cookies.txt', 'rb') as f:
            line = f.read().decode('utf-8').strip('\n')
        return str(line)

    def __del__(self):
        # self.driver.quit()
        pass

