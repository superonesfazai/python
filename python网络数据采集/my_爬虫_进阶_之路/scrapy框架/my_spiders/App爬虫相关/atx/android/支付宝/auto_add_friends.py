# coding:utf-8

'''
@author = super_fazai
@File    : auto_add_friends.py
@connect : superonesfazai@gmail.com
'''

"""
支付宝批量加好友
"""

from gc import collect
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError
from fzutils.spider.async_always import *

class ALiPay(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        # TODO 魅族采坑记(appium速度太慢, 改用atx)
        # 魅族要关闭flyme支付保护, 否则自动化打开支付宝, usb连接就会被自动断开, 导致无法进行后续自动化操作
        # 关闭方式: 手机管家 -> 右上角设置 -> 关闭flyme支付保护

        # 驱动配置
        # server = "http://localhost:4723/wd/hub"
        # desired_caps = {
        #     "platformName": "Android",
        #     "deviceName": "M1816",
        #     'appPackage': 'com.eg.android.AlipayGphone',
        #     'appActivity': '.AlipayLogin',
        #     'platformVersion': '8.1',
        #     'automationName': 'appium',                     # 还是用appium, 不用uiautomator2
        #     'autoLaunch': 'true',                           # 只要autoLaunch为false,就不会安装ServerApk
        #     # 此外: @@ 所有一定要把uiautomator2Server加入神隐模式的白名单,或者关闭神隐模式.即让它能后台运行 (从电量管理设置)
        # }

        # 打开meizu原生的计算器, 可以正常运行, 但是支付宝uiautomator无法打开
        # desired_caps = {
        #     "platformName": "Android",
        #     "deviceName": "M1816",
        #     'appPackage': 'com.meizu.flyme.calculator',
        #     'appActivity': 'com.meizu.flyme.calculator.Calculator',
        #     'platformVersion': '8.1',
        #     'automationName': 'appium',
        #     'autoLaunch': 'true',
        # }
        # self.driver = webdriver.Remote(command_executor=server, desired_capabilities=desired_caps)
        # self.wait = WebDriverWait(self.driver, 30)

        # adb device 查看
        self.d = u2.connect("816QECTK24ND8")
        print(self.d.info)
        self.d.set_fastinput_ime(True)
        self.d.debug = True
        self.now_session = self.d.session(pkg_name="com.eg.android.AlipayGphone")
        self.phone_list = []
        # 支付宝登录页面类型
        self.login_type = 0
        with open('phone.txt', 'r') as f:
            for line in f:
                self.phone_list.append(line.replace('\n', ''))
        pprint(self.phone_list)
        self.phone_list = self.phone_list[150:]
        print('total phone num: {}'.format(self.phone_list))

    async def _fck_run(self):
        # TODO 先退出登录
        print('开始运行...')
        login_res = await self._login()
        await self._enter_add_friends_page()
        await self._start_add_friends()

        print('运行完毕!')

    async def _login(self) -> bool:
        """
        登录支付宝
        :return:
        """
        if self.d(text=u"输入手机号，使用支付宝").exists():
            # 初始化的情况
            self.d(text=u"输入手机号，使用支付宝").click()
            self.d(className="android.widget.EditText").send_keys('18698570079')
            self.d(resourceId="com.ali.user.mobile.security.ui:id/next_btn").click()
            # face btn
            self.d(resourceId="com.ali.user.mobile.security.ui:id/faceLoginButtonLayout").click()
            # allow use 相机
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
        else:
            # 已登录但是退出后的情况  即点击下方头像登录的情况
            # 点击头像
            self.login_type = 1
            self.d(resourceId="com.ali.user.mobile.security.ui:id/userAccountImage").click()
            # 刷脸btn
            self.d(resourceId="com.ali.user.mobile.security.ui:id/faceLoginButtonLayout").click()

        while True:
            a = input('刷脸登陆是否已完成?(y):')
            if a == 'y':
                break

        if self.login_type == 0:
            # 下一步
            self.d(resourceId="com.alipay.mobile.antui:id/btn_confirm").click()
            # allow 定位
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()

        return True

    async def _enter_add_friends_page(self):
        """
        进入加好友页面
        :return:
        """
        # 点朋友
        self.d(resourceId="com.alipay.mobile.socialwidget:id/social_tab_text").click()
        if self.login_type == 0:
            # allow 访问通讯录
            self.d(resourceId="com.alipay.mobile.antui:id/ensure").click()
            # allow 读取联系人信息
            self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()

        # 点 '+' 进行添加好友
        self.d(resourceId="com.alipay.mobile.socialwidget:id/title_more_menu_button").click()
        # 添加朋友
        self.d(resourceId="com.alipay.mobile.antui:id/item_name", text=u"添加朋友").click()

        # 点击输入框
        self.d(resourceId="com.alipay.mobile.antui:id/search_bg").click()

        return None

    async def _start_add_friends(self):
        """
        开始批量加好友(每日添加好友有上线!)
        :return:
        """
        index = 0
        while index < len(self.phone_list):
            phone_num = self.phone_list[index]

            try:
                # 清空输入框
                self.d(resourceId="com.alipay.mobile.ui:id/social_search_normal_input").clear_text()
                # 输入手机号
                self.d(resourceId="com.alipay.mobile.ui:id/social_search_normal_input").send_keys(phone_num)

                # 点击搜索
                self.d(resourceId="com.alipay.mobile.contactsapp:id/search_tip_TableView").click()

                # 存在多个对应的账号
                # 只取第一个
                user_name_ele_first = self.d(resourceId="com.alipay.mobile.contactsapp:id/user_name")
                # 是否存在多个账户对应的页面, 存在则True
                user_name_ele_first_exists = user_name_ele_first.exists()
                print('user_name_ele_first 是否存在?: {}'.format(user_name_ele_first_exists))
                await async_sleep(2)
                if not user_name_ele_first_exists:
                    add_friend_btn = self.d(resourceId="com.alipay.android.phone.wallet.profileapp:id/ll_menu2")
                    print('8' * 50)
                    print('add_friend_btn 是否存在?: {}'.format(add_friend_btn.exists()))
                    if add_friend_btn.exists():
                        # 只对应单个支付宝账号
                        pass
                    else:
                        index += 1
                        print('[-] 添加 {} fail! 原因: 账号不存在!'.format(phone_num))

                        # 也存在已被添加的账号, 作为异常抛出
                        ensure_btn_ele = self.d(resourceId="com.alipay.mobile.antui:id/ensure")
                        if ensure_btn_ele.exists():
                            ensure_btn_ele.click(timeout=4)
                        else:
                            # 防止卡住, 进行附近点击
                            self.d.click(0.755, 0.265)
                            continue

                        add_friend_btn_text = add_friend_btn.get_text(timeout=4)
                        # print('add_friend_btn_text: {}'.format(add_friend_btn_text))
                        if add_friend_btn_text == '发消息':
                            print('[-] 添加 {} fail! 原因: 该账号已被添加!'.format(phone_num))
                            continue
                        else:
                            pass

                        continue
                else:
                    pass

                if user_name_ele_first_exists:
                    user_name_ele_first.click()

                # 加好友页面处理
                # 加好友 btn
                self.d(resourceId="com.alipay.android.phone.wallet.profileapp:id/ll_menu2").click()
                # 朋友验证 发送btn
                self.d(resourceId="com.alipay.mobile.ui:id/title_bar_generic_button").click()

                # 返回加好友页面
                self.d(resourceId="com.alipay.mobile.antui:id/back_button").click()

                print('[+] 添加 {} success!'.format(phone_num))
                index += 1
            except (AssertionError, UiObjectNotFoundError) as e:
                print(e)
                index += 1

        return

    def __del__(self):
        try:
            self.d
        except:
            pass
        try:
            self.driver.quit()
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = ALiPay()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
