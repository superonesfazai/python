# coding:utf-8

'''
@author = super_fazai
@File    : recommend_good_ops.py
@connect : superonesfazai@gmail.com
'''

"""
荐好ops
"""

from sys import path as sys_path
sys_path.append('..')

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
    CHROME_DRIVER_PATH,
)
from article_spider import ArticleParser

import nest_asyncio
from random import randint

from fzutils.spider.fz_driver import (
    BaseDriver,
    CHROME,
)
from fzutils.spider.async_always import *

nest_asyncio.apply()

class RecommendGoodOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            log_print=True,
            is_new_loop=False,
            log_save_path=MY_SPIDER_LOGS_PATH + '/荐好/ops/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.request_num_retries = 6
        self.yx_username = input('请输入yx_username:')
        self.yx_password = input('请输入yx_passwd:')
        self.lg.info('yx_username: {}, yx_passwd: {}'.format(
            self.yx_username,
            self.yx_password))
        self.publish_url = 'https://configadmin.yiuxiu.com/Business/Index'

    async def auto_publish_articles(self):
        """
        自动发布文章
        :return:
        """
        article_parser = ArticleParser(logger=self.lg)
        article_list = self.loop.run_until_complete(article_parser.get_article_list_by_article_type(
            article_type='zq',))
        assert article_list != []
        pprint(article_list)
        try:
            del article_parser
        except:
            pass

        driver = BaseDriver(
            type=CHROME,
            load_images=True,
            executable_path=CHROME_DRIVER_PATH,
            logger=self.lg,
            headless=False,
            driver_use_proxy=False,
            ip_pool_type=self.ip_pool_type,
        )
        self.login_bg(driver=driver)
        self.get_into_recommend_good_manage(driver=driver)
        for item in article_list:
            try:
                title = item.get('title', '')
                assert title != ''
                article_url = item.get('article_url', '')
                assert article_url != ''
            except AssertionError:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            self.lg.info('发布ing title: {}, article_url: {}'.format(title, article_url))
            self.publish_one_article(
                driver=driver,
                article_url=article_url)

        try:
            del driver
        except:
            pass

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
        sleep(3.5)
        self.lg.info('login over!')

    def get_into_recommend_good_manage(self, driver: BaseDriver):
        """
        进入荐好管理
        :param driver:
        :return:
        """
        driver.find_element(value='span.nav-label').click()
        driver.find_element(value='a.J_menuItem').click()
        # 切换到目标iframe
        driver.switch_to_frame(frame_reference=1)

    def publish_one_article(self, driver: BaseDriver, article_url: str):
        """
        发布一篇图文
        :param article_url:
        :return:
        """
        # 输入待采集地址
        driver.find_element(value='input#SnatchUrl').send_keys(article_url)
        # 点击采集按钮
        driver.find_elements(value='span.input-group-btn button')[0].click()
        self.wait_for_delete_img_appear()
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
        sleep(1.5)

        return

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
        except:
            pass
        collect()

def main():
    _ = RecommendGoodOps()
    loop = get_event_loop()
    loop.run_until_complete(_.auto_publish_articles())

if __name__ == '__main__':
    main()