# coding:utf-8

'''
@author = super_fazai
@File    : zhihu_pc_login.py
@connect : superonesfazai@gmail.com
'''

"""
知乎pc版, 二维码模拟登陆
"""

from scrapy.selector import Selector
from time import sleep
from gc import collect
from pprint import pprint
from requests import get
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
import re

from fzutils.spider.fz_driver import (
    CHROME,
    BaseDriver,
    FIREFOX,
    PC,)
from fzutils.ip_pools import fz_ip_pool
from fzutils.internet_utils import get_random_pc_ua

# chrome驱动
CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
# phantomjs驱动
PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
# firefox驱动
FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

class ZhiHuLogin(object):
    def __init__(self):
        self._init_driver()
        self._set_headers()

    def _init_driver(self):
        self.driver = BaseDriver(
            type=FIREFOX,
            executable_path=FIREFOX_DRIVER_PATH,
            user_agent_type=PC,
            load_images=True,
            driver_use_proxy=True,
            headless=False,
            ip_pool_type=fz_ip_pool,
        ).driver

    def _set_headers(self):
        self.headers = {
            'authority': 'www.zhihu.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        
    def is_driver_low_version_error(self, body) -> bool:
        '''
        driver版本过低, 则重启再试
        :param body:
        :return:
        '''
        while True:     # 无限重试, 直到成功!
            driver_low_version_error = re.compile('你正在使用的浏览器版本过低').findall(body)
            if driver_low_version_error == []:
                break
            else:
                print('提示浏览器版本过低!')
                collect()
                self._init_driver()
                self.driver.get("https://www.zhihu.com/signup")
                sleep(3)
                body = self.driver.page_source
                continue

        return True

    def _get_login_cookies(self):
        '''
        :return:
        '''
        def _scan_qrcode(qrcode_url):
            '''扫码'''
            print('download qrcode ...')
            # local 保存qrcode
            qrcode_body = get(qrcode_url, headers=self.headers).content
            with open('./images/qrcode.jpg', 'wb') as f:
                f.write(qrcode_body)

            qrcode_img = Image.open('./images/qrcode.jpg')
            qrcode_img.show()

            before_url = self.driver.current_url
            print('wait to scan qrcode ...')
            sleep(15)

            while self.driver.current_url != before_url:
                print('扫码登陆成功!')
                print('-' * 100)
                break

            return True

        self.driver.get("https://www.zhihu.com/signup")
        sleep(3)
        self.is_driver_low_version_error(body=self.driver.page_source)

        try:
            self.driver.find_element_by_css_selector('div.SignContainer-switch span').click()
            sleep(1)
            self.driver.find_element_by_css_selector('span.Login-qrcode button').click()
            sleep(2)
            qrcode_url = Selector(text=self.driver.page_source).css('div.Qrcode-img img ::attr("src")').extract_first()
            print('获取到的二维码地址为:{}'.format(qrcode_url))
            print('wait to scan qrcode ...')

            # 扫码
            # scan_res = _scan_qrcode(qrcode_url=qrcode_url)
        except (NoSuchElementException, IndexError) as e:
            print(e)

        # TODO 出现: Missing argument grant_type
        sleep(20)
        cookies = self.driver.get_cookies()
        pprint(cookies)

        return cookies

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        collect()

# e.currentTarget.disabled
# r.handleClick
# v3/oauth/sign_in

if __name__ == "__main__":
    _ = ZhiHuLogin()
    _._get_login_cookies()
    sleep(2*60)
