# coding:utf-8

'''
@author = super_fazai
@File    : wx_circle_of_friends.py
@connect : superonesfazai@gmail.com
'''

"""
微信朋友圈爬虫
"""

from gc import collect
from asyncio import get_event_loop
from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class WXCircleOfFriendsSpider(object):
    def __init__(self):
        # 驱动配置
        server = "http://localhost:4723/wd/hub"
        desired_caps = {
            "platformName": "Android",
            "deviceName": "BCD9XA1761101847",
            'appPackage': 'com.tencent.mm',
            'appActivity': '.ui.LauncherUI',
        }
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=desired_caps)
        self.wait = WebDriverWait(self.driver, 30)
        self.phone_num = str(18698570079)

    async def _login(self) -> bool:
        print('开始运行...')
        sleep(5)
        try:
            # 权限点击
            self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
            sleep(1.5)
            self.driver.find_element_by_id('com.android.packageinstaller:id/do_not_ask_checkbox').click()
            self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
            sleep(1.5)

            # 短信登陆
            self.driver.find_element_by_id('com.tencent.mm:id/czy').click()
            sleep(1)
            self.driver.find_element_by_id('com.tencent.mm:id/hk').send_keys(self.phone_num)
            self.driver.find_element_by_id('com.tencent.mm:id/akc').click()
            sleep(3)
            self.driver.find_element_by_id('com.tencent.mm:id/bw6').click()
            sleep(1)
            self.driver.find_element_by_id('com.tencent.mm:id/c8z').click()     # 获取验证码
            sleep(.5)
            self.driver.find_element_by_id('com.tencent.mm:id/alo').click()     # 确认发送验证码
            verification_code = input('请输入手机获取到的验证码:')
            self.driver.find_elements_by_class_name('android.widget.EditText')[1].send_keys(verification_code)
            self.driver.find_element_by_id('com.tencent.mm:id/akc').click()
            print('正在登陆微信...')
            sleep(16)
            self.driver.find_element_by_id('com.tencent.mm:id/hp').click()      # 返回(跳过修改密码页面)
            sleep(2)
            self.driver.find_element_by_id('com.tencent.mm:id/aln').click()     # 是否查看通讯录(否)
            sleep(5)
            self.driver.find_element_by_id('com.tencent.mm:id/oc').click()      # 进入微信
            print('成功进入微信页面...等待数据同步完毕...')
            sleep(60*1.5)

            self.driver.find_elements_by_id('com.tencent.mm:id/ayf')[2].click() # 点击朋友圈
            self.driver.find_elements_by_id('com.tencent.mm:id/a9o')[1].click() # 进入朋友圈
        except Exception as e:
            print(e)
            return False

        return True

    async def _fck_run(self) -> bool:
        login_res = await self._login()
        if not login_res:
            print('登录失败!')
            return False

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = WXCircleOfFriendsSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())