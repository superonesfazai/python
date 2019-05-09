# coding:utf-8

'''
@author = super_fazai
@File    : qutoutiao_ops.py
@connect : superonesfazai@gmail.com
'''

"""
趣头条ops阅读
"""

from gc import collect
import uiautomator2 as u2
# d对象的基础类
from uiautomator2 import UIAutomatorServer
from uiautomator2.exceptions import UiObjectNotFoundError
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.app_utils import (
    u2_page_back,
    u2_up_swipe_some_height,
    AndroidDeviceObj,)
from fzutils.spider.async_always import *
from fzutils.shell_utils import *

# 启动设备的id
DEVICE_ID = None

class QuTouTiaoOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        self.device_id = '816QECTK24ND8' if DEVICE_ID is None else DEVICE_ID
        # 设置设备id
        self.d = u2.connect(addr=self.device_id)
        d_info = self.d.info
        print(d_info)
        self.device_product_name = d_info.get('productName', '')
        assert self.device_product_name != '', 'self.device_product_name !=""'
        self.d.set_fastinput_ime(True)
        self.d.debug = False
        self.now_session = self.d.session(pkg_name="com.jifen.qukan")
        # 清理app的基数
        self.clear_app_base_num = 25

    async def _fck_run(self):
        await self._every_device_start_read()
        
    async def _every_device_start_read(self):
        """
        每台设备开始阅读...
        :return: 
        """
        device_obj = AndroidDeviceObj(
            d=self.d,
            device_id=self.device_id,
            device_product_name=self.device_product_name,)
        await self._read_forever(device_obj=device_obj)

    async def _read_forever(self, device_obj):
        """
        read forever
        :param device_obj:
        :return:
        """
        d:UIAutomatorServer = device_obj.d

        print('即将开始自动化read...')
        article_count = 0
        while True:
            if d(resourceId="com.jifen.qukan:id/fr", text=u"锁屏看资讯每日60金币送不停", className="android.widget.TextView").exists():
                d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()

            if d(resourceId="com.jifen.qukan:id/fr", text=u"开启 签到 提醒", className="android.widget.TextView").exists():
                d(resourceId="com.jifen.qukan:id/i3", className="android.widget.ImageView").click()

            if d(resourceId="com.jifen.qukan:id/zi", text=u"输入好友邀请码或手机号可得", className="android.widget.TextView").exists():
                d(resourceId="com.jifen.qukan:id/zp", className="android.widget.ImageView").click()

            if d(resourceId="android:id/alertTitle", text=u"趣头条无响应，要将其关闭吗？", className="android.widget.TextView").exists():
                d(resourceId="android:id/button2", text=u"等待", className="android.widget.Button").click()

            if d(resourceId="com.jifen.qukan:id/ug", text=u"您将获得以下专属权益", className="android.widget.TextView").exists():
                d(resourceId="com.jifen.qukan:id/uk", className="android.widget.ImageView").click()

            if d(resourceId="com.jifen.qukan:id/a54", text=u"广告", className="android.widget.TextView").exists():
                print('有广告, 跳过!')
                await u2_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            if d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").exists():
                # 获取首页定时金币
                print('@@@ 获取到定时金币!')
                d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").click()

            # 周期清内存
            await self._clear_app_memory(device_obj=device_obj, article_count=article_count)
            try:
                first_article_ele = d(
                    resourceId="com.jifen.qukan:id/a2t",
                    className="android.widget.TextView",
                    instance=0)
                article_title = first_article_ele.info.get('text', '')
                # 点击进入文章
                first_article_ele.click()
                # 阅读完该文章并返回上一页
                await self._read_one_article(device_obj=device_obj, article_title=article_title)
                article_count += 1

                if d(resourceId="com.jifen.qukan:id/s_", text=u"立即开启", className="android.widget.TextView").exists():
                    # 处理弹窗
                    d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()
                else:
                    pass

            except (UiObjectNotFoundError, Exception) as e:
                print(e)
                print('出错device_id: {}, device_product_name: {}'.format(device_obj.device_id, device_obj.device_product_name))
                # 异常处理
                if d(resourceId="com.jifen.qukan:id/acx", text=u"我来说两句...", className="android.widget.TextView").exists():
                    # 表示未退出文章, 先退出文章
                    await u2_page_back(d=d, back_num=1)

                await u2_up_swipe_some_height(d=d, swipe_height=.3)
                continue

            await u2_up_swipe_some_height(d=d, swipe_height=.3)

    async def _clear_app_memory(self, device_obj, article_count) -> None:
        """
        清理app内存并返回首页
        :param device_obj:
        :param article_count: 
        :return: 
        """
        d:UIAutomatorServer = device_obj.d

        if article_count % self.clear_app_base_num == 0\
                and article_count != 0:
            print('article_count: {}, clear app memory...'.format(article_count))
            d(resourceId="com.jifen.qukan:id/ji", text=u"我的", className="android.widget.Button").click()
            await async_sleep(2.5)

            if d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").exists():
                # 处理我的里面的弹窗
                d(resourceId="com.jifen.qukan:id/za", className="android.widget.ImageView").click()

            d(resourceId="com.jifen.qukan:id/ah_", className="android.widget.ImageView", instance=1).click()
            d(text=u"清除缓存", className="android.widget.TextView").click()
            await async_sleep(3.)
            print('clear over!')
            await u2_page_back(d=d, back_num=1)
            # 点击返回头条
            d(resourceId="com.jifen.qukan:id/jc", text=u"头条", className="android.widget.Button").click()
            # 下滑一次, 避免重复阅读
            await u2_up_swipe_some_height(d=d, swipe_height=.3)

        else:
            pass

    async def _read_one_article(self, device_obj, article_title) -> None:
        """
        阅读完单篇article并返回上一层
        :param d:
        :param article_title:
        :return:
        """
        d:UIAutomatorServer = device_obj.d

        print('[{} device_id: {}, device_product_name: {}] reading {} ...'.format(str(get_shanghai_time()), device_obj.device_id, device_obj.device_product_name, article_title))
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while not d(resourceId="com.jifen.qukan:id/nw", text=u"没有更多咯~", className="android.widget.TextView").exists():
            if swipe_count > 15:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            await u2_up_swipe_some_height(d=d, swipe_height=.7)
            swipe_count += 1

        print('[{} device_id: {}, device_product_name: {}] read over!'.format(str(get_shanghai_time()), device_obj.device_id, device_obj.device_product_name))
        await u2_page_back(d=d, back_num=1)

        return

    def __del__(self):
        try:
            del self.loop
            del self.d
            del self.now_session
        except:
            pass
        collect()

@click_command()
@click_option('--device_id', type=str, default=None, help='what is device_id !!')
def init_qytoutiao_ops_read(device_id,):
    """
    main
    :param device_id:
    :return:
    """
    global DEVICE_ID

    DEVICE_ID = device_id
    loop = None
    try:
        loop = get_event_loop()
        _ = QuTouTiaoOps()
        loop.run_until_complete(_._fck_run())
    except KeyboardInterrupt:
        pass
    finally:
        try:
            loop.close()
            del loop
        except:
            pass

if __name__ == '__main__':
    init_qytoutiao_ops_read()