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

username = ""
password = "111"

class Moments(object):
    def __init__(self):
        # 驱动配置
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Droid4X_MAC",
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
        # dl = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/d1w")))
        # dl.click()

        # 多个就返回一个list对象
        _dl = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.Button')))[0]
        _dl.click()

        # 点击用qq号登陆
        # qq = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/bwm")))
        # qq.click()

        _qq = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'android.widget.Button')))
        print(_qq)
        _qq[0].click()      # 根据index的号码如3, 就现在element="3"的元素

        # # passwd = self.driver.find_elements_by_id("com.tencent.mm:id/hx")
        # # 输入账号
        # user_passwd = self.driver.find_elements_by_id("com.tencent.mm:id/hx")
        # user = user_passwd[0]
        # passwd = user_passwd[1]
        # user.set_text(username)
        # # 输入密码
        # passwd.set_text(password)

        _user_passwd = self.driver.find_element_by_class_name('android.widget.EditText')
        _user = _user_passwd[0]
        _passwd = _user_passwd[1]
        _user.set_text(username)
        _passwd.set_text(password)

        # 点击登陆按钮
        # submit = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/bwn")))
        # submit.click()

        _submit = self.wait.until(EC.presence_of_all_elements_located(By.CLASS_NAME, 'android.widget.Button'))
        print(_submit)
        _submit[1].click()

        # 不匹配通讯录
        alk = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/alk")))
        alk.click()

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
