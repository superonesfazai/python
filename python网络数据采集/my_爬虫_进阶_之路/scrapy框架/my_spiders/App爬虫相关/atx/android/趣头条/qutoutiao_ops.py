# coding:utf-8

'''
@author = super_fazai
@File    : qutoutiao_ops.py
@connect : superonesfazai@gmail.com
'''

"""
趣头条自动阅读
"""

from gc import collect
import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.app_utils import (
    u2_page_back,
    u2_up_swipe_some_height,)
from fzutils.spider.async_always import *

class QuTouTiaoOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        self.d = u2.connect(addr="816QECTK24ND8")        # meizu
        print(self.d.info)
        self.d.set_fastinput_ime(True)
        self.d.debug = False
        self.now_session = self.d.session(pkg_name="com.jifen.qukan")
        # 清理app的基数
        self.clear_app_base_num = 25

    async def _fck_run(self):
        await self._read_forever()

    async def _read_forever(self):
        """
        read forever
        :return:
        """
        print('即将开始自动化read...')
        article_count = 0
        while True:
            if self.d(resourceId="com.jifen.qukan:id/fr", text=u"开启 签到 提醒", className="android.widget.TextView").exists():
                self.d(resourceId="com.jifen.qukan:id/i3", className="android.widget.ImageView").click()

            if self.d(resourceId="com.jifen.qukan:id/zi", text=u"输入好友邀请码或手机号可得", className="android.widget.TextView").exists():
                self.d(resourceId="com.jifen.qukan:id/zp", className="android.widget.ImageView").click()

            if self.d(resourceId="android:id/alertTitle", text=u"趣头条无响应，要将其关闭吗？", className="android.widget.TextView").exists():
                self.d(resourceId="android:id/button2", text=u"等待", className="android.widget.Button").click()

            if self.d(resourceId="com.jifen.qukan:id/ug", text=u"您将获得以下专属权益", className="android.widget.TextView").exists():
                self.d(resourceId="com.jifen.qukan:id/uk", className="android.widget.ImageView").click()

            if self.d(resourceId="com.jifen.qukan:id/a54", text=u"广告", className="android.widget.TextView").exists():
                print('有广告, 跳过!')
                await u2_up_swipe_some_height(d=self.d, swipe_height=.3)
                continue

            if self.d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").exists():
                # 获取首页定时金币
                print('@@@ 获取到定时金币!')
                self.d(resourceId="com.jifen.qukan:id/v7", text=u"领取", className="android.widget.TextView").click()

            # 周期清内存
            await self._clear_app_memory(article_count=article_count)
            try:
                first_article_ele = self.d(
                    resourceId="com.jifen.qukan:id/a2t",
                    className="android.widget.TextView",
                    instance=0)
                article_title = first_article_ele.info.get('text', '')
                # 点击进入文章
                first_article_ele.click()
                # 阅读完该文章并返回上一页
                await self._read_one_article(article_title=article_title)
                article_count += 1

                if self.d(
                        resourceId="com.jifen.qukan:id/s_",
                        text=u"立即开启",
                        className="android.widget.TextView").exists():
                    # 处理弹窗
                    self.d(resourceId="com.jifen.qukan:id/sa", className="android.widget.ImageView").click()
                else:
                    pass

            except (UiObjectNotFoundError, Exception) as e:
                print(e)
                await u2_up_swipe_some_height(d=self.d, swipe_height=.3)
                continue

            await u2_up_swipe_some_height(d=self.d, swipe_height=.3)

    async def _clear_app_memory(self, article_count) -> None:
        """
        清理app内存
        :return:
        """
        if article_count % self.clear_app_base_num == 0\
                and article_count != 0:
            print('article_count: {}, clear app memory...'.format(article_count))
            self.d(resourceId="com.jifen.qukan:id/ji", text=u"我的", className="android.widget.Button").click()
            await async_sleep(2.5)
            self.d(resourceId="com.jifen.qukan:id/ah_", className="android.widget.ImageView", instance=1).click()
            self.d(text=u"清除缓存", className="android.widget.TextView").click()
            await async_sleep(3.)
            print('clear over!')
            await u2_page_back(d=self.d, back_num=1)
            # 点击返回头条
            self.d(resourceId="com.jifen.qukan:id/jc", text=u"头条", className="android.widget.Button").click()

        else:
            pass

    async def _read_one_article(self, article_title) -> None:
        """
        阅读完单篇article并返回上一层
        :return:
        """
        print('[{}] reading {} ...'.format(str(get_shanghai_time()), article_title))
        swipe_count = 0
        # 下滑直至文章被完全阅读
        while not self.d(
                resourceId="com.jifen.qukan:id/nw",
                text=u"没有更多咯~",
                className="android.widget.TextView").exists():
            if swipe_count > 15:
                # 原因: 长时间阅读评论, 收获金币有限
                break

            await u2_up_swipe_some_height(d=self.d, swipe_height=.7)
            swipe_count += 1

        print('[{}] read over!'.format(str(get_shanghai_time())))
        await u2_page_back(d=self.d, back_num=1)

        return

    def __del__(self):
        try:
            del self.loop
            del self.d
            del self.now_session
        except:
            pass
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    _ = QuTouTiaoOps()
    loop.run_until_complete(_._fck_run())