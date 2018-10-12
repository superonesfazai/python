# coding:utf-8

'''
@author = super_fazai
@File    : dingding_auto_punch_clock.py
@connect : superonesfazai@gmail.com
'''

"""
钉钉自动打卡
"""

from gc import collect
from asyncio import get_event_loop
from pprint import pprint
from time import sleep
from appium import webdriver
from fzutils.common_utils import json_2_dict

class DingDing(object):
    def __init__(self):
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "BCD9XA1761101847",
            'appPackage': 'com.alibaba.android.rimet',
            'appActivity': 'com.alibaba.android.rimet.biz.SplashActivity',
        }
        self.driver = webdriver.Remote(
            command_executor=server,
            desired_capabilities=desired_caps)
        with open('/Users/afa/myFiles/pwd/dingding_pwd.json', 'r') as f:
            ding_info = json_2_dict(f.read())
        self.username = ding_info['username']
        self.pwd = ding_info['pwd']

    async def _login(self) -> bool:
        print('正在登陆中...')
        label = '-'
        login_res = False
        try:
            self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
            sleep(1.)
            self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
            sleep(2)
            try:  # 按钮会自动消失
                self.driver.find_element_by_id('com.huawei.systemmanager:id/btn_allow').click()
                sleep(1.)
            except:
                pass
            self.driver.find_element_by_id('com.alibaba.android.rimet:id/et_phone_input').clear()
            self.driver.find_element_by_id('com.alibaba.android.rimet:id/et_phone_input').send_keys(self.username)
            self.driver.find_element_by_id('com.alibaba.android.rimet:id/et_pwd_login').send_keys(self.pwd)
            self.driver.find_element_by_id('com.alibaba.android.rimet:id/btn_next').click()
            sleep(2.5)
            self.driver.find_element_by_xpath('//android.view.View[@content-desc="同意"]').click()
            label = '+'
            sleep(10)
            login_res = True
        except Exception as e:
            print(e)

        print('[{}] 登陆{}!'.format(label, '成功' if label == '+' else '失败'))

        return login_res

    async def _punch_clock(self) -> bool:
        '''
        打卡
        :return:
        '''
        try:
            self.driver.find_element_by_id('android:id/button2').click()
        except:
            pass
        sleep(1.)
        # 点击主按钮到打卡页面
        self.driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="工作"]/android.widget.RelativeLayout/android.widget.FrameLayout[1]').click()
        # 点击考勤打卡
        self.driver.find_element_by_xpath('//android.webkit.WebView[@content-desc="千行千面首页"]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[1]').click()
        sleep(4)

        # 允许定位
        self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
        self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
        sleep(1.5)

        try:
            # 上班打卡
            # self.driver.find_element_by_xpath('//android.view.View[@content-desc="上班打卡"]').click()
            # 下班打卡
            self.driver.find_element_by_xpath('//android.view.View[@content-desc="下班打卡"]').click()
            sleep(2.)
            print('@@@ 打卡成功!')
        except Exception as e:
            print(e)

        # 返回并退出登陆
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/back_icon').click()
        sleep(1.5)
        self.driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="我的"]/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.ImageView').click()
        sleep(1.5)
        self.driver.swipe(0, 1000, 0, 1)
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/rl_setting').click()
        sleep(1.2)
        self.driver.find_elements_by_id('com.alibaba.android.rimet:id/uidic_forms_item_text')[-1].click()
        sleep(2)
        self.driver.find_elements_by_class_name('android.widget.Button')[-1].click()
        print('退出登陆!')

        print('自动打卡脚本执行完毕!'.center(60, '*'))

        return True

    async def _fck_run(self) -> bool:
        # .biz.home.activity.HomeActivity
        # com.alibaba.android.user.login.SignUpWithPwdActivity
        # com.alibaba.android.user.login.SignUpActivity
        print('开始执行脚本...')
        sleep(5)

        login_res = await self._login()
        if login_res:
            punch_res = await self._punch_clock()

        return True

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = DingDing()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())