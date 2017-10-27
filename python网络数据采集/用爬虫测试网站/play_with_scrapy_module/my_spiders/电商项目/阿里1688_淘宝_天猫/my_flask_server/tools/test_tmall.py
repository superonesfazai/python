# coding:utf-8

'''
@author = super_fazai
@File    : test_tmall.py
@Time    : 2017/10/27 16:12
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import re
import gc

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

class test():
    def __init__(self):
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    def deal_with_div(self, url):
        self.driver.set_page_load_timeout(5)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(8)
            # self.driver.save_screenshot('tmp_login1.png')

            locator = (By.CSS_SELECTOR, 'div#description')
            try:
                WebDriverWait(self.driver, 8, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('获取div#description错误: ', e)
            else:
                print('div#description加载完毕...')
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 5 seconds(当获取验证码时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        body = self.driver.page_source

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body = re.compile(r'<div id="description".*?>.*?</div><div ').findall(body)[0]
        body = re.compile(r'src="data:image/png;.*?"').sub('', body)
        body = re.compile(r'data-ks-lazyload').sub('src', body)
        body = re.compile(r'https:').sub('', body)
        body = re.compile(r'src="').sub('src=\"https:', body)

        body = re.compile(r'<table.*?>.*?</table>').sub('', body)  # 防止字段太长
        body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">.*</div>').sub('', body)
        # body = re.compile(r'<div class="rmsp rmsp-bl rmsp-bl">')

        self.driver.quit()
        gc.collect()
        return body

a = test()

# url = 'https://mdetail.tmall.com/templates/pages/desc?id=39993036168'
url = 'http://mdetail.tmall.com/templates/pages/desc?id=557905387519'
body = a.deal_with_div(url)
print(body)
