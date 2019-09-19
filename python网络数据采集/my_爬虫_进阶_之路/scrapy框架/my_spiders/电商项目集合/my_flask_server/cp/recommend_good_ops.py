# coding:utf-8

'''
@author = super_fazai
@File    : recommend_good_ops.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
    CHROME_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_exceptions import SqlServerConnectionException
from article_spider import ArticleParser

import nest_asyncio
from random import randint
from random import sample as random_sample
from selenium.common.exceptions import NoSuchFrameException

from fzutils.spider.fz_driver import (
    BaseDriver,
    CHROME,
    FIREFOX,
)
from fzutils.spider.selenium_always import *
from fzutils.spider.async_always import *

nest_asyncio.apply()

class RecommendGoodOps(AsyncCrawler):
    """荐好ops"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            log_print=True,
            is_new_loop=False,
            log_save_path=MY_SPIDER_LOGS_PATH + '/荐好/ops/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.request_num_retries = 6
        self.article_type = 'zq'
        self.yx_username = input('请输入yx_username:')
        self.yx_password = input('请输入yx_password:')
        self.lg.info('yx_username: {}, yx_password: {}'.format(
            self.yx_username,
            self.yx_password))
        self.publish_url = 'https://configadmin.yiuxiu.com/Business/Index'
        self.select_sql0 = 'SELECT unique_id FROM dbo.recommend_good_ops_article_id_duplicate_removal'
        self.insert_sql0 = 'INSERT INTO dbo.recommend_good_ops_article_id_duplicate_removal(unique_id, create_time) values(%s, %s)'
        # 敏感标题过滤
        self.sensitive_str_tuple = (
            '走势分析', '股票', 'A股', '上证', '深指', '大盘', '涨停', '跌停', '纳斯达克', '道琼斯',
        )
        self.min_article_id = 0
        self.max_article_id = 0

    async def _fck_run(self):
        # 休眠5分钟s, 避免频繁发!
        # sleep_time = 0.
        sleep_time = 60 * 4.
        self.db_article_id_list = await self.get_db_unique_id_list()
        assert self.db_article_id_list != []
        self.lg.info('db_article_id_list_len: {}'.format(len(self.db_article_id_list)))

        while True:
            if get_shanghai_time().hour == 0:
                # 夜晚休眠
                await async_sleep(60 * 60 * 5)
            else:
                pass
            try:
                await self.auto_publish_articles()
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
            finally:
                self.lg.info('休眠{}s...'.format(sleep_time))
                await async_sleep(sleep_time)

    async def get_db_unique_id_list(self) -> list:
        """
        获取db的unique_id_list
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if not self.sql_cli.is_connect_success:
            raise SqlServerConnectionException

        res = []
        try:
            res = self.sql_cli._select_table(
                sql_str=self.select_sql0,
                logger=self.lg,)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        res = [] if res is None else res

        return [item[0] for item in res]

    async def auto_publish_articles(self):
        """
        自动发布文章
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if not self.sql_cli.is_connect_success:
            raise SqlServerConnectionException
        else:
            pass

        if self.min_article_id == 0\
            or self.max_article_id == 0:
            article_parser = ArticleParser(logger=self.lg)
            article_list = self.loop.run_until_complete(article_parser.get_article_list_by_article_type(
                article_type=self.article_type,))
            try:
                del article_parser
            except:
                pass
            assert article_list != []

            self.min_article_id, self.max_article_id = self.get_latest_max_and_min_artcile_id_from_article_list(
                article_list=article_list,)
            self.lg.info('最新的min_article_id: {}, max_article_id: {}'.format(
                self.min_article_id,
                self.max_article_id,))
        else:
            pass

        # 创建目标集合
        article_list = self.get_zq_own_create_article_id_list(
            min_article_id=self.min_article_id,
            max_article_id=self.max_article_id,)

        # 测试用
        # article_id = '17300123'
        # article_list = [{
        #     'uid': get_uuid3(target_str='{}::{}'.format('zq', article_id)),
        #     'article_type': 'zq',
        #     'article_id': article_id,
        #     'title': '未知',
        #     'article_url': 'https://focus.youth.cn/mobile/detail/id/{}#'.format(article_id),
        # }]

        assert article_list != []
        # pprint(article_list)

        target_article_list = self.get_target_article_list(article_list=article_list)
        if target_article_list == []:
            self.lg.info('待发布的target_article_list为空list, pass!')
            return

        driver = BaseDriver(
            type=CHROME,
            executable_path=CHROME_DRIVER_PATH,
            # 本地老是出错
            # type=FIREFOX,
            # executable_path=FIREFOX_DRIVER_PATH,

            load_images=True,
            logger=self.lg,
            headless=True,
            driver_use_proxy=False,
            ip_pool_type=self.ip_pool_type,
        )
        try:
            self.login_bg(driver=driver)
            self.get_into_recommend_good_manage(driver=driver)
            for item in target_article_list:
                uid = item.get('uid', '')
                title = item.get('title', '')
                article_url = item.get('article_url', '')
                self.lg.info('正在发布文章 title: {}, article_url: {} ...'.format(title, article_url))
                self.publish_one_article(
                    driver=driver,
                    article_url=article_url,)
                # 新增, 以及插入db
                self.db_article_id_list.append(uid)
                self.sql_cli._insert_into_table_2(
                    sql_str=self.insert_sql0,
                    params=(
                        uid,
                        get_shanghai_time(),
                    ),
                    logger=self.lg,)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
        finally:
            try:
                del driver
            except:
                try:
                    del driver
                except:
                    pass

        return

    def get_latest_max_and_min_artcile_id_from_article_list(self, article_list) -> tuple:
        """
        获取最新范围的article_id最大, 最小的article_id(目的动态的自己创建值)
        :return: (int, int)
        """
        latest_article_id_list = []
        for item in article_list:
            # eg: zq是'17296475'
            article_id = item.get('article_id', '')
            if len(article_id) >= 8:
                latest_article_id_list.append(int(article_id))
            else:
                continue

        assert latest_article_id_list != []
        latest_article_id_list = sorted(latest_article_id_list)
        # pprint(latest_article_id_list)

        return (latest_article_id_list[0], latest_article_id_list[-1])

    def get_zq_own_create_article_id_list(self, min_article_id: int, max_article_id: int):
        """
        自己create的article_id_list
        :return:
        """
        article_id_list = [str(article_id) for article_id in range(min_article_id, max_article_id)]
        # 截取10
        article_id_list = random_sample(article_id_list, 10)
        res = [{
            'uid': get_uuid3(target_str='{}::{}'.format('zq', article_id)),
            'article_type': 'zq',
            'title': '未知',
            'article_id': article_id,
            'article_url': 'https://focus.youth.cn/mobile/detail/id/{}#'.format(article_id),
        } for article_id in article_id_list]

        new_res = res

        # 本地不检测了
        # article_parser = ArticleParser(logger=self.lg)
        # # article_list = self.loop.run_until_complete(article_parser.get_article_list_by_article_type(
        # #     article_type=self.article_type,))
        # new_res = []
        # for item in res:
        #     article_url = item.get('article_url', '')
        #     try:
        #         self.lg.info('本地检测url: {}'.format(article_url))
        #         _ = self.loop.run_until_complete(article_parser._parse_article(
        #             article_url=article_url,))
        #         title = _.get('title', '')
        #         assert title != ''
        #         # 标题必须小于等于30
        #         assert len(title) <= 30
        #     except Exception:
        #         continue
        #
        #     item.update({
        #         'title': title,
        #     })
        #     new_res.append(item)

        return new_res

    def get_target_article_list(self, article_list: list) -> list:
        """
        获取未被发布的item
        :return:
        """
        target_article_list = []
        for item in article_list:
            try:
                title = item.get('title', '')
                assert title != ''
                uid = item.get('uid', '')
                assert uid != ''
                article_url = item.get('article_url', '')
                assert article_url != ''
                if uid not in self.db_article_id_list:
                    target_article_list.append(item)
                else:
                    # 已发布的跳过
                    self.lg.info('该文章之前已被发布![where title: {}, url: {}]'.format(title, article_url))
                    continue
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

        return target_article_list

    def login_bg(self, driver: BaseDriver):
        """
        login
        :return:
        """
        self.lg.info('login ...')
        driver.get_url_body(url=self.publish_url)
        driver.find_element(value='input#loginName').send_keys(self.yx_username)
        driver.find_element(value='input#loginPwd').send_keys(self.yx_password)
        driver.find_element(value='button#subbut').click()
        sleep(5.)
        self.lg.info('login over!')

    def get_into_recommend_good_manage(self, driver: BaseDriver):
        """
        进入荐好管理
        :param driver:
        :return:
        """
        driver.find_element(value='span.nav-label').click()
        driver.find_element(value='a.J_menuItem').click()

    def publish_one_article(self, driver: BaseDriver, article_url: str):
        """
        发布一篇图文
        :param article_url:
        :return:
        """
        try:
            # 切换到目标iframe(用index有时候不准, pass)
            # driver.switch_to_frame(frame_reference=1)

            iframe_ele_list = driver.find_elements(by=By.TAG_NAME, value='iframe')
            # pprint(iframe_ele_list)
            assert iframe_ele_list != []
            target_iframe_ele = iframe_ele_list[1] if len(iframe_ele_list) > 1 else iframe_ele_list[0]
            driver.switch_to_frame(frame_reference=target_iframe_ele)
        except (NoSuchFrameException,) as e:
            # 没匹配到frame(可能是原先就在目标iframe, eg: title过长的, 再切回iframe, 但是iframe_ele_list为0)
            raise e

        # 清空输入框
        input_box_ele = driver.find_element(value='input#SnatchUrl')
        input_box_ele.clear()
        # 输入待采集地址
        input_box_ele.send_keys(article_url)
        # 点击采集按钮
        driver.find_elements(value='span.input-group-btn button')[0].click()
        self.wait_for_delete_img_appear(driver=driver)
        # 获取输入框的值
        title = driver.find_element(value='input#RecommendName').get_attribute('value')
        if self.filter_title(title=title):
            raise AssertionError('该标题包含敏感词汇, 退出发布!')
        else:
            pass
        if isinstance(title, str) and len(title) > 30:
            # 标题过长则return, 不发布
            self.lg.info('@@@ title 标题过长, 无法发布!! 跳过!')
            return
        else:
            pass

        # 点击发布按钮
        driver.find_elements(value='span.input-group-btn button')[1].click()

        # 切换至主页面
        driver.switch_to_default_content()
        # 填写被发布人
        random_phone = self.get_random_phone()
        driver.find_element(value='input.layui-layer-input').send_keys(random_phone)
        # 点击确定
        driver.find_element(value='a.layui-layer-btn0').click()

        self.lg.info('url: {} 发布成功!'.format(article_url))
        # 发布成功, 等待5.秒, 等待页面元素置空
        sleep(5.)

        return

    def filter_title(self, title) -> bool:
        """
        过滤敏感title
        :param title:
        :return: True 包含敏感 | False 不包含
        """
        res = False
        if isinstance(title, str):
            self.lg.info('title: {}'.format(title))
            for item in self.sensitive_str_tuple:
                if item in title:
                    return True
                else:
                    continue
        else:
            pass

        return res

    @fz_set_timeout(seconds=25)
    def wait_for_delete_img_appear(self, driver: BaseDriver):
        """
        直至出现图片, 超时退出(并且避免发布无图文章)
        :return:
        """
        while True:
            delete_btn_text = driver.find_element(value='div.deletebut').text
            # self.lg.info('delete_btn_text: {}'.format(delete_btn_text))
            if delete_btn_text == '删除':
                break
            else:
                continue

        self.lg.info('该url采集完毕!')

    def get_random_phone(self) -> int:
        """
        随机个手机号
        :return:
        """
        phone_list = []
        with open('../tools/phone.txt', 'r') as f:
            for line in f:
                try:
                    phone_list.append(int(line.replace('\n', '')))
                except Exception:
                    continue

        # pprint(phone_list)
        random_phone = phone_list[randint(0, len(phone_list) - 1)]
        self.lg.info('random_phone: {}'.format(random_phone))

        return random_phone

    def __del__(self):
        try:
            del self.lg
            del self.loop
            del self.db_article_id_list
            del self.publish_url
        except:
            pass
        collect()

def main():
    _ = RecommendGoodOps()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()