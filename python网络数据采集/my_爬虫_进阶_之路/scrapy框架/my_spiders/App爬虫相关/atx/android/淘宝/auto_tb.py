# coding:utf-8

'''
@author = super_fazai
@File    : auto_tb.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
import uiautomator2 as u2
from uiautomator2.session import UiObject
from uiautomator2.exceptions import UiObjectNotFoundError
from fzutils.spider.app_utils import (
    u2_get_some_ele_height,
    u2_page_back,
    u2_get_device_display_h_and_w,)
from fzutils.spider.async_always import *

class TaoBaoOps(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        # adb device 查看
        self.d = u2.connect('816QECTK24ND8')
        print(self.d.info)
        self.d.set_fastinput_ime(True)
        self.d.debug = False
        self.now_session = self.d.session(pkg_name='com.taobao.taobao')
        self.max_shop_crawl_count = 20                                          # 一个keyword需要抓取的店铺数

    async def _fck_run(self):
        print('开始运行...')
        await self._search()
        print('运行完毕!')

    async def _search(self):
        """
        搜索
        :return:
        """
        # 首页点击搜索框
        self.d(resourceId="com.taobao.taobao:id/home_searchedit").click()

        keyword_list = ['aa', 'bb']

        for item in keyword_list:
            one_res = await self._search_shop_info_by_one_keyword(keyword=item)
            pprint(one_res)

        print('全部关键字采集完毕!!!')

    async def _search_shop_info_by_one_keyword(self, keyword) -> list:
        """
        根据某关键字进行相应采集
        :param keyword:
        :return:
        """
        print('--->>> 即将开始采集 keyword: {} 对应的shop info...'.format(keyword))
        # 搜索的是否为店铺
        is_shop_search = False
        res = []

        # 输入内容
        self.d(resourceId="com.taobao.taobao:id/searchEdit").send_keys(keyword)
        # 搜索
        self.d(resourceId="com.taobao.taobao:id/searchbtn").click()
        await async_sleep(2)

        if not is_shop_search:
            # 点击店铺(只需要点击一次, 后续都是以店铺来搜索的)
            self.d(resourceId="com.taobao.taobao:id/tab_text", text=u"店铺").click()
            await async_sleep(2)
            # 点击销量优先
            self.d(resourceId="com.taobao.taobao:id/show_text", text=u"销量优先", description=u"销量优先",
                   className="android.widget.TextView").click()
            is_shop_search = True

        # TODO 方案一无法再ele list里面定位某个特定ele, 并进行后续操作! pass
        # 方案2: 滑动一个采集一个
        self.first_swipe_height, self.second_swipe_height = await self._get_first_swipe_height_and_second_swipe_height()

        # 先上滑隐藏全部, 天猫, 店铺, 淘宝经验
        await self._u2_up_swipe_some_height(d=self.d, height=self.first_swipe_height)
        shop_name_list = []

        shop_crawl_count = 1
        while shop_crawl_count < self.max_shop_crawl_count:
            print()
            # TODO 不适用instance, 而是用ele index索引的原因是
            #   instance会导致循环到一定个数出现instance=0对应的某元素不在当前page, 而无法被点击, 导致后续操作紊乱
            # 当前页面的shop_title list
            now_page_shop_title_list = [
                item.info.get('text', '')
                for item in self.d(
                    resourceId="com.taobao.taobao:id/shopTitle",
                    className="android.widget.TextView",
                    clickable=False, )]
            pprint(now_page_shop_title_list)
            # clickable = False 确定当前页面某btn是否已被点击, 未被点击 False
            first_shop_title_ele = self.d(
                resourceId="com.taobao.taobao:id/shopTitle",
                className="android.widget.TextView",
                # instance=0,
                text=now_page_shop_title_list[1] if shop_crawl_count != 1 else now_page_shop_title_list[0],
                # 保证每个都被遍历
                clickable=False, )
            try:
                shop_title = first_shop_title_ele.info.get('text', '')
            except UiObjectNotFoundError:
                continue

            if shop_title not in shop_name_list:
                print('正在采集店名: {}, shop_crawl_count: {} ...'.format(shop_title, shop_crawl_count))
                shop_name_list.append(shop_title)
            else:
                print('该店名: {} 已遍历, pass'.format(shop_title))
                await self._u2_up_swipe_some_height(d=self.d, height=self.second_swipe_height)
                # await async_sleep(2)  # 等待新返回的list成功显示
                continue

            try:
                # 点击shop title ele进店
                # print('++++++ {} ele exists is {}'.format(shop_title, first_shop_title_ele.exists()))
                # print('即将点击first_shop_title_ele...')
                first_shop_title_ele.click()
                await async_sleep(3)
                # 点击粉丝数进入店铺印象页面
                self.d(descriptionMatches='粉丝数\d+.*?', className="android.view.View").click()
                await async_sleep(6)

                phone_exist = self.d(description='服务电话', className="android.view.View").exists()
                assert phone_exist is True, '[-] 无服务电话!!!'
                print('[+] 有服务电话!!!')
                phone_num = self.d(descriptionMatches="\d+-\d+|\d+", className="android.view.View") \
                    .info.get('contentDescription', '')
                print('@' * 10 + ' 服务电话: {}'.format(phone_num))

                res.append({
                    'shop_name': shop_title,
                    'phone': phone_num,
                })
            except (UiObjectNotFoundError, AssertionError) as e:
                print(e)
                while not first_shop_title_ele.exists():
                    await u2_page_back(d=self.d, back_num=1)

                continue

            # 返回搜索结果list页面
            # 默认返回前两页会页面混乱
            # await u2_page_back(d=self.d, back_num=2)
            # 改用元素定位来看是否成功返回上层
            while not first_shop_title_ele.exists():
                await u2_page_back(d=self.d, back_num=1)

            await self._u2_up_swipe_some_height(d=self.d, height=self.second_swipe_height)
            # await async_sleep(2)  # 等待新返回的list成功显示
            shop_crawl_count += 1

        print('--->>> 采集 keyword: {} 对应的shop info 完毕!'.format(keyword))

        return res

    async def _get_first_swipe_height_and_second_swipe_height(self) -> tuple:
        """
        获取first_swipe_height and second_swipe_height
        :return:
        """
        # 获取上方全部, 天猫, 店铺, 淘宝经验的parent 元素块的 height
        h1 = await u2_get_some_ele_height(ele=self.d(className="android.support.v7.app.ActionBar$Tab", instance=3))
        first_swipe_height = h1 / 1000

        # 获取综合排序的元素块 height
        h2 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/sortbtnContainer", className="android.widget.LinearLayout"))

        # 获取店铺label块 height
        h3 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/topLayout"))
        # 获取goods 块height
        h4 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/midLayout"))
        # 获取相似块的 height
        h5 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/shop_tag_line"))

        second_swipe_height = (h4 + h5) / 1000
        print('###### first_swipe_height: {}, second_swipe_height: {}, h2: {}'.format(
            first_swipe_height,
            second_swipe_height,
            h2/1000))

        return first_swipe_height, second_swipe_height

    async def _u2_up_swipe_some_height(self, d, height) -> None:
        """
        u2 上滑某个高度
        :param height:
        :return:
        """
        d.swipe(0., 0.1 + height, 0, 0.1)

    def __del__(self):
        try:
            del self.d
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = TaoBaoOps()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())