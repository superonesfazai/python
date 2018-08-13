# coding:utf-8

'''
@author = super_fazai
@File    : my_phantomjs.py
@Time    : 2017/3/21 15:30
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from ..ip_pools import MyIpPools
from ..internet_utils import get_random_pc_ua
from ..common_utils import _print

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
)

from scrapy.selector import Selector

from random import randint
import re
import gc
from time import sleep

__all__ = [
    'MyPhantomjs',
]

PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class MyPhantomjs(object):
    def __init__(self, load_images=False, executable_path=EXECUTABLE_PATH, logger=None):
        '''
        初始化
        :param load_images: 是否加载图片
        '''
        super(MyPhantomjs, self).__init__()
        self.my_lg = logger
        self._set_driver(load_images, executable_path)

    def _set_driver(self, load_images, executable_path, num_retries=4):
        '''
        初始化self.driver，并且出错重试
        :param load_images: 是否加载图片
        :param num_retries: 重试次数
        :param executable_path: 执行路径
        :return:
        '''
        try:
            self.init_phantomjs(load_images, executable_path)
        except Exception as e:
            # _print(msg='初始化phantomjs时出错:', logger=self.my_lg, log_level=2, exception=e)
            if num_retries > 0:
                return self._set_driver(load_images, executable_path, num_retries=num_retries - 1)
            else:
                _print(msg='初始化phantomjs时出错:', logger=self.my_lg, log_level=2, exception=e)
                raise e

    def init_phantomjs(self, load_images, executable_path):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        _print(msg='--->>>初始化phantomjs驱动中<<<---', logger=self.my_lg)
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = load_images
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua()  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies

        self.driver = webdriver.PhantomJS(executable_path=executable_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='------->>>初始化完毕<<<-------', logger=self.my_lg)

        return True

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        '''
        给phantomjs切换代理ip
        :return:
        '''
        ip_object = MyIpPools()
        proxy_ip = ip_object._get_random_proxy_ip()
        if not proxy_ip:
            return False

        # _print(msg='------>>>| 正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip), logger=self.my_lg)
        proxy_ip = re.compile(r'https://|http://').sub('', proxy_ip)
        proxy_ip = proxy_ip.split(':')                          # 切割成['xxxx', '端口']

        try:
            tmp_js = {
                'script': 'phantom.setProxy({}, {});'.format(proxy_ip[0], proxy_ip[1]),
                'args': []
            }
            self.driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
            self.driver.execute('executePhantomScript', tmp_js)

        except Exception:
            _print(msg='动态切换ip失败', logger=self.my_lg, log_level=2)
            return False

        return True

    def use_phantomjs_to_get_url_body(self, url, css_selector='', exec_code=''):
        '''
        通过phantomjs来获取url的body
        :param url: 待获取的url
        :return: 字符串类型
        '''
        change_ip_result = self.from_ip_pool_set_proxy_ip_to_phantomjs()
        if change_ip_result is False:
            if self.from_ip_pool_set_proxy_ip_to_phantomjs() is False:      # 一次切换失败，就尝试第二次
                return ''
            else: pass

        try:
            self.driver.set_page_load_timeout(20)  # 设置成10秒避免数据出错
        except:
            try: self.driver.set_page_load_timeout(20)
            except: return ''

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(20)  # 隐式等待和显式等待可以同时使用

            if css_selector != '':
                locator = (By.CSS_SELECTOR, css_selector)
                try:
                    WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
                except Exception as e:
                    _print(msg='遇到错误: ', logger=self.my_lg, log_level=2, exception=e)
                    return ''
                else:
                    _print(msg='{0}加载完毕'.format(css_selector), logger=self.my_lg)

            if exec_code != '':     # 动态执行代码
                # 执行代码前先替换掉'  '
                try:
                    _ = compile(exec_code.replace('  ', ''), '', 'exec')
                    exec(_)
                except Exception as e:
                    # self.driver.save_screenshot('tmp_screen.png')
                    # _print(exception=e, logger=self.my_lg)
                    _print(msg='动态执行代码时出错!', logger=self.my_lg, log_level=2)
                    return ''
                # self.driver.save_screenshot('tmp_screen.png')

            main_body = self._wash_html(self.driver.page_source)
            # _print(msg=str(main_body), logger=self.my_lg)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            _print(msg='-->>time out after 20 seconds when loading page', logger=self.my_lg, log_level=2)
            _print(msg='报错如下: ', logger=self.my_lg, log_level=2, exception=e)
            try:
                self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except WebDriverException or Exception: pass        # 内部urllib.error.URLError
            _print(msg='main_body为空!', logger=self.my_lg, log_level=2)
            main_body = ''

        return main_body

    def get_url_cookies_from_phantomjs_session(self, url, css_selector=''):
        '''
        从session中获取cookies
        :param url:
        :return: cookies 类型 str
        '''
        _print(msg='正在获取cookies...请耐心等待...', logger=self.my_lg)
        change_ip_result = self.from_ip_pool_set_proxy_ip_to_phantomjs()
        if change_ip_result is False:
            if self.from_ip_pool_set_proxy_ip_to_phantomjs() is False:      # 一次切换失败，就尝试第二次
                return ''
            else: pass

        try:
            self.driver.set_page_load_timeout(20)  # 设置成10秒避免数据出错
        except:
            try: self.driver.set_page_load_timeout(20)
            except: return ''

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(20)  # 隐式等待和显式等待可以同时使用

            if css_selector != '':
                locator = (By.CSS_SELECTOR, css_selector)
                try:
                    WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
                except Exception as e:
                    _print(msg='遇到错误: ', logger=self.my_lg, log_level=2, exception=e)
                    return ''
                else:
                    _print(msg='{0}已经加载完毕'.format(css_selector), logger=self.my_lg)

            cookies = self.phantomjs_cookies_2_str(self.driver.get_cookies())
            # _print(msg=str(cookies), logger=self.my_lg)

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            _print(msg='-->>time out after 20 seconds when loading page', logger=self.my_lg, log_level=2)
            _print(msg='报错如下: ', logger=self.my_lg, log_level=2, exception=e)
            try:
                self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except WebDriverException: pass
            cookies = ''

        return cookies

    def phantomjs_cookies_2_str(self, cookies):
        '''
        从phantomjs的cookies中获取到规范格式的cookies字符串
        :param cookies:
        :return: '' 表示获取失败 | str
        '''
        if cookies == []:
            return ''

        tmp_cookies = {}
        cookies_str = ''
        for item in cookies:
            tmp_cookies[item.get('name', '')] = item.get('value', '')

        # pprint(tmp_cookies)
        for key, value in tmp_cookies.items():
            cookies_str += key + '=' + value + ';'

        return cookies_str

    def _wash_html(self, html):
        '''
        清洗html
        :param html:
        :return:
        '''
        html = re.compile(r'\n').sub('', html)
        html = re.compile(r'  ').sub('', html)
        html = re.compile(r'\t').sub('', html)

        return html

    def __del__(self):
        try:
            self.driver.quit()
            del self.my_lg
        except:
            pass
        gc.collect()

# from logging import INFO, ERROR
# from fzutils.time_utils import get_shanghai_time
# from fzutils.log_utils import set_logger
#
# my_lg = set_logger(
#     log_file_name='/Users/afa/myFiles/my_spider_logs/电商项目' + '/my_spiders_server/day_by_day/' + str(get_shanghai_time())[0:10] + '.txt',
#     console_log_level=INFO,
#     file_log_level=ERROR
# )
#
# _ = MyPhantomjs(logger=my_lg)
# del _
