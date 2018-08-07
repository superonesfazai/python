# coding:utf-8

'''
@author = super_fazai
@File    : moments.py
@Time    : 2018/5/25 20:37
@connect : superonesfazai@gmail.com
'''

import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = "2939161681"
password = "111"

class Moments(object):
    def __init__(self):
        # 驱动配置
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "fz_5_0_0",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
        }
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=desired_caps)
        self.wait = WebDriverWait(self.driver, 30)

    def login(self):
        """
        登陆微信
        :return:
        """
        # 登录按钮
        _dl = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d75')))
        _dl.click()

        # 返回一个list
        _qq = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/c1t')))[0]
        print(_qq)
        _qq.click()      # 根据index的号码如3, 就现在element="3"的元素

        qq_id_passwd = self.driver.find_elements_by_id('com.tencent.mm:id/hz')
        # 输qq号
        qq_id_passwd[0].set_text(username)
        # 输密码
        qq_id_passwd[1].set_text(password)

        # 点击登陆按钮
        submit = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/c1u')))
        submit.click()

    def enter(self):
        # 点击"发现"选项卡
        finds = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@resource-id='com.tencent.mm:id/ayn']")))
        finds[2].click()
        # 进入朋友圈
        friend = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/a9d")))
        friend.click()

    def crawl(self):
        flick_start_x = 300
        flick_start_y = 300
        flick_distance = 700
        while True:
            self.driver.swipe(flick_start_x, flick_start_y+flick_distance, flick_start_x, flick_start_y)
            self.get_page_info()

    def get_page_info(self):
        items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@resource-id='com.tencent.mm:id/ddn']//android.widget.LinearLayout")))
        for item in items:
            try:
                # 昵称
                nickname = item.find_element_by_id("com.tencent.mm:id/apv").get_attribute("text")
                # 正文
                content = item.find_element_by_id("com.tencent.mm:id/deq").get_attribute("text")
                print("{}---{}".format(nickname, content.replace("\n", "")))
            except NoSuchElementException:
                pass

    def run(self):
        # 登陆微信
        self.login()
        # 进入朋友圈
        self.enter()
        # 抓取信息模拟上滑
        self.crawl()


if __name__ == "__main__":
    m = Moments()
    m.run()
