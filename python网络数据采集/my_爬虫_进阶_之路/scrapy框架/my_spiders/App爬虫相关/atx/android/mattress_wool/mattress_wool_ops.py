# coding:utf-8

"""
@author = super_fazai
@File    : mattress_wool_ops.py
@connect : superonesfazai@gmail.com
"""

"""
羊毛ops

注: 仅供技术交流, 勿进行商业行为
"""

from settings import (
    DEVICE_ID_LIST,
    CHANGE_MACHINE_PKG_NAME,
    APP_NAME,
    AUTO_READ,
    AUTO_TRY_APP,
    AUTO_REGISTER,
    AUTO_GET_NOW_PKG_NAME,
    QT_INVITE_CODE,
    HT_INVITE_CODE,
    AUTO_LOOK_GOODS,
    BASE_READ_PRINT_STR,
    AUTO_PLAY_GAME,
    GAME_NAME,)
from wool_exceptions import (
    ReadTimeOutException,
    AppInstalledBeforeException,
    NoMoreArticlesException,)
from wool_utils import (
    device_id_in_red_rice_1s,
    device_id_in_oppo_r7s,
    sleep_random_time,)

from gc import collect
import uiautomator2 as u2
# d对象的基础类
from uiautomator2 import UIAutomatorServer
from uiautomator2.session import UiObject
# UI选择器的参数名可从此类中获取
from uiautomator2.session import Selector as U2Selector
from uiautomator2.exceptions import (
    UiObjectNotFoundError,
    UiAutomationNotConnectedError,)
from fzutils.ip_pools import tri_ip_pool
from fzutils.exceptions import AppNoResponseException
from fzutils.register_utils import YiMaSmser
from fzutils.spider.async_always import *
from fzutils.spider.app_utils import *
from fzutils.shell_utils import *

"""
* 输入法: 搜狗输入法
* kingroot: 因为r7s安装软件检测, 涉及其包的相关按钮的点击
* 金山电池医生: 运行前先使用金山电池医生关闭其他耗电服务, 可有效降低耗电量, 提高脚本稳定性!!
* 改机apk: 
    版本6.3.9, 加入包解析错误, 可安装6.3.6版
    *** 只有一个子账号, 每次使用前先手动绑定一次(切记: 先去重置下设备id, 再进行绑定)(避免自动绑定过于频繁, 被禁止一定时长[6-9分钟...]) 
* 红米1s:
    xposed安装版本: xposedinstallermiui8.apk (android 4.4)
    红米1s(电信联通版) 卡刷9.7开发者版本(下载地址: http://bigota.d.miui.com/7.11.16/miui_HM1SWC_7.11.16_2787e0f1ed_4.4.zip)
    $ adb -s de295374 push miui_HM1SWC_7.11.16_2787e0f1ed_4.4.zip /sdcard/
    # 关于本机 -> 系统更新 -> 右上角按钮 -> 手动选择安装包 -> miui_HM1SWC_7.11.16_2787e0f1ed_4.4.zip -> 确定进行自动安装 -> 安装好后 -> 设置 -> 权限管理 -> root -> 开启root
* oppo r7s:
    xposed安装版本: xposedinstallermiui8.apk (android 4.4)
    kingroot
"""

class MattressWoolOps(AsyncCrawler):
    """羊毛ops"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        self.short_name = 'qt' if APP_NAME is None else APP_NAME
        self.auto_read = True if AUTO_READ == 1 else False                              # 模式是否为自动阅读
        self.auto_try_app = True if AUTO_TRY_APP == 1 else False                        # 模式是否为自动试玩
        self.auto_register = True if AUTO_REGISTER == 1 else False                      # 模式是否为自动注册
        self.auto_get_now_pkg_name = True if AUTO_GET_NOW_PKG_NAME == 1 else False      # 模式为自动获取当前app pkg_name
        self.auto_look_goods = True if AUTO_LOOK_GOODS == 1 else False                  # 模式是否为自动逛商品
        self.auto_play_game = True if AUTO_PLAY_GAME == 1 else False                    # 模式是否为自动玩游戏
        self.game_name = '' if GAME_NAME is None else GAME_NAME
        self.wool_app_info = self._init_wool_app_info()                                 # 羊毛app信息
        self.pkg_name = self._get_wool_pkg_name()
        self.clear_app_base_num = 15                                                    # 清理app的基数
        self.try_app_sleep_time = 3.15 * 60
        self.d_debug = False
        self.set_fast_input_ime = True
        self.device_id_list = DEVICE_ID_LIST
        self.ht_invite_code = HT_INVITE_CODE
        self.qt_invite_code = QT_INVITE_CODE
        self.base_read_print_str = BASE_READ_PRINT_STR
        self.change_machine_pkg_name = CHANGE_MACHINE_PKG_NAME
        self._init_yima_obj_info()
        self.qt_installed_app_name_list = self._get_qt_installed_app_name_list()

    def _init_yima_obj_info(self):
        """
        获取yima obj
        :return:
        """
        with open('/Users/afa/myFiles/pwd/yima_pwd.json', 'r') as f:
            yima_info = json_2_dict(f.read())
        # self.yima_smser_obj = YiMaSmser(username=yima_info['username'], pwd=yima_info['pwd'])
        self.ym_username, self.ym_pwd = yima_info['username'], yima_info['pwd']

        if self.short_name == 'qt':
            self.ym_project_id = 2674

        elif self.short_name == 'ht':
            self.ym_project_id = 8080

        else:
            self.ym_project_id = -1

    def _get_wool_pkg_name(self):
        """
        获取包名
        :return:
        """
        for item in self.wool_app_info:
            if item.get('short_name', '') == self.short_name:
                return item.get('pkg_name', '')

        raise NotImplemented

    @staticmethod
    def _init_wool_app_info():
        """
        初始化羊毛app信息
        :return:
        """
        return [
            {
                'short_name': 'qt',
                'pkg_name': 'com.jifen.qukan',
            },
            {
                'short_name': 'ht',
                'pkg_name': 'com.cashtoutiao',
            },
            {
                'short_name': 'sd',
                'pkg_name': 'c.l.a',
            },
        ]

    async def _fck_run(self):
        pkg_name = self.pkg_name
        if self.auto_get_now_pkg_name:
            # 设置空, 不启动任何app
            pkg_name = ''
        elif self.auto_register:
            if self.short_name == 'ht':
                pkg_name = self.change_machine_pkg_name

            elif self.short_name == 'qt':
                pkg_name = self.change_machine_pkg_name

        self.device_obj_list = await get_u2_init_device_list(
            loop=self.loop,
            u2=u2,
            pkg_name=pkg_name,
            device_id_list=self.device_id_list,
            d_debug=self.d_debug,
            set_fast_input_ime=self.set_fast_input_ime,)

        if self.auto_get_now_pkg_name:
            # 自动化当前包名
            for device_obj in self.device_obj_list:
                d: UIAutomatorServer = device_obj.d
                msg = '当前pkg_name: {}'.format(d.current_app().get('package', ''))
                print(self._get_print_base_str(device_obj=device_obj) + msg)

        if self.auto_read:
            # auto read
            await self._every_device_start_someone_actions(actions_name='read')

        if self.auto_try_app:
            # auto try apps
            await self._every_device_start_someone_actions(actions_name='try_apps')

        if self.auto_register:
            # auto register 和继续后方相关操作
            await self._every_device_start_someone_actions(actions_name='register')

        if self.auto_look_goods:
            # auto look goods
            await self._every_device_start_someone_actions(actions_name='look_goods')

        if self.auto_play_game:
            await self._every_device_start_someone_actions(actions_name='play_game')

    async def _every_device_start_someone_actions(self, actions_name):
        """
        每台设备开始某行为链
        :param actions_name: 行为名
        :return:
        """
        async def get_func_name():
            """
            获取func_name
            :return:
            """
            nonlocal actions_name

            if actions_name == 'read':
                m_func_name = self._read_forever

            elif actions_name == 'try_apps':
                m_func_name = self._auto_try_apps

            elif actions_name == 'register':
                m_func_name = self._auto_register_and_other_actions

            elif actions_name == 'look_goods':
                m_func_name = self._auto_look_goods

            elif actions_name == 'play_game':
                m_func_name = self._auto_play_game

            else:
                raise ValueError('actions_name value 异常!')

            return m_func_name

        tasks = []
        func_name = await get_func_name()

        for device_obj in self.device_obj_list:
            try:
                print('create task[where device_id: {}]...'.format(device_obj.device_id))
            except AttributeError as e:
                # 处理设备无法连接的, 导致的错误: AttributeError: 'NoneType' object has no attribute 'device_id'
                print(e)
                continue

            func_args = [
                device_obj,
            ]
            tasks.append(self.loop.create_task(unblock_func(
                func_name=func_name,
                func_args=func_args,
                default_res=None,)))

        all_res = await async_wait_tasks_finished(tasks=tasks)

        return all_res

    def _auto_play_game(self, device_obj):
        """
        auto play game
        :param device_obj:
        :return:
        """
        msg = '即将开始auto play game ...'
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        if self.short_name == 'sd':
            self._sd_auto_play_game(device_obj=device_obj)

        else:
            raise NotImplemented

    def _sd_auto_play_game(self, device_obj):
        """
        sd play game
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        # 点击进入逛逛领币
        msg = '正在进入选择比赛游戏界面 ...'
        print(self._get_print_base_str(device_obj=device_obj) + msg)

        d(resourceId="c.l.a:id/text", text=u"小游戏赚钱", className="android.widget.TextView").click()
        while not d(resourceId="c.l.a:id/title", text=u"推荐游戏", className="android.widget.TextView")\
            .exists():
            pass
        u2_block_up_swipe_some_height(d=d, swipe_height=.3)
        d(resourceId="c.l.a:id/tv_game_name", text=u"守护飞飞", className="android.widget.TextView").click()
        d(resourceId="c.l.a:id/title_1", text=u"新手房", className="android.widget.TextView").click()

        while True:
            d(text=u"准备开始", className="android.widget.TextView", instance=1).click()
            start_btn = d(resourceId="c.l.a:id/iv_start_game", text=u"开始游戏", className="android.widget.TextView")
            while not start_btn.exists():
                pass
            start_btn.click()

            msg = '正在进入游戏页面中 ...'
            print(self._get_print_base_str(device_obj=device_obj) + msg)
            while not d(resourceId="c.l.a:id/iv_back", className="android.widget.ImageView").exists():
                # 游戏进入界面
                pass

            # 点击开始游戏按钮
            d.click(0.488, 0.687)
            sleep(5.)
            # 把滑块上升至一定高度
            d.drag(0.502, 0.636, 0.491, 0.636, 0.5)
            # 中心位置x, y
            center_x = .497
            center_y = .452
            try:
                while True:
                    # 在中心位置先左滑
                    d.drag(center_x, center_y, 0.398, center_y, 0.0)
                    # 再滑回中心位置
                    d.drag(0.398, center_y, center_x, center_y, 0.0)
                    # 再右滑
                    d.drag(center_x, center_y, 0.596, center_y, 0.0)
                    # 再滑回中心位置
                    d.drag(0.596, center_y, center_x, center_y, 0.0)
            except KeyboardInterrupt as e:
                print(self._get_print_base_str(device_obj=device_obj), e)
                while True:
                    aa = input('请输入是否点击完成(y)').replace('\n', '')
                    if aa == 'y':
                        break

    def _auto_look_goods(self, device_obj):
        """
        auto 逛商品
        :param device_obj:
        :return:
        """
        msg = '即将开始auto 逛商品...'
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        if self.short_name == 'sd':
            self._sd_auto_look_goods(device_obj=device_obj)

        else:
            raise NotImplemented

    def _sd_auto_look_goods(self, device_obj):
        """
        sd auto look goods
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        # 点击进入逛逛领币
        msg = '正在进入逛逛领币 ...'
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        d(resourceId="c.l.a:id/tab_text", text=u"逛逛领币", className="android.widget.TextView").click()
        while not d(text=u"逛一逛即得闪电币奖励", className="android.widget.TextView").exists():
            pass
        article_count = 0
        read_goods_title_list = []
        while True:
            try:
                # 首页恶意弹窗处理(逛商品page也走这个统一处理)
                self._ht_home_window_handle(device_obj=device_obj)
            except (AppNoResponseException, NoMoreArticlesException):
                break

            try:
                first_article_ele = d(
                    resourceId="c.l.a:id/title",
                    className="android.widget.TextView",
                    instance=0,)
                article_title = first_article_ele.info.get('text', '')
                assert article_title not in read_goods_title_list, \
                    'article_title in read_goods_title_list, so pass!'
                first_article_ele.click()

                # 阅读goods info(直接采用读文章的模型)
                self._sd_read_one_article(
                    device_obj=device_obj,
                    article_title=article_title,
                    article_count=article_count, )
                article_count += 1
                if article_title not in read_goods_title_list:
                    read_goods_title_list.append(article_title)

            except (UiObjectNotFoundError, AssertionError, Exception) as e:
                print(self._get_print_base_str(device_obj=device_obj), e)
                u2_block_up_swipe_some_height(d=d, swipe_height=.35,)
                sleep_random_time(1., 1.5)
                continue

            u2_block_up_swipe_some_height(d=d, swipe_height=.3)
            # 避免下滑过于频繁
            sleep_random_time(1., 1.5)

        self._restart_app_and_continue_actions(
            device_obj=device_obj,
            actions_name='look_goods')

    def _auto_register_and_other_actions(self, device_obj):
        """
        自动注册并完成后续行为
        :return:
        """
        msg = '即将开始auto 注册账号并绑定手机添加邀请码...'
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        if self.short_name == 'ht':
            self._ht_auto_register_and_other_actions(device_obj=device_obj)

        elif self.short_name == 'qt':
            self._qt_auto_register_and_other_actions(device_obj=device_obj)

        else:
            raise NotImplemented

    def _qt_auto_register_and_other_actions(self, device_obj):
        """
        qt 自动注册并完成后续行为
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        while True:
            # 重置设备id, 通过改机app启动设备
            self._init_device_id_info(
                device_obj=device_obj,
                target_app_index=1,)
            # 下面是测试时使用, 避免总是频繁改变设备id(前提已更改一次设备id)
            # d.app_stop(pkg_name=self.pkg_name)
            # d.app_start(pkg_name=self.pkg_name)

            tmp_btn: UiObject = u2_get_ui_obj(
                d=d,
                resourceId='com.jifen.qukan:id/a2c',
                text='先去逛逛',
                className='android.widget.TextView',)
            while not tmp_btn.exists():
                if d(resourceId="com.jifen.qukan:id/fr", text=u"版本升级", className="android.widget.TextView").exists():
                    d(resourceId="com.jifen.qukan:id/ux", text=u"以后更新", className="android.widget.TextView").click()
                pass
            tmp_btn.click()

            mine_btn: UiObject = u2_get_ui_obj(
                d=d,
                text='我的',
                resourceId='com.jifen.qukan:id/jl',
                className='android.widget.Button', )
            # 开始目标app相关操作
            while True:
                try:
                    self._qt_home_window_handle(device_obj=device_obj)
                    mine_btn.click()
                    break
                except Exception as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    continue

            input_num_label: UiObject = u2_get_ui_obj(
                d=d,
                resourceId='com.jifen.qukan:id/wu',
                text='请输入手机号码',
                className='android.widget.TextView',)
            while not input_num_label.exists():
                pass

            while True:
                try:
                    self.yima_smser_obj = YiMaSmser(username=self.ym_username, pwd=self.ym_pwd)
                    # phone_num = '13451463505'
                    # phone_num = '18698570079'
                    phone_num = self.yima_smser_obj._get_phone_num(project_id=self.ym_project_id)
                    assert phone_num != '', 'phone_num != ""'
                    msg = '新获取到phone_num: {}'.format(phone_num)
                    print(self._get_print_base_str(device_obj=device_obj) + msg)
                except AssertionError as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    sleep(8.)
                    continue

                try:
                    phone_input_ele: UiObject = u2_get_ui_obj(
                        d=d,
                        resourceId='com.jifen.qukan:id/aeo',
                        text='请输入11位手机号码',
                        className='android.widget.EditText',)
                    phone_input_ele.clear_text()
                    phone_input_ele.set_text(text=phone_num)
                    sleep(2.)

                    u2_get_ui_obj(
                        d=d,
                        resourceId='com.jifen.qukan:id/ia',
                        text='获取短信验证码',
                        className='android.widget.Button',).click()

                    # sms_res = '1813'
                    # sms_res = input('请输入手机验证码: ').replace('\n', '')
                    sms_res = self.yima_smser_obj._get_sms(phone_num=phone_num, project_id=self.ym_project_id)
                    print(self._get_print_base_str(device_obj=device_obj) + 'sms_res: {}'.format(sms_res))
                    try:
                        sms_res = re.compile('(\d+)').findall(sms_res)[0]
                        assert sms_res != '', 'sms_res !=""'
                        assert len(sms_res) == 4, 'sms_res长度异常!'
                    except (AssertionError, IndexError) as e:
                        print(self._get_print_base_str(device_obj=device_obj), e)
                        u2_block_page_back(d=d)
                        continue

                    # 输入手机验证码
                    self._qt_input_phone_verification_code(
                        device_obj=device_obj,
                        sms_res=sms_res,)

                    tmp_btn: UiObject = u2_get_ui_obj(
                        d=d,
                        text='点击领钱',
                        className='android.widget.TextView',)
                    while not mine_btn.exists():
                        if tmp_btn.exists():
                            tmp_btn.click()
                        pass
                    mine_btn.click()
                    sleep(2.)
                    # TODO 弹窗(这个弹窗无法被定位, 手动进行点击)
                    tmp_btn: UiObject = u2_get_ui_obj(
                        d=d,
                        resourceId='com.jifen.qukan:id/a09',
                        className='android.widget.ImageView',)
                    if tmp_btn.exists():
                        tmp_btn.click()

                    u2_get_ui_obj(
                        d=d,
                        resourceId='com.jifen.qukan:id/ai8',
                        className='android.widget.TextView',
                        text='输入邀请码',).click()
                    tmp_btn: UiObject = u2_get_ui_obj(
                        d=d,
                        description='领取红包',
                        className='android.view.View',)
                    while not tmp_btn.exists():
                        pass

                    input_ele: UiObject = u2_get_ui_obj(
                        d=d,
                        className='android.widget.EditText',)
                    input_ele.set_text(text=self.qt_invite_code)
                    u2_get_ui_obj(d=d, className='android.view.View', description='拆红包得5000金币').click()
                    u2_block_page_back(d=d, back_num=1)

                    # ...
                    u2_get_ui_obj(
                        d=d,
                        resourceId='com.jifen.qukan:id/jf',
                        text='头条',
                        className='android.widget.Button',).click()
                    try:
                        self._read_someone_time_duration(device_obj=device_obj)
                    except (TimeoutError, Exception) as e:
                        print(self._get_print_base_str(device_obj=device_obj), e)
                        # 结束进程
                        d.app_stop(pkg_name=self.pkg_name)

                        break

                except Exception as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    raise e

            print(self._get_print_base_str(device_obj=device_obj) + '注册phone_num: {} success!'.format(phone_num))

    def _qt_input_phone_verification_code(self, device_obj, sms_res: str):
        """
        qt 输入手机验证码
        :param device_obj:
        :param sms_res:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + '正在输入手机验证码 ...')
        # 输入4位验证码
        # 先输入某数字, 使底部弹出输入法切换框
        first_phone_code_input_ele: UiObject = u2_get_ui_obj(
            d=d,
            resourceId='com.jifen.qukan:id/wx',
            className='android.widget.EditText',)
        first_phone_code_input_ele.set_text('0')
        print(self._get_print_base_str(device_obj=device_obj) + '正在切换至搜狗输入法 ...')
        # 再切换至搜狗输入法
        if device_id_in_red_rice_1s(device_id=device_obj.device_id):
            # 点击切换输入法
            d.click(0.863, 0.963)
            sleep(2.)
            d(resourceId="android:id/text1", text=u"搜狗输入法", className="android.widget.CheckedTextView").click()

        elif device_id_in_oppo_r7s(device_id=device_obj.device_id):
            d.click(0.896, 0.902)
            sleep(2.)
            d(resourceId="android:id/radio", className="android.widget.RadioButton", instance=1).click()

        else:
            raise ValueError('device_id value 异常!')

        # 点到第一个输入框进行后续输入(双击)
        first_phone_code_input_ele.click()
        first_phone_code_input_ele.click()
        first_phone_code_input_ele.clear_text()
        # 等待键盘显示
        print(self._get_print_base_str(device_obj=device_obj) + '等待搜狗键盘显示 ...')

        if device_id_in_red_rice_1s(device_id=device_obj.device_id):
            sleep(12.)
        elif device_id_in_oppo_r7s(device_id=device_obj.device_id):
            sleep(5.)
        else:
            raise ValueError('device_id value 异常!')

        for index, item in enumerate(sms_res):
            # TODO 测试发现无法输入最后数字
            # d(resourceId="com.cashtoutiao:id/et_code{}".format(index+1), className="android.widget.EditText")\
            #     .send_keys(text=item)

            # 改用搜狗数字键盘模拟点击
            x, y = self._sg_num_keyword(num=int(item), device_id=device_obj.device_id)
            d.click(x, y)

        print(self._get_print_base_str(device_obj=device_obj) + '验证码输入完成!')

        return

    def _ht_auto_register_and_other_actions(self, device_obj):
        """
        ht 自动注册并完成后续行为
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        while True:
            # 重置设备id, 通过改机app启动设备
            self._init_device_id_info(
                device_obj=device_obj,
                target_app_index=0,)
            # 下面是测试时使用, 避免总是频繁改变设备id(前提已更改一次设备id)
            # d.app_stop(pkg_name=self.pkg_name)
            # d.app_start(pkg_name=self.pkg_name)

            while not d(text=u"恭喜您获得", className="android.widget.TextView").exists():
                # if d(text=u"是否上传此错误报告，以帮助我们分析问题？报告可能包含您的个⼈信息，但我们会做好保密并仅⽤作问题分析。查看⽇志摘要", className="android.widget.TextView").exists():
                if d(resourceId="miui:id/alertTitle", textMatches=u"很抱歉，\“.*?\”已停止运行。", className="android.widget.TextView").exists():
                    print(self._get_print_base_str(device_obj=device_obj) + '目标程序启动异常! 即将开始new envir ...')
                    # 程序启动异常
                    d(resourceId="android:id/button2", text=u"取消", className="android.widget.Button").click()
                    return self._ht_auto_register_and_other_actions(device_obj=device_obj)

                else:
                    pass

                pass
            # 关闭每次新开沙盒app的弹窗
            d(resourceId="com.cashtoutiao:id/iv_close", className="android.widget.ImageView").click()

            # 开始目标app相关操作
            while True:
                try:
                    self._ht_home_window_handle(device_obj=device_obj)
                    d(text=u"我的", className="android.widget.TextView").click()
                    break
                except Exception as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    continue

            unbound_phone_num_btn = d(
                resourceId="com.cashtoutiao:id/text_number",
                text=u"未绑定手机",
                className="android.widget.TextView")
            while not unbound_phone_num_btn.exists():
                pass
            unbound_phone_num_btn.click()

            # 开始绑定手机号
            d(resourceId="com.cashtoutiao:id/account_phone_layout", className="android.widget.RelativeLayout")\
                .child_by_text(txt='手机号').click()

            while True:
                try:
                    self.yima_smser_obj = YiMaSmser(username=self.ym_username, pwd=self.ym_pwd)
                    # phone_num = '13451463505'
                    phone_num = self.yima_smser_obj._get_phone_num(project_id=self.ym_project_id)
                    assert phone_num != '', 'phone_num != ""'
                    print(self._get_print_base_str(device_obj=device_obj) + '新获取到phone_num: {}'.format(phone_num))
                except AssertionError as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    sleep(8.)
                    continue

                try:
                    phone_input_ele = d(resourceId="com.cashtoutiao:id/et_phone", className="android.widget.EditText")
                    phone_input_ele.clear_text()
                    phone_input_ele.set_text(text=phone_num)
                    sleep(2.)

                    if d(
                            resourceId="com.cashtoutiao:id/tv_change_phone", 
                            text=u"验证码绑定", 
                            className="android.widget.TextView").exists():
                        d(
                            resourceId="com.cashtoutiao:id/tv_change_phone", 
                            text=u"验证码绑定", 
                            className="android.widget.TextView").click()
                        sleep(1.5)

                    d(
                        resourceId="com.cashtoutiao:id/login_button", 
                        text=u"获取短信验证码", 
                        className="android.widget.TextView").click()

                    # sms_res = '181338'
                    sms_res = self.yima_smser_obj._get_sms(phone_num=phone_num, project_id=self.ym_project_id)
                    print(self._get_print_base_str(device_obj=device_obj) + 'sms_res: {}'.format(sms_res))
                    try:
                        sms_res = re.compile('(\d+)').findall(sms_res)[0]
                        assert sms_res != '', 'sms_res !=""'
                        assert len(sms_res) == 6, 'sms_res长度异常!'
                    except (AssertionError, IndexError) as e:
                        print(self._get_print_base_str(device_obj=device_obj), e)
                        u2_block_page_back(d=d)
                        continue

                    # 输入手机验证码
                    self._ht_input_phone_verification_code(
                        device_obj=device_obj,
                        sms_res=sms_res,)

                    while not d(resourceId="com.cashtoutiao:id/tv_skip", text=u"跳过 >", className="android.widget.TextView").exists():
                        pass
                    d(resourceId="com.cashtoutiao:id/tv_skip", text=u"跳过 >", className="android.widget.TextView").click()
                    sleep(3.)
                    u2_block_page_back(d=d)
                    sleep(2.)
                    u2_block_up_swipe_some_height(d=d, swipe_height=.5)
                    sleep(3.)

                    # 输入邀请码
                    d(resourceId="com.cashtoutiao:id/tv_invite_title", text=u"输入邀请码", className="android.widget.TextView").click()
                    d(resourceId="com.cashtoutiao:id/et_input", text=u"请输入邀请码", className="android.widget.EditText").set_text(text=self.ht_invite_code)
                    d(resourceId="com.cashtoutiao:id/view_get", className="android.view.View").click()
                    sleep(2.)
                    d(resourceId="com.cashtoutiao:id/tv_confirm", text=u"确认领取", className="android.widget.TextView").click()
                    print(self._get_print_base_str(device_obj=device_obj) + '输入邀请码成功!')

                    # 进行签到
                    d(text=u"任务中心", className="android.widget.TextView").click()
                    d(resourceId="com.cashtoutiao:id/sign_btn_container", className="android.widget.RelativeLayout").click()
                    # 弹窗忽略
                    d(resourceId="com.cashtoutiao:id/tv_left", text=u"忽略", className="android.widget.TextView").click()

                    # TODO 自动阅读特定时长(此处超时后, self._read_forever函数还在继续执行未退出!!)
                    d(text=u"头条", className="android.widget.TextView").click()
                    try:
                        self._read_someone_time_duration(device_obj=device_obj)
                    except (TimeoutError, Exception) as e:
                        print(self._get_print_base_str(device_obj=device_obj), e)
                        # 结束进程
                        d.app_stop(pkg_name=self.pkg_name)

                        break

                except UiAutomationNotConnectedError as e:
                    # TODO 无连接则直接抛出异常, 终止后续所有操作!!
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    raise UiAutomationNotConnectedError

                except Exception as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    # test
                    raise e

            print(self._get_print_base_str(device_obj=device_obj) + '注册phone_num: {} success!'.format(phone_num))

    def _ht_input_phone_verification_code(self, device_obj, sms_res: str) -> None:
        """
        ht 输入手机验证码
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + '正在输入手机验证码 ...')
        # 输入6位验证码
        # 先输入某数字, 使底部弹出输入法切换框
        d(resourceId="com.cashtoutiao:id/et_code1", className="android.widget.EditText").set_text('0')
        # 再切换至搜狗输入法
        if device_id_in_red_rice_1s(device_id=device_obj.device_id):
            # 点击切换输入法
            d.click(0.863, 0.963)
            sleep(2.)
            d(resourceId="android:id/text1", text=u"搜狗输入法", className="android.widget.CheckedTextView").click()

        elif device_id_in_oppo_r7s(device_id=device_obj.device_id):
            d.click(0.896, 0.902)
            sleep(2.)
            d(resourceId="android:id/radio", className="android.widget.RadioButton", instance=1).click()

        else:
            raise ValueError('device_id value 异常!')

        # 点到第一个输入框进行后续输入(双击)
        d(resourceId="com.cashtoutiao:id/et_code1", className="android.widget.EditText").click()
        d(resourceId="com.cashtoutiao:id/et_code1", className="android.widget.EditText").click()
        d(resourceId="com.cashtoutiao:id/et_code1", className="android.widget.EditText").clear_text()
        # 等待键盘显示
        print(self._get_print_base_str(device_obj=device_obj) + '等待搜狗键盘显示 ...')

        if device_id_in_red_rice_1s(device_id=device_obj.device_id):
            sleep(12.)
        elif device_id_in_oppo_r7s(device_id=device_obj.device_id):
            sleep(5.)
        else:
            raise ValueError('device_id value 异常!')

        for index, item in enumerate(sms_res):
            # TODO 测试发现无法输入最后数字
            # d(resourceId="com.cashtoutiao:id/et_code{}".format(index+1), className="android.widget.EditText")\
            #     .send_keys(text=item)

            # 改用搜狗数字键盘模拟点击
            x, y = self._sg_num_keyword(num=int(item), device_id=device_obj.device_id)
            d.click(x, y)

        print(self._get_print_base_str(device_obj=device_obj) + '验证码输入完成!')

        return

    def _init_device_id_info(self, device_obj, target_app_index=0):
        """
        通过改机app重置设备id
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        # * 测试发现无需重置id, 新建envir, 就已在环境中重置设备id
        # print(self._get_print_base_str(device_obj=device_obj) + '正在重置 device_id ...')
        # # 先重置设备id
        # d(resourceId="zpp.wjy.xxsq:id/setting", className="android.widget.ImageView").click()
        # human_swipe(d=d, slide_distance=.6)
        # d(resourceId="zpp.wjy.xxsq:id/tv_title", text=u"重置设备id", className="android.widget.TextView").click()
        # print(self._get_print_base_str(device_obj=device_obj) + '重置设备id成功!')

        # # 重启改机app, 并新建环境打开目标app
        # # 必须先终止改机进程, 再重启
        d.app_stop(pkg_name=self.change_machine_pkg_name)
        print(self._get_print_base_str(device_obj=device_obj) + 'restarting 改机app ...')
        d.app_start(pkg_name=self.change_machine_pkg_name)

        print(self._get_print_base_str(device_obj=device_obj) + '正在new envir ...')
        new_envir_btn = d(resourceId="zpp.wjy.xxsq:id/tv_new", text=u"新建环境", className="android.widget.TextView")
        while not new_envir_btn.exists():
            pass
        new_envir_btn.click()
        sleep(5.)
        # 去绑定子账号
        if d(resourceId="android:id/message",
             text=u"未绑定子账号,请到账号管理任选一个子账号点击'绑定本机'",
             className="android.widget.TextView").exists():
            d(resourceId="android:id/button1", text=u"去账号管理", className="android.widget.Button").click()
            bind_this_machine_btn = d(description=u"绑定本机", className="android.view.View")
            while not bind_this_machine_btn.exists():
                pass
            bind_this_machine_btn.click()
            sleep(3.)

            u2_block_page_back(d=d, back_num=1)
            sleep(1.5)
        else:
            pass

        # * 新建符合目标软件正常运行的环境
        while True:
            while not new_envir_btn.exists():
                pass
            new_envir_btn.click()
            while d(resourceId="zpp.wjy.xxsq:id/tv_title", text=u"自动保存应用数据", className="android.widget.TextView").exists():
                # 表示在新建环境
                pass

            phone_info_ele = d(resourceId="zpp.wjy.xxsq:id/tv_info", className="android.widget.TextView")
            while not phone_info_ele.exists():
                pass
            phone_info = phone_info_ele.info.get('text', '')
            phone_model = ''
            try:
                phone_model = re.compile('手机: (.*?)\\n运营商').findall(phone_info)[0]
            except IndexError:
                pass
            if d(resourceId="zpp.wjy.xxsq:id/textView5", text=u"警告", className="android.widget.TextView").exists():
                print(self._get_print_base_str(device_obj=device_obj) + '[-] model: {}, 分辨率异常, 跳过!'.format(phone_model))
            else:
                print(self._get_print_base_str(device_obj=device_obj) + '[+] model: {}, 分辨率正常!! 退出新建环境!'.format(phone_model))
                break

        toast_msg = d.toast.get_message(wait_timeout=10., default='')
        print(self._get_print_base_str(device_obj=device_obj) + 'toast_msg: {}'.format(toast_msg))
        print(self._get_print_base_str(device_obj=device_obj) + '重置device_id success!!')

        # 随机模拟定位
        print(self._get_print_base_str(device_obj=device_obj) + '随机模拟定位ing ...')
        d(resourceId="zpp.wjy.xxsq:id/text", text=u"虚拟定位", className="android.widget.TextView").click()
        d(resourceId="zpp.wjy.xxsq:id/btn", text=u"[快捷] 随机模拟定位", className="android.widget.Button").click()
        toast_msg = d.toast.get_message(wait_timeout=10., default='')
        print(self._get_print_base_str(device_obj=device_obj) + 'toast_msg: {}'.format(toast_msg))

        # 启动目标app
        self._start_up_target_app_from_change_machine_app(
            device_obj=device_obj,
            target_app_index=target_app_index,)

        return

    def _start_up_target_app_from_change_machine_app(self, device_obj, target_app_index=0) -> None:
        """
        从改机app中启动目标app
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d
        device_id = device_obj.device_id

        # 从改机app启动目标app
        print(self._get_print_base_str(device_obj=device_obj) + '正在从改机app 内部启动目标程序 ...')
        d(resourceId="zpp.wjy.xxsq:id/iv_icon", className="android.widget.ImageView", instance=target_app_index).click()
        d(resourceId="zpp.wjy.xxsq:id/title", text=u"启动", className="android.widget.TextView").click()
        print(self._get_print_base_str(device_obj=device_obj) + '内部启动按钮已点击!')

        # TODO device_id: de295374执行完上面步骤后, 可能需要手动点击目标app, 此处设置为自动启动, 存在兼容问题!!
        if 'de295374' == device_id:
            d.app_start(pkg_name=self.pkg_name)
        else:
            pass

        return

    def _sg_num_keyword(self, num:int, device_id: str) -> tuple:
        """
        搜狗数字键盘对应点击
        :param device_id:
        :param num:
        :return:
        """
        hm_1s_num_keyword = {
            1: (0.279, 0.686),
            2: (0.501, 0.681),
            3: (0.723, 0.681),
            4: (0.276, 0.773),
            5: (0.496, 0.773),
            6: (0.718, 0.776),
            7: (0.273, 0.866),
            8: (0.501, 0.863),
            9: (0.718, 0.863),
            0: (0.498, 0.95),
        }
        oppo_r7s_num_keyword = {
            1: (0.268, 0.6),
            2: (0.493, 0.598),
            3: (0.692, 0.595),
            4: (0.255, 0.688),
            5: (0.459, 0.688),
            6: (0.666, 0.687),
            7: (0.255, 0.767),
            8: (0.496, 0.768),
            9: (0.697, 0.77),
            0: (0.498, 0.872),
        }
        if device_id_in_red_rice_1s(device_id=device_id):
            num_keyword = hm_1s_num_keyword

        elif device_id_in_oppo_r7s(device_id=device_id):
            num_keyword = oppo_r7s_num_keyword

        else:
            raise ValueError('device_id 异常, 请检查!')

        for key, value in num_keyword.items():
            if num == key:
                return value

    def _auto_try_apps(self, device_obj):
        """
        自动试玩app
        :return:
        """
        if self.short_name == 'qt':
            self._qt_auto_try_apps(device_obj=device_obj)

        else:
            raise NotImplemented

    def _qt_auto_try_apps(self, device_obj):
        """
        qt auto try apps
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + '即将开始auto试玩app...')
        # 先处理恶意弹窗
        self._qt_home_window_handle(device_obj=device_obj)
        d(resourceId="com.jifen.qukan:id/jj", text=u"任务", className="android.widget.Button").click()
        d(text=u"试玩领金币", className="android.widget.TextView").click()
        sleep(3.)

        while True:
            try:
                # 点击金币按钮进行安装
                # d(text=u"+864  ★", className="android.widget.TextView")
                first_ele = d(textMatches=u"\+\d+  ★", className="android.widget.TextView", instance=0)
                first_ele_text = first_ele.info.get('text', '')
                print(self._get_print_base_str(device_obj=device_obj) + '安装按钮text: {}'.format(first_ele_text))
                first_ele.click()
                try_app_btn = d(
                    textMatches=u"打开注册并试玩|打开激活|打开试玩|打开浏览|打开使用|打开阅读|打开注册",
                    className="android.widget.TextView")

                if not try_app_btn.exists():
                    # 先前 该app未安装的情况
                    d(text=u"立即下载", className="android.widget.TextView").click()
                    print(self._get_print_base_str(device_obj=device_obj) + 'starting download ...')

                    if device_id_in_red_rice_1s(device_id=device_obj.device_id):
                        # 红米1s
                        while not d(
                                resourceId="com.miui.packageinstaller:id/ok_button",
                                text=u"安装",
                                className="android.widget.Button")\
                                .exists():
                            pass
                        d(resourceId="com.miui.packageinstaller:id/ok_button",
                          text=u"安装",
                          className="android.widget.Button")\
                            .click()

                        complete_installed_btn = d(
                            resourceId="com.miui.packageinstaller:id/done_button",
                            text=u"完成",
                            className="android.widget.Button")
                        while not complete_installed_btn.exists():
                            pass
                        complete_installed_btn.click()

                    elif device_id_in_oppo_r7s(device_id=device_obj.device_id):
                        # oppo r7s
                        ok_install_btn = d(
                            resourceId="com.kingroot.kinguser:id/btn_install",
                            text=u"确认安装",
                            className="android.widget.Button")
                        while not ok_install_btn.exists():
                            pass
                        ok_install_btn.click()

                        complete_installed_btn = d(
                            resourceId="com.kingroot.kinguser:id/btn_right",
                            text=u"完成",
                            className="android.widget.Button")
                        while not complete_installed_btn.exists():
                            pass

                        # r7s完成按钮点击无响应的, 因此进行点击页面回退按钮
                        # complete_installed_btn.click()
                        d(resourceId="com.kingroot.kinguser:id/left_iv", className="android.widget.ImageView").click()

                    else:
                        # 魅族
                        while not d(
                                resourceId="com.android.packageinstaller:id/virus_scan_done",
                                text=u"确定要继续安装吗？",
                                className="android.widget.TextView").exists():
                            pass

                        d(
                            resourceId="com.android.packageinstaller:id/action_positive",
                            text=u"继续",
                            description=u"继续",
                            className="android.widget.TextView", ).click()

                        complete_installed_btn = d(
                            resourceId="com.android.packageinstaller:id/action_negative",
                            text=u"完成",
                            description=u"完成",
                            className="android.widget.TextView")
                        while not complete_installed_btn.exists():
                            pass

                        complete_installed_btn.click()

                    print(self._get_print_base_str(device_obj=device_obj) + 'installed!')
                else:
                    # app 已安装的情况
                    print(self._get_print_base_str(device_obj=device_obj) + '该app已安装, 可直接进入试玩!')

                # 开始试玩
                try_app_btn.click()
                if device_id_in_red_rice_1s(device_id=device_obj.device_id):
                    while not d(resourceId="android:id/button1", text=u"允许", className="android.widget.Button").exists():
                        pass
                    d(resourceId="android:id/button1", textMatches=u"允许", className="android.widget.Button").click()

                print(self._get_print_base_str(device_obj=device_obj) + '休眠{}s ... 等待app试玩结束!!'.format(self.try_app_sleep_time))
                try:
                    self._try_someone_app(device_obj=device_obj)
                except Exception as e:
                    print(self._get_print_base_str(device_obj=device_obj), e)
                    pass
                print(self._get_print_base_str(device_obj=device_obj) + '试玩结束!!')

                # 卸载某app
                self.uninstall_someone_app(device_obj=device_obj)

                # 返回趣头条app
                # TODO 红米重启后到首页了...需要改下再
                d.app_start(pkg_name=self.pkg_name)
                sleep(4.)

                # 领取奖励
                d(text=u"领取奖励", className="android.widget.TextView").click()
                toast_msg = d.toast.get_message(6., default='')
                print(self._get_print_base_str(device_obj=device_obj) + 'Toast msg: {}'.format(toast_msg))
                if '即可领取奖励' in toast_msg:
                    print(self._get_print_base_str(device_obj=device_obj) + '未试玩结束...')
                else:
                    pass

                # 每次领取完奖励必须下滑刷新一次
                u2_block_up_swipe_some_height(d=d, swipe_height=.5)
                sleep(4.)

                # 试玩结束...

            except UiObjectNotFoundError as e:
                print(self._get_print_base_str(device_obj=device_obj), e)
                # 下滑一个高度, 用于处理试玩app列表为空的情况, 进行下滑刷新list
                d.swipe(0., .3, 0., .3 + .5)
                # 避免频繁请求接口
                sleep_time = 15.
                print(self._get_print_base_str(device_obj=device_obj) + 'sleep time: {} ...'.format(sleep_time))
                sleep(sleep_time)

    def uninstall_someone_app(self, device_obj):
        """
        卸载某个app
        :return:
        """
        d: UIAutomatorServer = device_obj.d
        try:
            # 卸载某个app
            current_app_pkg_name = d.current_app().get('package', '')
            assert current_app_pkg_name != '', 'current_app_pkg_name != ""'
            assert current_app_pkg_name != self.pkg_name, "current_app_pkg_name != self.pkg_name"
            msg = 'current_app_pkg_name: {}, starting uninstall ...'.format(current_app_pkg_name)
            print(self._get_print_base_str(device_obj=device_obj) + msg)
            # 先停止app, 再进行卸载
            d.app_stop(pkg_name=current_app_pkg_name)
            d.app_uninstall(pkg_name=current_app_pkg_name)
        except Exception as e:
            print(self._get_print_base_str(device_obj=device_obj), e)

    @fz_set_timeout(seconds=3.15 * 60)
    def _try_someone_app(self, device_obj):
        """
        试玩某个app
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        total_sleep_time = 3.15 * 60
        index = 1
        # 每过下面秒数进行记录一次
        record_time_long = 10.
        while total_sleep_time - index * record_time_long > 0:
            # if d(text=u"允许", className="android.widget.Button").exists():
            #     # 允许所有申请的权限
            #     d(text=u"允许", className="android.widget.Button").click()

            if d(
                    resourceId="com.android.packageinstaller:id/permission_message",
                    textMatches=u"\w+申请获取定位权限|\w+申请读写手机存储权限|\w+申请拍照和录像权限",
                    className="android.widget.TextView").exists():
                # 处理权限申请相关弹窗
                d(
                    resourceId="com.android.packageinstaller:id/permission_allow_button",
                    text=u"允许",
                    className="android.widget.Button").click()

            if d(
                    resourceId="android:id/alertTitle",
                    text=u"\w+申请获取定位权限",
                    className="android.widget.TextView").exists():
                d(resourceId="android:id/button1", text=u"允许", className="android.widget.Button").click()

            if d(
                    resourceId="android:id/message",
                    text=u"允许 \w+ ROOT 权限|允许 \w+申请 ROOT 权限",
                    className="android.widget.TextView").exists():
                d(resourceId="android:id/button2", text=u"取消", className="android.widget.Button").click()

            sleep(record_time_long)
            msg = 'rest time: {}s'.format(total_sleep_time - index * record_time_long)
            print(self._get_print_base_str(device_obj=device_obj) + msg)
            index += 1
            # 自己手动进行相关操作 ...
            pass

    def _read_forever(self, device_obj):
        """
        read forever
        :param device_obj:
        :return:
        """
        print(self._get_print_base_str(device_obj=device_obj) + '即将开始自动化read...')
        sleep(12.)

        if self.short_name == 'qt':
            self._qt_read_forever(device_obj=device_obj)

        elif self.short_name == 'ht':
            self._ht_read_forever(device_obj=device_obj)

        elif self.short_name == 'sd':
            self._sd_read_forever(device_obj=device_obj)

        else:
            raise NotImplemented

    def _sd_read_forever(self, device_obj) -> None:
        """
        sd auto read(运行前先使用金山电池医生关闭其他耗电服务, 可有效降低耗电量, 提高脚本稳定性!!)
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        article_count = 0
        read_article_title_list = []
        while True:
            try:
                # 首页恶意弹窗处理
                self._ht_home_window_handle(device_obj=device_obj)
            except (AppNoResponseException, NoMoreArticlesException):
                break

            try:
                first_article_ele = d(
                    resourceId="c.l.a:id/title",
                    className="android.widget.TextView",
                    instance=0,)
                sub_title_ele = d(
                    resourceId="c.l.a:id/from_text",
                    className="android.widget.TextView",
                    instance=0,)
                article_title = first_article_ele.info.get('text', '')
                assert article_title not in read_article_title_list, \
                    'article_title in readed_article_title_list, so pass!'
                sub_title = sub_title_ele.info.get('text', '')
                # instance=0时, 如果未显示出子标题, 下滑直至其显示, 再判断是否合法
                assert sub_title != '', 'sub_title != ""'
                assert '广告' not in sub_title, '广告 in sub_title, pass'
                assert not d(resourceId="c.l.a:id/action", text=u"免费下载", className="android.widget.TextView").exists(), \
                    '广告, 让你下载app, pass'
                # 广告, 让你下载app
                assert not d(className="com.tencent.tbs.core.webkit.WebView").exists(), \
                    '广告, 让你下载app, pass!'
                # 点击进入文章
                first_article_ele.click()

                # 阅读完该文章并返回上一页
                self._sd_read_one_article(
                    device_obj=device_obj,
                    article_title=article_title,
                    article_count=article_count, )
                article_count += 1
                if article_title not in read_article_title_list:
                    read_article_title_list.append(article_title)

            except (UiObjectNotFoundError, AssertionError, Exception) as e:
                print(self._get_print_base_str(device_obj=device_obj), e)
                u2_block_up_swipe_some_height(d=d, swipe_height=.3,)
                sleep_random_time(1., 1.5)
                continue

            u2_block_up_swipe_some_height(d=d, swipe_height=.3)
            # 避免下滑过于频繁
            sleep_random_time(1., 1.5)

        self._restart_app_and_continue_actions(
            device_obj=device_obj,
            actions_name='read')

    def _sd_read_one_article(self, device_obj, article_title, article_count) -> None:
        """
        sd 阅读某篇文章
        :param device_obj:
        :param article_title:
        :param article_count:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        msg = self.base_read_print_str.format(
            article_count,
            article_title, )
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while True:
            if swipe_count >= 8:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            if d(resourceId="c.l.a:id/tv", text=u"每个评价都能获得高额奖励", className="android.widget.TextView").exists():
                # look goods
                d(resourceId="c.l.a:id/confirm", text=u"确定", className="android.widget.TextView").click()

            # 每次少滑点, 阅读文章速度慢了, 每篇收益更高
            u2_block_up_swipe_some_height(d=d, swipe_height=.45, base_height=.25)
            swipe_count += 1
            # 休眠一下, 反而每次阅读收益更多
            sleep_random_time(.15, .3)

        print(self._get_print_base_str(device_obj=device_obj) + 'read over!')
        while not d(
                resourceId="c.l.a:id/tab_text",
                text=u"我的",
                className="android.widget.TextView",).exists():
            u2_block_page_back(d=d, back_num=1)
            sleep(.5)

        return

    def _sd_home_window_handle(self, device_obj):
        """
        sd 首页弹窗处理
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        return

    def _ht_read_forever(self, device_obj) -> None:
        """
        ht auto read(运行前先使用金山电池医生关闭其他耗电服务, 可有效降低耗电量, 提高脚本稳定性!!)
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        article_count = 0
        while True:
            try:
                # 首页恶意弹窗处理
                self._ht_home_window_handle(device_obj=device_obj)
                if d(text=u"没有更多了", className="android.widget.TextView").exists():
                    # 说明首页文章已被下滑至底部
                    raise NoMoreArticlesException

            except (AppNoResponseException, NoMoreArticlesException):
                break

            if d(resourceId="com.cashtoutiao:id/tv_src", textMatches=u".*?广告|红包抽奖", className="android.widget.TextView").exists()\
                    or d(resourceId="com.cashtoutiao:id/tv_reward_header_tip", text=u"浏览广告赢更多金币", className="android.widget.TextView").exists():
                print(self._get_print_base_str(device_obj=device_obj) + '有广告, 跳过!')
                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                # 避免下滑过于频繁
                sleep_random_time(1., 1.5)
                continue

            if d(resourceId="com.cashtoutiao:id/count_down_tv", text=u"点击领取", className="android.widget.TextView").exists():
                # 获取首页定时金币
                print(self._get_print_base_str(device_obj=device_obj) + '@@@ 获取到定时金币!')
                d(resourceId="com.cashtoutiao:id/count_down_tv", text=u"点击领取", className="android.widget.TextView").click()
                d(resourceId="com.cashtoutiao:id/tv_left", text=u"忽略", className="android.widget.TextView").click()

            self._clear_app_memory(
                device_obj=device_obj,
                article_count=article_count,)
            try:
                first_article_ele = d(
                    resourceId="com.cashtoutiao:id/tv_title",
                    className="android.widget.TextView",
                    instance=0,)
                article_title = first_article_ele.info.get('text', '')
                # 点击进入文章
                first_article_ele.click()

                # 视频文章无法播放处理
                toast_msg = d.toast.get_message(wait_timeout=.2, default='')
                assert toast_msg != '手机系统版本过低', '手机系统版本过低, 无法播放视频, 跳过该视频文章!'

                # 阅读完该文章并返回上一页
                self._ht_read_one_article(
                    device_obj=device_obj,
                    article_title=article_title,
                    article_count=article_count,)
                article_count += 1

            except (UiObjectNotFoundError, Exception) as e:
                print(self._get_print_base_str(device_obj=device_obj), e)

                if d(resourceId="com.cashtoutiao:id/up_keyboard", text=u"写评论...", className="android.widget.TextView").exists():
                    # 表明未退回首页, 还在文章内部, 此处进行退出!
                    u2_block_page_back(d=d, back_num=1)

                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            u2_block_up_swipe_some_height(d=d, swipe_height=.3)
            # 避免下滑过于频繁
            sleep_random_time(1., 1.5)

        self._restart_app_and_continue_actions(
            device_obj=device_obj,
            actions_name='read')

    @fz_set_timeout(seconds=2.5 * 60)
    def _read_someone_time_duration(self, device_obj) -> None:
        """
        ht 阅读指定时长
        :param device_obj:
        :return:
        """
        # TODO 原先超时退出后while True还在执行
        self._read_forever(device_obj=device_obj)

    def _ht_home_window_handle(self, device_obj) -> None:
        """
        ht 首页弹窗处理
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        if d(resourceId="com.cashtoutiao:id/tv_reload", text=u"刷新", className="android.widget.TextView").exists():
            d(resourceId="com.cashtoutiao:id/tv_reload", text=u"刷新", className="android.widget.TextView").click()
            sleep(6.)

        if d(resourceId="com.cashtoutiao:id/yes_update_btn", text=u"安全升级", className="android.widget.TextView").exists():
            d(resourceId="com.cashtoutiao:id/close_update_btn", text=u"以后再说", className="android.widget.TextView").click()

        if d(resourceId="com.cashtoutiao:id/tv_next_see", text=u"以后再说", className="android.widget.TextView").exists():
            d(resourceId="com.cashtoutiao:id/iv_close", className="android.widget.ImageView").click()

        if d(resourceId="com.cashtoutiao:id/img_close", className="android.widget.ImageView").exists():
            d(resourceId="com.cashtoutiao:id/img_close", className="android.widget.ImageView").click()

        return

    def _ht_read_one_article(self, device_obj, article_title, article_count):
        """
        ht read someone article
        :param device_obj:
        :param article_title:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        msg = self.base_read_print_str.format(
            article_count,
            article_title,)
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while True:
            if swipe_count > 8:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            if d(resourceId="com.cashtoutiao:id/msg", text=u"当前为移动网络，请点击播放", className="android.widget.TextView").exists():
                # 视频文章, 点击播放
                try:
                    d(resourceId="com.cashtoutiao:id/continue_play", text=u"继续播放", className="android.widget.TextView").click()
                except UiObjectNotFoundError:
                    pass

            # 展开全文按钮
            # meizu
            unfold_full_text_btn1 = d(text=u"展开全文", className="android.view.View",)
            # 1s or r7s
            # unfold_full_text_btn2 = d(description=u"展开全文", className="android.view.View",)
            unfold_full_text_btn2: UiObject = u2_get_ui_obj(
                d=d,
                text='',
                description=u"展开全文",
                className="android.view.View",
                clickable=True,
                enabled=True,)

            if unfold_full_text_btn1.exists():
                unfold_full_text_btn1.click()

            if unfold_full_text_btn2.exists():
                unfold_full_text_btn2.click()

            # 每次少滑点, 阅读文章速度慢了, 每篇收益更高
            u2_block_up_swipe_some_height(d=d, swipe_height=.45, base_height=.25)
            swipe_count += 1
            # 休眠一下, 反而每次阅读收益更多
            sleep_random_time(.1, .25)

        print(self._get_print_base_str(device_obj=device_obj) + 'read over!')
        while not d(text=u"我的", className="android.widget.TextView").exists():
            u2_block_page_back(d=d, back_num=1)

        return

    def _qt_read_forever(self, device_obj) -> None:
        """
        qt auto read
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        article_count = 0
        first_article_ele = d(
            resourceId="com.jifen.qukan:id/a3t",
            className="android.widget.TextView",
            instance=0)
        while True:
            try:
                # 首页恶意弹窗处理
                self._qt_home_window_handle(device_obj=device_obj)
            except AppNoResponseException:
                break

            if not first_article_ele.exists():
                # 刚启动app时由于网络因素, 首页数据未加载出来, 下滑加载
                d.swipe(0., .3, 0., .3 + .4)
                sleep(2.)

            if d(resourceId="com.jifen.qukan:id/a54", text=u"广告", className="android.widget.TextView").exists()\
                    or d(resourceId="com.jifen.qukan:id/a69", text=u"广告", className="android.widget.TextView").exists():
                print(self._get_print_base_str(device_obj=device_obj) + '有广告, 跳过!')
                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            if d(resourceId="com.jifen.qukan:id/w4", text=u"领取", className="android.widget.TextView").exists():
                # 获取首页定时金币
                print(self._get_print_base_str(device_obj=device_obj) + '@@@ 获取到定时金币!')
                d(resourceId="com.jifen.qukan:id/w4", text=u"领取", className="android.widget.TextView").click()

            # 周期清内存
            self._clear_app_memory(device_obj=device_obj, article_count=article_count)
            try:
                article_title = first_article_ele.info.get('text', '')
                # 点击进入文章
                first_article_ele.click()
                # 阅读完该文章并返回上一页
                self._qt_read_one_article(
                    device_obj=device_obj,
                    article_title=article_title,
                    article_count=article_count,)
                article_count += 1

                if d(resourceId="com.jifen.qukan:id/s_", text=u"立即开启", className="android.widget.TextView").exists():
                    # 处理弹窗
                    d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()
                else:
                    pass

            except (UiObjectNotFoundError, Exception) as e:
                print(self._get_print_base_str(device_obj=device_obj), e)
                # 异常处理
                if d(resourceId="com.jifen.qukan:id/sb",
                     text=u"确认要下载此链接吗？",
                     className="android.widget.TextView").exists():
                    # 下载弹窗处理
                    d(resourceId="com.jifen.qukan:id/rm", text=u"取消", className="android.widget.TextView").click()

                if d(resourceId="com.jifen.qukan:id/aea", text=u"我来说两句...", className="android.widget.TextView").exists():
                    # 表示未退出文章, 先退出文章
                    u2_block_page_back(d=d, back_num=1)

                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            u2_block_up_swipe_some_height(d=d, swipe_height=.3)

        self._restart_app_and_continue_actions(
            device_obj=device_obj,
            actions_name='read')

    def _restart_app_and_continue_actions(self, device_obj, actions_name='read'):
        """
        重启app, 继续read
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        # 清除app 数据并重启
        # d.app_clear(pkg_name=self.pkg_name)
        d.app_stop(pkg_name=self.pkg_name)
        try:
            del d
        except Exception:
            pass
        new_device_obj = u2_get_device_obj_by_device_id(
            u2=u2,
            device_id=device_obj.device_id,
            pkg_name=self.pkg_name,
            d_debug=self.d_debug,
            set_fast_input_ime=self.set_fast_input_ime, )

        if actions_name == 'read':
            return self._read_forever(device_obj=new_device_obj)

        elif actions_name == 'look_goods':
            return self._auto_look_goods(device_obj=new_device_obj)

        else:
            raise NotImplemented

    def _qt_home_window_handle(self, device_obj) -> None:
        """
        qt首页恶意弹窗处理
        :param device_obj:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        if d(resourceId="com.jifen.qukan:id/se", text=u"开启推送通知", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/sk", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/fr", text=u"版本升级", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/ux", text=u"以后更新", className="android.widget.TextView").click()

        if d(resourceId="com.jifen.qukan:id/a2c", text=u"先去逛逛", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/a2c", text=u"先去逛逛", className="android.widget.TextView").click()

        if d(resourceId="com.jifen.qukan:id/fr", text=u"锁屏看资讯每日60金币送不停", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/fr", text=u"开启 签到 提醒", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/i3", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/zi", text=u"输入好友邀请码或手机号可得", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/zp", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/a0g", text=u"输入好友邀请码或手机号可得", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/a0n", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/ug", text=u"您将获得以下专属权益", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/uk", className="android.widget.ImageView").click()

        if d(resourceId="android:id/alertTitle", text=u"趣头条无响应，要将其关闭吗？", className="android.widget.TextView").exists():
            print(self._get_print_base_str(device_obj=device_obj) + 'app 无响应!!')
            d(resourceId="android:id/button2", text=u"等待", className="android.widget.Button").click()
            # TODO 长期运行会卡在此处无响应
            raise AppNoResponseException

        # 首次启动app, 会弹出
        if d(resourceId="com.jifen.qukan:id/a2c", text=u"先去逛逛", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/a2c", text=u"先去逛逛", className="android.widget.TextView").click()

        # r7s gps定位
        if d(resourceId="oppo:id/permission_prompt", text=u"趣头条正在尝试使用GPS定位（注：软件还可以通过其他途径获取位置信息）", className="android.widget.TextView").exists():
            # 勾选不再提醒
            d(resourceId="oppo:id/remember_cb", text=u"不再提醒", className="android.widget.CheckBox").click()
            d(resourceId="android:id/button2", textMatches=u"拒绝", className="android.widget.Button").click()

        return

    def _clear_app_memory(self, device_obj, article_count) -> None:
        """
        清理app内存并返回首页
        :param device_obj:
        :param article_count:
        :return:
        """
        if self.short_name == 'qt':
            self._qt_clear_app_memory(
                device_obj=device_obj,
                article_count=article_count)

        elif self.short_name == 'ht':
            self._ht_clear_app_memory(
                device_obj=device_obj,
                article_count=article_count,)

        else:
            raise NotImplemented

    def _ht_clear_app_memory(self, device_obj, article_count) -> None:
        """
        ht清理app内存并返回首页
        :param device_obj:
        :param article_count:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        if article_count % self.clear_app_base_num == 0 \
                and article_count != 0:
            msg = 'article_count: {}, clear app memory...'.format(article_count)
            print(self._get_print_base_str(device_obj=device_obj) + msg)
            d(text=u"我的", className="android.widget.TextView").click()
            sleep(3.)

            # 下滑显示系统设置
            u2_block_up_swipe_some_height(d=d, swipe_height=.5)
            d(resourceId="com.cashtoutiao:id/system_rl_settings", className="android.widget.RelativeLayout").click()
            d(text=u"清除缓存", className="android.widget.TextView").click()
            sleep(12.)
            print(self._get_print_base_str(device_obj=device_obj) + 'clear over!')
            u2_block_page_back(d=d, back_num=1)
            # 点击返回头条
            d(text=u"头条", className="android.widget.TextView").click()
            # 下滑一次, 避免重复阅读
            u2_block_up_swipe_some_height(d=d, swipe_height=.3)

        else:
            pass

    def _qt_clear_app_memory(self, device_obj, article_count) -> None:
        """
        qt清理app内存并返回首页
        :param device_obj:
        :param article_count:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        if article_count % self.clear_app_base_num == 0\
                and article_count != 0:
            msg = 'article_count: {}, clear app memory...'.format(article_count)
            print(self._get_print_base_str(device_obj=device_obj) + msg)
            d(resourceId="com.jifen.qukan:id/jl", text=u"我的", className="android.widget.Button").click()
            sleep(3.)

            if d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").exists():
                # 处理我的里面的弹窗
                d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").click()

            if d(resourceId="com.jifen.qukan:id/a0a", className="android.widget.ImageView").exists():
                d(resourceId="com.jifen.qukan:id/a0a", className="android.widget.ImageView").click()

            if d(resourceId="com.jifen.qukan:id/a09", className="android.widget.ImageView").exists():
                d(resourceId="com.jifen.qukan:id/a09", className="android.widget.ImageView").click()

            d(resourceId="com.jifen.qukan:id/aiy", className="android.widget.ImageView", instance=1).click()
            d(text=u"清除缓存", className="android.widget.TextView").click()
            sleep(3.)
            print(self._get_print_base_str(device_obj=device_obj) + 'clear over!')
            u2_block_page_back(d=d, back_num=1)
            # 点击返回头条
            d(resourceId="com.jifen.qukan:id/jf", text=u"头条", className="android.widget.Button").click()
            # 下滑一次, 避免重复阅读
            u2_block_up_swipe_some_height(d=d, swipe_height=.3)

        else:
            pass

    def _qt_read_one_article(self, device_obj, article_title, article_count) -> None:
        """
        qt阅读完单篇article并返回上一层
        :param article_title:
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        msg = self.base_read_print_str.format(
            article_count,
            article_title,)
        print(self._get_print_base_str(device_obj=device_obj) + msg)
        sleep_random_time(1., 1.5)
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while not d(
                resourceId="com.jifen.qukan:id/ny",
                text=u"没有更多咯~",
                className="android.widget.TextView").exists():
            if swipe_count >= 10:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            if d(resourceId="com.jifen.qukan:id/xw", className="android.widget.ImageView").exists():
                # 表明该文章为图片文章, 即多张图片
                # 右滑
                d.swipe(.6, .2, .2, .2)
                swipe_count += 1
                sleep(.1)
                continue

            if d(text=u"评论赞赏上线了", className="android.widget.TextView").exists():
                d(resourceId="com.jifen.qukan:id/pt", text=u"去赞赏", className="android.widget.Button").click()

            if d(resourceId="com.jifen.qukan:id/mx", text=u"继续观看", className="android.widget.Button").exists():
                d(resourceId="com.jifen.qukan:id/mx", text=u"继续观看", className="android.widget.Button").click()

            u2_block_up_swipe_some_height(d=d, swipe_height=.7)
            swipe_count += 1
            sleep_random_time(.1, .25)

        print(self._get_print_base_str(device_obj=device_obj) + 'read over!')
        u2_block_page_back(d=d, back_num=1)

        return

    @staticmethod
    def _get_print_base_str(device_obj) -> str:
        """
        基础打印str
        :return:
        """
        now_time_str_fuc = lambda : str(get_shanghai_time())

        return '[{} device_id: {:16s}, device_product_name: {:14s}] '.format(
            now_time_str_fuc(),
            device_obj.device_id,
            device_obj.device_product_name,)
    
    @staticmethod
    def _get_qt_installed_app_name_list() -> list:
        """
        ht 已被安装过的app(先不处理, 全重新安装)
        :return:
        """
        return [
            '好运APP',
            'QQ音乐',
            '陌陌',
            '腾讯手机管家',
            '一键清理',
            '360影视大全',
            '红人直播',
            '腾讯视频',
            '免费淘小说',
            '映客',
            'YY',
            '微视',
            '全民K歌',
            'KK美女直播',
            '波波视频',
            '应用宝',
            '233小游戏',
            '2345王牌手机助手',
            'QQ浏览器',
            '豌豆荚',
        ]

    def __del__(self):
        try:
            del self.loop
            del self.device_id_list
            del self.device_obj_list
            del self.wool_app_info
        except:
            pass
        collect()

@click_command()
@click_option('--app_name', type=str, default=None, help='value in ("qt", "ht", "sd")')
@click_option('--auto_read', type=int, default=0, help='value in (0, 1)')
@click_option('--auto_try_app', type=int, default=0, help='value in (0, 1)')
@click_option('--auto_register', type=int, default=0, help='value in (0, 1)')
@click_option('--get_now_pkg_name', type=int, default=0, help='value in (0, 1)')
@click_option('--auto_look_goods', type=int, default=0, help='value in (0, 1)')
@click_option('--auto_play_game', type=int, default=0, help='value in (0, 1)')
@click_option('--game_name', type=str, default=None, help='value in ("shff",)')
def init_mattress_wool_ops(app_name,
                           auto_read: int,
                           auto_try_app: int,
                           auto_register: int,
                           get_now_pkg_name: int,
                           auto_look_goods: int,
                           auto_play_game: int,
                           game_name: str):
    """
    main
    :param app_name:
    :param auto_read:
    :param auto_try_app:
    :param auto_register:
    :param get_now_pkg_name:
    :return:
    """
    global APP_NAME, AUTO_READ, AUTO_TRY_APP, AUTO_REGISTER, AUTO_GET_NOW_PKG_NAME, AUTO_LOOK_GOODS, AUTO_PLAY_GAME, GAME_NAME

    APP_NAME = app_name
    AUTO_READ = auto_read
    AUTO_TRY_APP = auto_try_app
    AUTO_REGISTER = auto_register
    AUTO_GET_NOW_PKG_NAME = get_now_pkg_name
    AUTO_LOOK_GOODS = auto_look_goods
    AUTO_PLAY_GAME = auto_play_game
    GAME_NAME = game_name
    loop = None
    try:
        _ = MattressWoolOps()
        loop = get_event_loop()
        res = loop.run_until_complete(_._fck_run())
    except KeyboardInterrupt:
        pass
    finally:
        try:
            loop.close()
            del loop
        except:
            pass

if __name__ == '__main__':
    init_mattress_wool_ops()