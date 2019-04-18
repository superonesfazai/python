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
    u2_get_device_display_h_and_w,
    u2_up_swipe_some_height,)
from fzutils.spider.bloom_utils import BloomFilter
from fzutils.spider.async_always import *

class TaoBaoOps(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path='/Users/afa/myFiles/my_spider_logs/atx/tb/shop_info/',
        )
        # adb device 查看
        self.d = u2.connect('816QECTK24ND8')
        self.lg.info(self.d.info)
        self.d.set_fastinput_ime(True)
        self.d.debug = False
        self.now_session = self.d.session(pkg_name='com.taobao.taobao')
        self.max_shop_crawl_count = 100                                                   # 一个keyword需要抓取的店铺数
        self.tb_jb_hot_keyword_file_path = '/Users/afa/Desktop/tb_jb_hot_keyword.txt'     # 结巴分词后已检索的hot keyword写入处
        self.tb_ops_file_path = '/Users/afa/Desktop/tb_ops.txt'
        self._init_tb_jb_boom_filter()
        self._init_key_list()
        # 不遍历的list
        self.dump_shop_name_list = ['天猫超市', '阿里健康大药房', '天猫精灵官方旗舰店']

    def _init_key_list(self) -> None:
        """
        初始化待采集key
        :return:
        """
        self.lg.info('初始化ing self.key_list ...')
        self.key_list = []
        index = 0
        with open(self.tb_jb_hot_keyword_file_path, 'r') as f:
            try:
                for line in f:
                    item = line.replace('\n', '')
                    if item not in self.key_list:
                        self.lg.info('add {}, index: {}'.format(item, index))
                        self.key_list.append(item)
                        index += 1
            except UnicodeDecodeError as e:
                self.lg.error('遇到错误: {}'.format(e))

        self.lg.info('初始化完毕! len: {}'.format(self.key_list.__len__()))

        return None

    def _init_tb_jb_boom_filter(self) -> None:
        """
        初始化
        :return:
        """
        self.lg.info('初始化ing self.tb_jb_boom_filter ...')
        # 结巴分词后已检索的hot keyword存储
        self.tb_jb_boom_filter = BloomFilter(
            capacity=500000,
            error_rate=.00001)
        index = 0
        try:
            with open(self.tb_ops_file_path, 'r') as f:
                try:
                    for line in f:
                        item = line.replace('\n', '')
                        if item not in self.tb_jb_boom_filter:
                            self.lg.info('add {}, index: {}'.format(item, index))
                            self.tb_jb_boom_filter.add(item)
                            index += 1

                except UnicodeDecodeError as e:
                    self.lg.error('遇到错误: {}'.format(e))

        except Exception as e:
            self.lg.error('遇到错误:', exc_info=True)
            raise e

        self.lg.info('初始化完毕! len: {}'.format(self.tb_jb_boom_filter.__len__()))

        return None

    async def _fck_run(self):
        self.lg.info('开始运行...')
        await self._search()
        self.lg.info('运行完毕!')

    async def _search(self):
        """
        搜索
        :return:
        """
        # 首页点击搜索框
        self.d(resourceId="com.taobao.taobao:id/home_searchedit").click()

        for keyword in self.key_list:
            if keyword in self.tb_jb_boom_filter:
                # 去除已遍历的过的hot key
                self.lg.info('hot key: {} in self.tb_jb_boom_filter'.format(keyword))
                continue

            one_res = await self._search_shop_info_by_one_keyword(keyword=keyword)
            # pprint(one_res)
            # add record
            await self._write_tb_ops_txt(target_list=[keyword])
            self.tb_jb_boom_filter.add(keyword)

        self.lg.info('全部关键字采集完毕!!!')

    async def _search_shop_info_by_one_keyword(self, keyword) -> list:
        """
        根据某关键字进行相应采集
        :param keyword:
        :return:
        """
        self.lg.info('--->>> 即将开始采集 keyword: {} 对应的shop info...'.format(keyword))
        # 搜索的是否为店铺
        is_shop_search = False

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
            self.d(
                resourceId="com.taobao.taobao:id/show_text",
                text=u"销量优先",
                description=u"销量优先",
                className="android.widget.TextView").click()
            is_shop_search = True

        await async_sleep(2)
        if self.d(
                resourceId="com.taobao.taobao:id/tipTitle",
                text=u"没有搜索结果",
                className="android.widget.TextView")\
                .exists():
            # 处理没有搜索结果的
            self.lg.info('### 该关键字: {} 无搜索结果!'.format(keyword))
            return []

        # TODO 方案一无法再ele list里面定位某个特定ele, 并进行后续操作! pass
        # 方案2: 滑动一个采集一个
        self.first_swipe_height, self.second_swipe_height = await self._get_first_swipe_height_and_second_swipe_height()
        self.lg.info('self.first_swipe_height: {}, self.second_swipe_height: {}'.format(self.first_swipe_height, self.second_swipe_height))

        # 先上滑隐藏全部, 天猫, 店铺, 淘宝经验
        await u2_up_swipe_some_height(d=self.d, swipe_height=self.first_swipe_height)

        shop_name_list = []
        shop_crawl_count = 1
        res = []
        while shop_crawl_count < self.max_shop_crawl_count:
            # TODO 不适用instance, 而是用ele index索引的原因是
            #   instance会导致循环到一定个数出现instance=0对应的某元素不在当前page, 而无法被点击, 导致后续操作紊乱
            # 当前页面的shop_title list
            now_page_shop_title_list = [
                item.info.get('text', '')
                for item in self.d(
                    resourceId="com.taobao.taobao:id/shopTitle",
                    className="android.widget.TextView",
                    clickable=False, )]
            self.lg.info('now_page_shop_title_list: {}'.format(str(now_page_shop_title_list)))
            try:
                assert now_page_shop_title_list != [], 'now_page_shop_title_list不为空list!'
            except AssertionError:
                # 从店铺首页返回搜索页
                await u2_page_back(d=self.d, back_num=1)
                await u2_up_swipe_some_height(
                    d=self.d,
                    swipe_height=self.second_swipe_height)
                await async_sleep(1.)  # 等待新返回的list成功显示
                continue

            # clickable = False 确定当前页面某btn是否已被点击, 未被点击 False
            first_shop_title_ele = self.d(
                resourceId="com.taobao.taobao:id/shopTitle",
                className="android.widget.TextView",
                # instance=0,
                text=now_page_shop_title_list[1] if shop_crawl_count != 1 else now_page_shop_title_list[0],
                # 保证每个都被遍历
                clickable=False,)
            try:
                shop_title = first_shop_title_ele.info.get('text', '')
            except UiObjectNotFoundError:
                continue

            if shop_title not in shop_name_list \
                    and shop_title not in self.dump_shop_name_list:
                self.lg.info('正在采集店名: {}, shop_crawl_count: {} ...'.format(shop_title, shop_crawl_count))
                shop_name_list.append(shop_title)

            else:
                # 处理已遍历的店 or 不遍历的店
                self.lg.info('该店名: {} 已遍历, pass'.format(shop_title))
                await u2_up_swipe_some_height(
                    d=self.d,
                    # 注意: 此处这样设置是为避免上滑过快, 导致first_shop_title_ele元素为空!
                    # 导致进入while not first_shop_title_ele.exists()死循环而退出tb app, 返回系统首页!!
                    swipe_height=self.second_swipe_height/2)
                # TODO 此处可以设置不休眠!! 未刷新出来下次再下滑刷新
                # await async_sleep(.5)  # 等待新返回的list成功显示
                continue

            try:
                # 点击shop title ele进店
                # self.lg.info('++++++ {} ele exists is {}'.format(shop_title, first_shop_title_ele.exists()))
                # self.lg.info('即将点击first_shop_title_ele...')
                first_shop_title_ele.click()
                # TODO 此处可不睡眠, 因为该元素出现较快, atx会等待
                # await async_sleep(3.)
                # 点击粉丝数进入店铺印象页面
                self.d(descriptionMatches='粉丝数\d+.*?', className="android.view.View").click()
                await async_sleep(6.5)

                phone_list = await self._get_shop_phone_num_list()
                address = await self._get_shop_address()
                ii = {
                    'shop_name': shop_title,
                    'phone_list': phone_list,
                    'address': address,
                }
                await self._send_2_tb_shop_info_handle(one_dict=ii)
                res.append(ii)
            except (UiObjectNotFoundError, AssertionError):
                self.lg.error('遇到错误:', exc_info=True)
                await self._back_2_search_page(first_shop_title_ele=first_shop_title_ele)

                continue

            # 返回搜索结果list页面
            # 默认返回前两页会页面混乱
            # await u2_page_back(d=self.d, back_num=2)
            # 改用元素定位来看是否成功返回上层
            await self._back_2_search_page(first_shop_title_ele=first_shop_title_ele)

            await u2_up_swipe_some_height(d=self.d, swipe_height=self.second_swipe_height)
            # await async_sleep(2)  # 等待新返回的list成功显示
            shop_crawl_count += 1

        self.lg.info('--->>> 采集 keyword: {} 对应的shop info 完毕!'.format(keyword))

        return res

    async def _back_2_search_page(self, first_shop_title_ele=None) -> None:
        """
        回退至搜索页
        :return:
        """
        while not self.d(
                resourceId="com.taobao.taobao:id/show_text",
                text=u"销量优先",
                className="android.widget.TextView").exists():
            # 根据销量优先按钮
        # 根据first_shop_title_ele来判断是否已返回搜索页, 长期运行会出错!
        # while not first_shop_title_ele.exists():
            await u2_page_back(d=self.d, back_num=1)
            # 此处休眠, 等待判断元素出现, 不可忽略
            await async_sleep(.3)

    async def _send_2_tb_shop_info_handle(self, one_dict:dict) -> None:
        """
        发送到tb_shop_info_handle
        :param one_dict:
        :return:
        """
        # 将采集结果发往server
        url = 'http://127.0.0.1:9001/tb_shop_info_handle'
        data = dumps([one_dict])
        Requests.get_url_body(
            use_proxy=False,
            method='post',
            url=url,
            data=data, )

        return

    async def _write_tb_ops_txt(self, target_list) -> None:
        """
        写入tb_jb_hot_keyword.txt
        :param target_list:
        :return:
        """
        target_list = list(set(target_list))
        with open(self.tb_ops_file_path, 'a+') as f:
            for item in target_list:
                f.write(item + '\n')
                self.lg.info('write hot key: {}'.format(item))

        return None

    async def _get_shop_phone_num_list(self) -> list:
        """
        获取某店铺的手机号list
        :return:
        """
        phone_exist = self.d(description='服务电话', className="android.view.View").exists()
        assert phone_exist is True, '[-] 无服务电话!!!'
        self.lg.info('[+] 有服务电话!!!')
        phone_num = self.d(descriptionMatches="\d+-\d+|\d+", className="android.view.View") \
            .info.get('contentDescription', '')
        self.lg.info('@' * 10 + ' 服务电话: {}'.format(phone_num))

        return [{
            'phone': phone_num,
        }]

    async def _get_shop_address(self) -> str:
        """
        获取shop所在地
        :return:
        """
        # 由于所在地无法定位, 默认都是北京
        address = '北京'

        # address_exist = self.d(description='所在地', className="android.view.View").exists()
        # if address_exist:
        #     self.lg.info('[+] 所在地存在')
        # else:
        #     self.lg.info('[-] 所在地不存在')

        return address

    async def _get_first_swipe_height_and_second_swipe_height(self) -> tuple:
        """
        获取first_swipe_height and second_swipe_height
        :return:
        """
        # 获取上方全部, 天猫, 店铺, 淘宝经验的parent 元素块的 height
        # h1 = await u2_get_some_ele_height(ele=self.d(className="android.support.v7.app.ActionBar$Tab", instance=3))
        h1 = await u2_get_some_ele_height(ele=self.d(className="android.widget.LinearLayout", instance=18))
        first_swipe_height = h1 / 1000

        # 获取综合排序的元素块 height
        h2 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/sortbtnContainer", className="android.widget.LinearLayout"))

        # 获取店铺label块 height(第一个)
        h3 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/topLayout"))
        # 获取goods 块height
        h4 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/midLayout"))
        # 获取相似块的 height
        h5 = await u2_get_some_ele_height(ele=self.d(resourceId="com.taobao.taobao:id/shop_tag_line"))

        second_swipe_height = (h4 + h5) / 1000
        # self.lg.info('###### first_swipe_height: {}, second_swipe_height: {}, h2: {}'.format(
        #     first_swipe_height,
        #     second_swipe_height,
        #     h2/1000))

        return first_swipe_height, second_swipe_height

    def __del__(self):
        try:
            del self.d
            del self.lg
            del self.loop
            del self.tb_jb_boom_filter
            del self.key_list
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = TaoBaoOps()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())