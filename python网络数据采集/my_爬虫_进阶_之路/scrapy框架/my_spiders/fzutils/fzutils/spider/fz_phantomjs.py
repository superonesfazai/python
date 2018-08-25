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
from ..internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)
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

import re
import gc
from time import sleep
import os
import shutil
from zipfile import ZipFile

__all__ = [
    'MyPhantomjs',
]

PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

# 启动类型
CHROME = 0
PHANTOMJS = 1

# user-agent类型
PC = 0
PHONE = 1

class MyPhantomjs(object):
    def __init__(self, type=PHANTOMJS, load_images=False,
                 executable_path=PHANTOMJS_DRIVER_PATH, logger=None,
                 high_conceal=True, chrome_visualizate=False,
                 user_agent_type=PC):
        '''
        初始化
        :param load_images: 是否加载图片
        :param high_conceal: ip是否高匿
        :param chrome_visualizate: 是否为无头浏览器(针对chrome)
        :param user_agent_type: user-agent类型
        '''
        super(MyPhantomjs, self).__init__()
        self.type = type
        self.high_conceal = high_conceal
        self.executable_path = executable_path
        self.load_images = load_images
        self.chrome_visualizate = chrome_visualizate
        self.my_lg = logger
        self.user_agent_type = user_agent_type
        self._set_driver()

    def _set_driver(self, num_retries=4):
        '''
        初始化self.driver，并且出错重试
        :param num_retries: 重试次数
        :return:
        '''
        try:
            if self.type == PHANTOMJS:
                self._init_phantomjs()
            elif self.type == CHROME:
                self._init_chrome()
            else:
                raise ValueError('type赋值异常!请检查!')
        except Exception as e:
            # _print(msg='初始化phantomjs时出错:', logger=self.my_lg, log_level=2, exception=e)
            if num_retries > 0:
                return self._set_driver(num_retries=num_retries-1)
            else:
                _print(msg='初始化phantomjs时出错:', logger=self.my_lg, log_level=2, exception=e)
                raise e

    def _init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        _print(msg='--->>>初始化phantomjs驱动中<<<---', logger=self.my_lg)
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = self.load_images
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua()
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies

        self.driver = webdriver.PhantomJS(executable_path=self.executable_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 20)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='------->>>初始化完毕<<<-------', logger=self.my_lg)

        return True

    def _init_chrome(self):
        '''
        如果使用chrome请设置page_timeout=30(可用)
        :return:
        '''
        _print(msg='--->>>初始化chrome驱动中<<<---', logger=self.my_lg)
        chrome_options = webdriver.ChromeOptions()
        if not self.chrome_visualizate:
            chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
        chrome_options.add_argument('--disable-gpu')    # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
        # chrome_options.add_argument('window-size=1200x600')   # 设置窗口大小

        # 设置无图模式
        # prefs = {
        #     'profile.managed_default_content_settings.images': 1 if self.load_images else 2,
        # }
        # chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('blink-settings=imagesEnabled={0}'.format('true' if self.load_images else 'false'))

        '''无法打开https解决方案'''
        # 配置忽略ssl错误
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True

        # 设置代理
        ip_object = MyIpPools(high_conceal=self.high_conceal)
        proxy_ip = re.compile(r'https://|http://').sub('', ip_object._get_random_proxy_ip()) if isinstance(ip_object._get_random_proxy_ip(), str) else ''
        if proxy_ip != '':
            chrome_options.add_argument('--proxy-server=http://{0}'.format(proxy_ip))
        else:
            raise AssertionError('给chrome设置代理失败, 异常抛出!')

        # 修改user-agent
        chrome_options.add_argument('--user-agent={0}'.format(get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua()))

        chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])    # 忽视证书错误
        chrome_options.add_argument('--allow-running-insecure-content')

        self.driver = webdriver.Chrome(
            executable_path=self.executable_path,
            chrome_options=chrome_options,
            desired_capabilities=capabilities
        )
        wait = ui.WebDriverWait(self.driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='------->>>初始化完毕<<<-------', logger=self.my_lg)

        return True

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        '''
        给phantomjs切换代理ip
        :return:
        '''
        ip_object = MyIpPools(high_conceal=self.high_conceal)
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

    def use_phantomjs_to_get_url_body(self, url, css_selector='', exec_code='', timeout=20):
        '''
        通过phantomjs来获取url的body
        :param url: 待获取的url
        :return: 字符串类型
        '''
        if self.type == PHANTOMJS:
            change_ip_result = self.from_ip_pool_set_proxy_ip_to_phantomjs()
            if change_ip_result is False:
                if self.from_ip_pool_set_proxy_ip_to_phantomjs() is False:      # 一次切换失败，就尝试第二次
                    return ''
                else: pass
        else:   # 其他类型不动态改变代理
            pass

        try:
            self.driver.set_page_load_timeout(timeout)
        except:
            try: self.driver.set_page_load_timeout(timeout)
            except: return ''

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(timeout)  # 隐式等待和显式等待可以同时使用

            if css_selector != '':
                locator = (By.CSS_SELECTOR, css_selector)
                try:
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.presence_of_element_located(locator))
                except Exception as e:
                    _print(msg='遇到错误: ', logger=self.my_lg, log_level=2, exception=e)
                    return ''
                else:
                    _print(msg='{0}加载完毕'.format(css_selector), logger=self.my_lg)

            # self.driver.save_screenshot('tmp_screen.png')
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
            _print(msg='-->>time out after {0} seconds when loading page'.format(timeout), logger=self.my_lg, log_level=2)
            _print(msg='报错如下: ', logger=self.my_lg, log_level=2, exception=e)
            try:
                self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except Exception: pass        # 内部urllib.error.URLError or WebDriverException
            _print(msg='main_body为空!', logger=self.my_lg, log_level=2)
            main_body = ''

        return main_body

    def get_url_cookies_from_phantomjs_session(self, url, css_selector='', timeout=20):
        '''
        从session中获取cookies
        :param url:
        :return: cookies 类型 str
        '''
        _print(msg='正在获取cookies...请耐心等待...', logger=self.my_lg)
        if self.type == PHANTOMJS:
            change_ip_result = self.from_ip_pool_set_proxy_ip_to_phantomjs()
            if change_ip_result is False:
                if self.from_ip_pool_set_proxy_ip_to_phantomjs() is False:      # 一次切换失败，就尝试第二次
                    return ''
                else: pass
        else:       # 其他类型部动态修改代理
            pass

        try:
            self.driver.set_page_load_timeout(timeout)  # 设置成10秒避免数据出错
        except:
            try: self.driver.set_page_load_timeout(timeout)
            except: return ''

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(timeout)  # 隐式等待和显式等待可以同时使用

            if css_selector != '':
                locator = (By.CSS_SELECTOR, css_selector)
                try:
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.presence_of_element_located(locator))
                except Exception as e:
                    _print(msg='遇到错误: ', logger=self.my_lg, log_level=2, exception=e)
                    return ''
                else:
                    _print(msg='{0}已经加载完毕'.format(css_selector), logger=self.my_lg)

            cookies = self.phantomjs_cookies_2_str(self.driver.get_cookies())
            # _print(msg=str(cookies), logger=self.my_lg)

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            _print(msg='-->>time out after {0} seconds when loading page'.format(timeout), logger=self.my_lg, log_level=2)
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
        html = re.compile('\n|\t|  ').sub('', html)

        return html

    def __del__(self):
        try:
            self.driver.quit()
            del self.my_lg
        except:
            pass
        gc.collect()

class ChromeExtensioner(object):
    '''
    chrome扩展插件: 旨在动态设置代理
        用法:
            chrome_options = webdriver.ChromeOptions()
            ext = ChromeExtensioner()
            chrome_options.add_argument('--load-extension={0}'.format(ext.get_extension_dir_path()))
    '''
    def __init__(self, extension_dir='./extensions', schema='http',
                 host='127.0.0.1', port='8000', username='', passwd=''):
        self.extension_dir = extension_dir
        self.ip_pools_info = {
            'schema': schema,
            'host': host,
            'port': port,
            'username': username,
            'password': passwd,
        }

    def get_extension_dir_path(self):
        '''
        本地先生成插件内容, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        with open(path + '/manifest.json', 'w') as f:
            f.write(self.get_manifest_content())
        with open(path + '/background.js', 'w') as f:
            f.write(self.get_background_content())

        return os.path.abspath(path)

    def get_extension_file_path(self):
        '''
        从.zip文件中读取插件, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}.zip".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            os.remove(path)

        zf = ZipFile(path, mode='w')
        zf.writestr('manifest.json', self.get_manifest_content())
        zf.writestr('background.js', self.get_background_content())
        zf.close()

        return os.path.abspath(path)

    def get_manifest_content(self):
        '''
        mainfest.json内容
        :return:
        '''
        return '''
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        '''

    def get_background_content(self):
        '''
        background.js内容(关键内容)
        :return:
        '''
        return '''
        chrome.proxy.settings.set({{
            value: {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "{0}",
                        host: "{1}",
                        port: {2}
                    }},
                    bypassList: ["foobar.com"]
                }}
            }},
            scope: "regular"
        }}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
            function (details) {{
                return {{
                    authCredentials: {{
                        username: "{3}",
                        password: "{4}"
                    }}
                }};
            }},
            {{ urls: ["<all_urls>"] }},
            [ 'blocking' ]
        );
        '''.format(self.ip_pools_info['schema'], self.ip_pools_info['host'], self.ip_pools_info['port'], self.ip_pools_info['username'], self.ip_pools_info['password'])