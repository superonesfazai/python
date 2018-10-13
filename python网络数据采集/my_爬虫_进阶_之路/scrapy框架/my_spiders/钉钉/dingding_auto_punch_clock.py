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
from fzutils.time_utils import get_shanghai_time

# 上班打卡时间点
start_work_time = '9:00'
# 下班打卡时间点
end_work_time = '21:00'

class DingDing(object):
    def __init__(self, username, pwd, start_work:bool=False, end_work:bool=False):
        '''
        :param username: 用户名
        :param pwd: 密码
        :param start_work: 上班打卡
        :param end_work: 下班打卡
        '''
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
        self.username = username
        self.pwd = pwd
        self.start_work = start_work
        self.end_work = end_work

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
            sleep(2.)
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
            if self.start_work:
                # 上班打卡
                self.driver.find_element_by_xpath('//android.view.View[@content-desc="上班打卡"]').click()
            if self.end_work:
                # 下班打卡
                self.driver.find_element_by_xpath('//android.view.View[@content-desc="下班打卡"]').click()

            sleep(2.)
            print('@@@ {}打卡成功!'.format('上班' if self.start_work else '下班'))
        except Exception as e:
            print(e)

        logout_res = await self._logout()
        if not logout_res:
            print('退出登陆失败!')

        print('自动打卡脚本执行完毕!'.center(60, '*'))

        return True

    async def _logout(self) -> bool:
        '''
        退出登陆
        :return:
        '''
        # 返回并退出登陆
        try:
            self.driver.find_element_by_id('com.alibaba.android.rimet:id/back_icon').click()
            sleep(1.5)
        except Exception:
            print('考勤返回按钮没有发现!跳过!')
        self.driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="我的"]/android.widget.RelativeLayout/android.widget.FrameLayout[1]/android.widget.ImageView').click()
        sleep(1.5)
        self.driver.swipe(0, 1000, 0, 1)
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/rl_setting').click()
        sleep(1.2)
        self.driver.find_elements_by_id('com.alibaba.android.rimet:id/uidic_forms_item_text')[-1].click()
        sleep(2)
        self.driver.find_elements_by_class_name('android.widget.Button')[-1].click()
        print('退出登陆!')

        return True

    async def _fck_run(self) -> bool:
        # print('waking up phone...')
        # self.driver.keyevent(26)
        # self.driver.swipe(0, 1000, 0, 1)
        print('开始执行脚本...')
        sleep(5)

        login_res = await self._login()
        if login_res:
            punch_res = await self._punch_clock()
            # await self._logout()

        return True

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        collect()

def main():
    def get_hour_minute(target_time):
        '''得到打卡hour, minute'''
        _ = target_time.split(':')
        return int(_[0]), int(_[1])

    with open('/Users/afa/myFiles/pwd/dingding_pwd.json', 'r') as f:
        ding_info = json_2_dict(f.read())

    start_work_time_hour, start_work_time_minute = get_hour_minute(start_work_time)
    end_work_time_hour, end_work_time_minute = get_hour_minute(end_work_time)

    while True:
        now_time = get_shanghai_time()
        hour, minute= now_time.hour, now_time.minute
        start_work, end_work = False, False
        if hour in (start_work_time_hour, end_work_time_hour):
            if hour == start_work_time_hour and minute > start_work_time_minute:
                start_work = True

            elif hour == end_work_time_hour and minute > end_work_time_minute:
                end_work = True

            if start_work or end_work:
                _ = DingDing(username=ding_info['username'], pwd=ding_info['pwd'], start_work=start_work, end_work=end_work)
                loop = get_event_loop()
                res = loop.run_until_complete(_._fck_run())
                if not res:
                    print('打卡失败!重试中...')
                    continue

                sleep(60 * 15)

        else:
            print('{} 未在打卡时间点...'.format(now_time))
            sleep(60)

if __name__ == '__main__':
    main()