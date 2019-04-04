# coding:utf-8

'''
@author = super_fazai
@File    : auto_add_friends.py
@connect : superonesfazai@gmail.com
'''

"""
支付宝批量加好友

启动方式:
1. python3 -m weditor 
2. python3 -m uiautomator2 init 
"""

from gc import collect
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError

from exceptions import AddFriendsToTheUpperLimitException
from fzutils.spider.app_utils import (
    u2_page_back,
    u2_up_swipe_some_height,)
from fzutils.spider.async_always import *

class ALiPay(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,)
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
        self.d = u2.connect(addr="816QECTK24ND8")        # meizu
        # self.d = u2.connect("U4AYPNDYCITWAE6D")     # oppo
        print(self.d.info)
        self.d.set_fastinput_ime(True)
        self.d.debug = False
        self.now_session = self.d.session(pkg_name="com.eg.android.AlipayGphone")
        self.phone_list = []
        # 支付宝登录页面类型
        self.login_type = 0
        # 截图保存的位置
        self.screen_save_path = '/Users/afa/myFiles/tmp/uiautomator2_files/screen/'
        # 小手位置
        self.hand_bounds = {
            'left': 676,
            'top': 0,
            'right': 720,
            'bottom': 45,
        }
        # 小手相似度
        self.hand_img_similarity = .84
        # 不收取的好友list
        self.no_collect_friends_list = ['方波',]

    async def _fck_run(self):
        # TODO 先退出登录
        print('开始运行...')
        login_res = await self._login()

        # 批量加好友
        # await self._init_phone_list()
        # await self._batch_add_friends()

        # 蚂蚁森林
        await self._ant_forest_steal_energy()

        print('运行完毕!')

    async def _init_phone_list(self):
        """
        初始化 phone list
        :return:
        """
        with open('phone.txt', 'r') as f:
            for line in f:
                self.phone_list.append(line.replace('\n', ''))
        pprint(self.phone_list)
        self.phone_list = self.phone_list[:]
        print('total phone num: {}'.format(len(self.phone_list)))

        return

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

    async def _ant_forest_steal_energy(self):
        """
        蚂蚁森林偷能量
        :return:
        """
        await self._init_ant_forest()
        await self._join_into_friend_page()
        await self._start_steal_energy()

    async def _join_into_friend_page(self) -> None:
        """
        进入好友列表页面
        :return:
        """
        # 向下滑动
        while True:
            try:
                self.d.swipe(0., 0.7, 0., 0.2)
                assert self.d(description=u"查看更多好友").exists() is not True
            except AssertionError:
                break
        print('已下滑至底部!')

        # 查看更多好友
        self.d(description=u"查看更多好友").click()
        print('获取好友页面中...')
        await async_sleep(6)

    async def _init_ant_forest(self) -> None:
        """
        初始化蚂蚁森林
        :return:
        """
        # 点蚂蚁森林
        self.d(
            resourceId="com.alipay.android.phone.openplatform:id/app_icon",
            className="android.widget.ImageView",
            instance=9).click()
        print('等待蚂蚁森林页面启动...')
        await async_sleep(15)

    async def _start_steal_energy(self) -> None:
        """
        开始偷能量
        :return:
        """
        ori_img_path = self.screen_save_path + 'screen.jpg'
        div_img_path = self.screen_save_path + 'div_img.jpg'
        # 待对比的hand路径
        ori_hand_img_path = 'ori_hand.jpg'
        hand_img_path = self.screen_save_path + 'hand.jpg'

        # 单页设置起始截止范围
        base_one_page_min_num = 0
        base_one_page_max_num = 80
        # 存储已被遍历的好友名
        traversed_friends_name_list = []
        while True:
            for index in range(base_one_page_min_num, base_one_page_max_num):
                try:
                    # div 块
                    div_ele = self.d(
                        className="android.view.View",
                        instance=index,
                        description='',)
                    child_count = div_ele.info.get('childCount', 0)
                except UiObjectNotFoundError:
                    # 处理index找不到元素带来的异常!
                    break

                if child_count < 6:
                    continue

                # 表示是最外层的div块
                # div_index: 8, 14, 20, 26, 33, 40, 47, 54, 61
                if index in (8, 14, 20):
                    # 排名前三的元素只有6个, friend_name索引需特殊设置
                    friend_name_ele_index = 1
                else:
                    friend_name_ele_index = 2

                try:
                    friends_name = div_ele.child(instance=friend_name_ele_index).info.get('contentDescription', '')
                    # print('friends_name: {}'.format(friends_name))
                except UiObjectNotFoundError:
                    # 处理index找不到元素带来的异常!
                    break

                if friends_name == '邀请':
                    # 退出
                    print('所有好友已遍历完成!')
                    break

                if friends_name in self.no_collect_friends_list \
                        or friends_name == ''\
                        or friends_name in traversed_friends_name_list \
                        or re.compile('\d+kg|获得了\d+个环保证书|\d+g').findall(friends_name) != []:
                    continue
                else:
                    pass

                div_ele_bounds = div_ele.info.get('bounds', {})
                self.d.screenshot(ori_img_path)
                # 指定位置截图
                specified_position_screenshot(
                    ori_img_path=ori_img_path,
                    target_img_save_path=div_img_path,
                    left=div_ele_bounds['left'],
                    top=div_ele_bounds['top'],
                    right=div_ele_bounds['right'],
                    bottom=div_ele_bounds['bottom'], )
                # 截图小手
                specified_position_screenshot(
                    ori_img_path=div_img_path,
                    target_img_save_path=hand_img_path,
                    left=self.hand_bounds['left'],
                    top=self.hand_bounds['top'],
                    right=self.hand_bounds['right'],
                    bottom=self.hand_bounds['bottom'], )
                img_similarity = img_similarity_calculate(
                    img_path1=ori_hand_img_path,
                    img_path2=hand_img_path,
                    mode=3, )
                if img_similarity >= self.hand_img_similarity\
                        or img_similarity in (0.703125,):
                    print('[+] {} 可收取! img_similarity: {}'.format(friends_name, img_similarity))
                    # 点击进入待收取的friend
                    div_ele.child(instance=friend_name_ele_index).click()
                    await async_sleep(5.)
                    await self._collect_energy()

                else:
                    print('[-] {} 不可收取! img_similarity: {}'.format(friends_name, img_similarity))

                if friends_name not in traversed_friends_name_list:
                    traversed_friends_name_list.append(friends_name)

            # 这样处理避免出现查看更多的刷新未完成!
            await u2_up_swipe_some_height(d=self.d, swipe_height=.2)
            await async_sleep(1.5)
            await u2_up_swipe_some_height(d=self.d, swipe_height=.5)
            await async_sleep(1.5)

    async def _collect_energy(self,) -> None:
        """
        收集能量并返回上页
        :return:
        """
        # 收取能量
        # descriptionMatches中为re
        power_ele_list = self.d(descriptionMatches='收集能量\d+克', className="android.widget.Button")
        power_ele_count = power_ele_list.count
        print('this friend had energy_num: {}个'.format(power_ele_count))
        # 原先使用下面无法遍历元素, 只能取到第一个, 第二个就报UiObjectNotFoundError
        # for power_ele in power_ele_list:
        # 改用下面的方式
        for index in range(power_ele_count):
            try:
                power_ele_list.__getitem__(index=index).click()
            except UiObjectNotFoundError as e:
                print(e)

        # 用于查看收取效果
        await async_sleep(2)
        await u2_page_back(d=self.d,)

        return None

    async def _batch_add_friends(self):
        """
        批量添加好友
        :return:
        """
        await self._enter_add_friends_page()
        await self._start_add_friends()

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
            phone_num = self.phone_list[get_random_int_number(0, len(self.phone_list) - 1)]

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
                    print('add_friend_btn 是否存在?: {}'.format(add_friend_btn.exists()))
                    if add_friend_btn.exists():
                        # 只对应单个支付宝账号
                        try:
                            add_friend_btn_text = add_friend_btn.info.get('text', '')
                            # print('add_friend_btn_text: {}'.format(add_friend_btn_text))
                            assert add_friend_btn_text != '发消息', '该账号已被添加!'
                        except AssertionError as e:
                            print(e)
                            index += 1
                            await u2_page_back(d=self.d, back_num=1)
                            continue

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

                        continue
                else:
                    pass

                if user_name_ele_first_exists:
                    user_name_ele_first.click()

                # 加好友页面处理
                # 加好友 btn
                self.d(resourceId="com.alipay.android.phone.wallet.profileapp:id/ll_menu2").click()
                await async_sleep(.5)
                if self.d(resourceId="android:id/message", text=u"今天已经发送太多好友申请了，明天再来吧。", className="android.widget.TextView")\
                        .exists():
                    raise AddFriendsToTheUpperLimitException

                # 朋友验证 发送btn
                self.d(resourceId="com.alipay.mobile.ui:id/title_bar_generic_button").click()
                # 返回加好友页面
                self.d(resourceId="com.alipay.mobile.antui:id/back_button").click()
                print('[+] 添加 {} success!'.format(phone_num))
                index += 1

            except AddFriendsToTheUpperLimitException:
                print('今日添加好友数已达到上限!')
                break

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
