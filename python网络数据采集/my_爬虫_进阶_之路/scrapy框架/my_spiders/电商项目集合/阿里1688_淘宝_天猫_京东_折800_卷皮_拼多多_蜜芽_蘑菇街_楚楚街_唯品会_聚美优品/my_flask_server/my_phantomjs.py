# coding:utf-8

'''
@author = super_fazai
@File    : my_phantomjs.py
@Time    : 2017/3/21 15:30
@connect : superonesfazai@gmail.com
'''

from settings import HEADERS
from settings import PHANTOMJS_DRIVER_PATH
from my_ip_pools import MyIpPools

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from scrapy.selector import Selector

from random import randint
import re, gc
from time import sleep

__all__ = [
    'MyPhantomjs',
]

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class MyPhantomjs(object):
    def __init__(self):
        super().__init__()
        self._set_driver()

    def _set_driver(self, num_retries=4):
        '''
        初始化self.driver，并且出错重试
        :param num_retries: 重试次数
        :return:
        '''
        try:
            self.init_phantomjs()
        except Exception as e:
            # print('初始化phantomjs时出错:', e)
            if num_retries > 0:
                return self._set_driver(num_retries=num_retries - 1)
            else:
                print('初始化phantomjs时出错:', e)
                raise e

    def init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, len(HEADERS)-1)]  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH

        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

        return True

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        '''
        给phantomjs切换代理ip
        :return:
        '''
        ip_object = MyIpPools()
        ip_list = ip_object.get_proxy_ip_from_ip_pool().get('http')
        try:
            proxy_ip = ip_list[randint(0, len(ip_list) - 1)]        # 随机一个代理ip
        except Exception:
            # print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
            return False

        # print('------>>>| 正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip))
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
            print('动态切换ip失败')
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
                    print('遇到错误: ', e)
                    return ''
                else:
                    print('{0}已经加载完毕'.format(css_selector))

            if exec_code != '':     # 动态执行代码
                # 执行代码前先替换掉'  '
                try:
                    _ = compile(exec_code.replace('  ', ''), '', 'exec')
                    exec(_)
                except:
                    # self.driver.save_screenshot('tmp_screen.png')
                    print('动态执行代码时出错!')
                    return ''
                # self.driver.save_screenshot('tmp_screen.png')

            main_body = self.driver.page_source
            main_body = re.compile(r'\n').sub('', main_body)
            main_body = re.compile(r'  ').sub('', main_body)
            main_body = re.compile(r'\t').sub('', main_body)
            # print(main_body)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 20 seconds when loading page')
            print('报错如下: ', e)
            try:
                self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except WebDriverException: pass
            print('main_body为空!')
            main_body = ''

        return main_body

    def get_url_cookies_from_phantomjs_session(self, url, css_selector=''):
        '''
        从session中获取cookies
        :param url:
        :return: cookies 类型 str
        '''
        print('正在获取cookies...请耐心等待...')
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
                    print('遇到错误: ', e)
                    return ''
                else:
                    print('{0}已经加载完毕'.format(css_selector))

            cookies = self.phantomjs_cookies_2_str(self.driver.get_cookies())
            # print(cookies)

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 20 seconds when loading page')
            print('报错如下: ', e)
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

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

