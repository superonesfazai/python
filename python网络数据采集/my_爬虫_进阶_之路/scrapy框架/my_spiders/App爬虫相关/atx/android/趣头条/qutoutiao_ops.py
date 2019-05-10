# coding:utf-8

'''
@author = super_fazai
@File    : qutoutiao_ops.py
@connect : superonesfazai@gmail.com
'''

"""
趣头条ops
"""

from gc import collect
import uiautomator2 as u2
# d对象的基础类
from uiautomator2 import UIAutomatorServer
from uiautomator2.exceptions import UiObjectNotFoundError
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.app_utils import (
    u2_block_page_back,
    u2_block_up_swipe_some_height,
    get_u2_init_device_list,
    u2_get_device_obj_by_device_id,)
from fzutils.common_utils import _print
from fzutils.exceptions import AppNoResponseException
from fzutils.spider.async_always import *

class QuTouTiaoOps(AsyncCrawler):
    """趣头条ops"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        # 清理app的基数
        self.clear_app_base_num = 25
        self.try_app_sleep_time = 3.15 * 60
        self.pkg_name = 'com.jifen.qukan'
        self.d_debug = False
        self.set_fast_input_ime = True
        # device_id_list
        self.device_id_list = [
            '816QECTK24ND8',
        ]

    async def _fck_run(self):
        self.device_obj_list = await get_u2_init_device_list(
            loop=self.loop,
            u2=u2,
            pkg_name=self.pkg_name,
            device_id_list=self.device_id_list,
            d_debug=self.d_debug,
            set_fast_input_ime=self.set_fast_input_ime,)

        # auto read
        # await self._every_device_start_read()
        # auto try apps
        await self._every_device_start_auto_try_apps()

    async def _every_device_start_read(self):
        """
        每台设备开始阅读...
        :return: 
        """
        tasks = []
        for device_obj in self.device_obj_list:
            print('create task[where device_id: {}]...'.format(device_obj.device_id))
            tasks.append(self.loop.create_task(self._unblock_read_forever(
                device_obj=device_obj,
            )))

        all_res = await async_wait_tasks_finished(tasks=tasks)

        return all_res

    async def _unblock_read_forever(self, device_obj, logger=None):
        """
        非阻塞阅读
        :return:
        """
        async def _get_args() -> list:
            """获取args"""
            return [
                device_obj,
            ]

        loop = get_event_loop()
        args = await _get_args()
        res = None
        try:
            res = await loop.run_in_executor(None, self._read_forever, *args)
        except Exception as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        finally:
            # loop.close()
            try:
                del loop
            except:
                pass
            collect()

            return res

    async def _every_device_start_auto_try_apps(self):
        """
        每台设备开始试玩app
        :return:
        """
        tasks = []
        for device_obj in self.device_obj_list:
            print('create task[where device_id: {}]...'.format(device_obj.device_id))
            tasks.append(self.loop.create_task(self._unblock_auto_try_apps(
                device_obj=device_obj,
            )))

        all_res = await async_wait_tasks_finished(tasks=tasks)

        return all_res

    async def _unblock_auto_try_apps(self, device_obj, logger=None):
        """
        [非阻塞]试玩app
        :param device_obj:
        :return:
        """
        async def _get_args() -> list:
            """获取args"""
            return [
                device_obj,
            ]

        loop = get_event_loop()
        args = await _get_args()
        res = None
        try:
            res = await loop.run_in_executor(None, self._auto_try_apps, *args)
        except Exception as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        finally:
            # loop.close()
            try:
                del loop
            except:
                pass
            collect()

            return res

    def _auto_try_apps(self, device_obj):
        """
        自动试玩app
        :return:
        """
        d: UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + '即将开始auto试玩app...')
        # 先处理恶意弹窗
        self._home_window_handle(device_obj=device_obj)
        d(resourceId="com.jifen.qukan:id/jg", text=u"任务", className="android.widget.Button").click()
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
                try_app_btn = d(textMatches=u"打开注册并试玩|打开激活|打开试玩|打开浏览|打开使用", className="android.widget.TextView")

                if not try_app_btn.exists():
                    # 先前 该app未安装的情况
                    d(text=u"立即下载", className="android.widget.TextView").click()
                    print(self._get_print_base_str(device_obj=device_obj) + 'starting download ...')
                    while not d(resourceId="com.android.packageinstaller:id/virus_scan_done", text=u"确定要继续安装吗？", className="android.widget.TextView").exists():
                        pass

                    d(resourceId="com.android.packageinstaller:id/action_positive",
                      text=u"继续",
                      description=u"继续",
                      className="android.widget.TextView",).click()

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
                d.app_start(pkg_name=self.pkg_name)
                sleep(3.)

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
                print('出错device_id: {}, device_product_name: {}'.format(device_obj.device_id, device_obj.device_product_name), e)

    def uninstall_someone_app(self, device_obj):
        """
        卸载某个app
        :return:
        """
        d:UIAutomatorServer = device_obj.d
        try:
            # 卸载某个app
            current_app_pkg_name = d.current_app().get('package', '')
            assert current_app_pkg_name != '', 'current_app_pkg_name != ""'
            print(self._get_print_base_str(device_obj=device_obj) + 'current_app_pkg_name: {}, starting uninstall ...'.format(current_app_pkg_name))
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

            if d(resourceId="com.android.packageinstaller:id/permission_message",
                 textMatches=u"\w+申请获取定位权限|\w+申请读写手机存储权限|\w+申请拍照和录像权限",
                 className="android.widget.TextView").exists():
                # 处理权限申请相关弹窗
                d(resourceId="com.android.packageinstaller:id/permission_allow_button", text=u"允许", className="android.widget.Button").click()

            if d(resourceId="android:id/message", text=u"允许 \w+ ROOT 权限", className="android.widget.TextView").exists():
                d(resourceId="android:id/button2", text=u"取消", className="android.widget.Button").click()

            sleep(record_time_long)
            print(self._get_print_base_str(device_obj=device_obj) + 'rest time: {}s'.format(total_sleep_time - index * record_time_long))
            index += 1
            # 自己手动进行相关操作 ...
            pass

    def _read_forever(self, device_obj):
        """
        read forever
        :param device_obj:
        :return:
        """
        d:UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + '即将开始自动化read...')
        article_count = 0
        while True:
            try:
                # 首页恶意弹窗处理
                self._home_window_handle(device_obj=device_obj)
            except AppNoResponseException:
                break

            if d(resourceId="com.jifen.qukan:id/a54", text=u"广告", className="android.widget.TextView").exists():
                print(self._get_print_base_str(device_obj=device_obj) + '有广告, 跳过!')
                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            if d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").exists():
                # 获取首页定时金币
                print(self._get_print_base_str(device_obj=device_obj) + '@@@ 获取到定时金币!')
                d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").click()

            # 周期清内存
            self._clear_app_memory(device_obj=device_obj, article_count=article_count)
            try:
                first_article_ele = d(
                    resourceId="com.jifen.qukan:id/a2t",
                    className="android.widget.TextView",
                    instance=0)
                article_title = first_article_ele.info.get('text', '')
                # 点击进入文章
                first_article_ele.click()
                # 阅读完该文章并返回上一页
                self._read_one_article(device_obj=device_obj, article_title=article_title)
                article_count += 1

                if d(resourceId="com.jifen.qukan:id/s_", text=u"立即开启", className="android.widget.TextView").exists():
                    # 处理弹窗
                    d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()
                else:
                    pass

            except (UiObjectNotFoundError, Exception) as e:
                print('出错device_id: {}, device_product_name: {}'.format(device_obj.device_id, device_obj.device_product_name), e)
                # 异常处理
                if d(resourceId="com.jifen.qukan:id/acx", text=u"我来说两句...", className="android.widget.TextView").exists():
                    # 表示未退出文章, 先退出文章
                    u2_block_page_back(d=d, back_num=1)

                u2_block_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            u2_block_up_swipe_some_height(d=d, swipe_height=.3)

        # 清除app 数据并重启
        d.app_clear(pkg_name=self.pkg_name)
        try:
            del d
        except:
            pass
        new_device_obj = u2_get_device_obj_by_device_id(
            u2=u2,
            device_id=device_obj.device_id,
            pkg_name=self.pkg_name,
            d_debug=self.d_debug,
            set_fast_input_ime=self.set_fast_input_ime,)

        return self._read_forever(device_obj=new_device_obj)

    def _home_window_handle(self, device_obj) -> None:
        """
        首页恶意弹窗处理
        :param device_obj:
        :return:
        """
        d:UIAutomatorServer = device_obj.d

        if d(resourceId="com.jifen.qukan:id/fr", text=u"锁屏看资讯每日60金币送不停", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/fr", text=u"开启 签到 提醒", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/i3", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/zi", text=u"输入好友邀请码或手机号可得", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/zp", className="android.widget.ImageView").click()

        if d(resourceId="com.jifen.qukan:id/ug", text=u"您将获得以下专属权益", className="android.widget.TextView").exists():
            d(resourceId="com.jifen.qukan:id/uk", className="android.widget.ImageView").click()

        if d(resourceId="android:id/alertTitle", text=u"趣头条无响应，要将其关闭吗？", className="android.widget.TextView").exists():
            print(self._get_print_base_str(device_obj=device_obj) + 'app 无响应!!')
            d(resourceId="android:id/button2", text=u"等待", className="android.widget.Button").click()
            # TODO 长期运行会卡在此处无响应
            raise AppNoResponseException

        return

    def _clear_app_memory(self, device_obj, article_count) -> None:
        """
        清理app内存并返回首页
        :param device_obj:
        :param article_count: 
        :return: 
        """
        d:UIAutomatorServer = device_obj.d

        if article_count % self.clear_app_base_num == 0\
                and article_count != 0:
            print(self._get_print_base_str(device_obj=device_obj) + 'article_count: {}, clear app memory...'.format(article_count))
            d(resourceId="com.jifen.qukan:id/ji", text=u"我的", className="android.widget.Button").click()
            sleep(3.)

            if d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").exists():
                # 处理我的里面的弹窗
                d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").click()

            d(resourceId="com.jifen.qukan:id/ah_", className="android.widget.ImageView", instance=1).click()
            d(text=u"清除缓存", className="android.widget.TextView").click()
            sleep(3.)
            print(self._get_print_base_str(device_obj=device_obj) + 'clear over!')
            u2_block_page_back(d=d, back_num=1)
            # 点击返回头条
            d(resourceId="com.jifen.qukan:id/jc", text=u"头条", className="android.widget.Button").click()
            # 下滑一次, 避免重复阅读
            u2_block_up_swipe_some_height(d=d, swipe_height=.3)

        else:
            pass

    def _read_one_article(self, device_obj, article_title) -> None:
        """
        阅读完单篇article并返回上一层
        :param d:
        :param article_title:
        :return:
        """
        d:UIAutomatorServer = device_obj.d

        print(self._get_print_base_str(device_obj=device_obj) + 'reading {} ...'.format(article_title))
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while not d(resourceId="com.jifen.qukan:id/nw", text=u"没有更多咯~", className="android.widget.TextView").exists():
            if swipe_count > 15:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            u2_block_up_swipe_some_height(d=d, swipe_height=.7)
            swipe_count += 1

        print(self._get_print_base_str(device_obj=device_obj) + 'read over!')
        u2_block_page_back(d=d, back_num=1)

        return

    def _get_print_base_str(self, device_obj) -> str:
        """
        基础打印str
        :return:
        """
        now_time_str_fuc = lambda : str(get_shanghai_time())

        return '[{} device_id: {}, device_product_name: {}] '.format(
            now_time_str_fuc(),
            device_obj.device_id,
            device_obj.device_product_name,)

    def __del__(self):
        try:
            del self.loop
            del self.device_id_list
            del self.device_obj_list
        except:
            pass
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    _ = QuTouTiaoOps()
    loop.run_until_complete(_._fck_run())