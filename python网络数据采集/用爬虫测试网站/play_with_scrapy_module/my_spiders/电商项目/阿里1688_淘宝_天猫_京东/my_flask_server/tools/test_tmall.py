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
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            # self.driver.save_screenshot('tmp_login1.png')

            locator = (By.CSS_SELECTOR, 'div#description')
            try:
                WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('获取div#description错误: ', e)
            else:
                print('div#description加载完毕...')
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 10 seconds(当获取验证码时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        body = self.driver.page_source

        # 过滤
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        body = re.compile(r'<div id="description".*?>.*</body>').findall(body)[0]
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
#
# a = test()
#
# tmall_url = input('请输入待爬取的天猫商品地址: ')
# tmall_url.strip('\n').strip(';')
# body = a.deal_with_div(tmall_url)
# print(body)

print('9' * 100)

tmp = '//h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?jsv=2.4.4&amp;appKey=12574478&amp;t=1510026132370&amp;sign=3c26382438c3932cf35b42afb035bf12&amp;api=mtop.relationrecommend.WirelessRecommend.recommend&amp;v=2.0&amp;type=jsonp&amp;dataType=jsonp&amp;callback=mtopjsonp4&amp;data=%7B%22appId%22%3A%22766%22%2C%22params%22%3A%22%7B%5C%22itemid%5C%22%3A%20%5C%2242613920441%5C%22%2C%5C%22sellerid%5C%22%3A%20%5C%22113773411%5C%22%7D%22%7D'
tmp = re.compile(r'&amp;').sub('&', tmp)
print(tmp)