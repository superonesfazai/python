# coding:utf-8

'''
@author = super_fazai
@File    : login_and_get_cookies.py
@Time    : 2017/10/10 13:11
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import sleep
from random import randint

# chrome驱动地址
my_chrome_driver_path = '/Users/afa/myFiles/tools/chromedriver'
username = ''
pwd = ''

class Login(object):
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome(my_chrome_driver_path)
        self.start_url = 'https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&reg= http://member.1688.com/member/join/enterprise_join.htm?lead=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&leadUrl=http://login.1688.com/member/'

    def login(self):
        self.driver.get(self.start_url)
        self.driver.implicitly_wait(10)
        self.driver.save_screenshot('tmp_login1.png')
        self.driver.find_element_by_class_name('J_UserName').clear()
        self.driver.find_element_by_css_selector('span#J_StandardPwd input').clear()
        self.driver.find_element_by_class_name('J_UserName').send_keys(username)
        # time.sleep(2)
        self.driver.find_element_by_css_selector('span#J_StandardPwd input').send_keys(pwd)
        # time.sleep(2)
        self.driver.find_element_by_css_selector('button.J_Submit').click()
        # time.sleep(4)
        print('正在拖动滑块进行验证...请稍等')
        # 获取滑动滑块的标签元素
        dragger = self.driver.find_element_by_class_name('nc-lang-cnt')
        action = ActionChains(self.driver)
        action.click_and_hold(dragger).perform()  # 鼠标左键按下不放

        # sleep(3)
        # self.driver.find_element_by_css_selector('span#J_StandardPwd input').send_keys(pwd)

        # for index in range(2000):
        try:
            # random_number = randint(1, 5)
            action.move_by_offset(300, 0).perform()  # 平行移动鼠标
        except UnexpectedAlertPresentException as e:
            print(e)
            # action.reset_actions()
            # sleep(0.02)  # 等待停顿时间
        action.click_and_hold(dragger).perform()  # 鼠标左键按下不放
        sleep(3)
        # # 重新赋值设置
        # self.driver.find_element_by_class_name('J_UserName').clear()
        # self.driver.find_element_by_css_selector('span#J_StandardPwd input').clear()
        # self.driver.find_element_by_class_name('J_UserName').send_keys(username)
        # # time.sleep(2)
        # self.driver.find_element_by_css_selector('span#J_StandardPwd input').send_keys(pwd)
        # # time.sleep(2)
        # self.driver.find_element_by_css_selector('button.J_Submit').click()
        sleep(4)
        # self.driver.implicitly_wait(10)
        self.driver.save_screenshot('tmp_login2.png')


if __name__ == '__main__':
    login_ali = Login()
    login_ali.login()


