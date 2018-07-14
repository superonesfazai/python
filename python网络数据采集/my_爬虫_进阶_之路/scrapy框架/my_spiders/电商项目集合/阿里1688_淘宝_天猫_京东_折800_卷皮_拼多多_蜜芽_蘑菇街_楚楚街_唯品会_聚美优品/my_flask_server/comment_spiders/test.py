# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''
import sys, json, re
sys.path.append('..')
from pprint import pprint

from fzutils.internet_utils import _get_url_contain_params
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs

def _init_chrome(is_headless=True, is_pic=True, is_proxy=True):
    '''
    如果使用chrome请设置page_timeout=30
    :return:
    '''
    from selenium.webdriver.support import ui
    from selenium import webdriver

    CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
    print('--->>>初始化chrome驱动中<<<---')
    chrome_options = webdriver.ChromeOptions()
    if is_headless:
        chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
    # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.

    # chrome_options.add_argument('window-size=1200x600')   # 设置窗口大小

    # 设置无图模式
    if is_pic:
        prefs = {
            'profile.managed_default_content_settings.images': 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 设置代理
    if is_proxy:
        ip_object = MyIpPools()
        proxy_ip = ip_object._get_random_proxy_ip().replace('http://', '') if isinstance(ip_object._get_random_proxy_ip(), str) else ''
        if proxy_ip != '':
            chrome_options.add_argument('--proxy-server={0}'.format(proxy_ip))

    '''无法打开https解决方案'''
    # 配置忽略ssl错误
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    # 修改user-agent
    chrome_options.add_argument('--user-agent={0}'.format(user_agent))

    # 忽视证书错误
    chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        chrome_options=chrome_options,
        desired_capabilities=capabilities
    )
    wait = ui.WebDriverWait(driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
    print('------->>>初始化完毕<<<-------')

    return driver

from time import sleep

class test():
    def __init__(self, goods_id):
        self.driver = _init_chrome(is_headless=False, is_pic=False, is_proxy=False)
        self.goods_id = goods_id

    def run(self):
        try:
            self.driver.set_page_load_timeout(20)  # 设置成10秒避免数据出错
        except:
            try: self.driver.set_page_load_timeout(20)
            except: return ''
        self.driver.implicitly_wait(20)  # 隐式等待和显式等待可以同时使用

        tmp_url = 'https://m.1688.com/page/offerRemark.htm?offerId=' + str(self.goods_id)
        self.driver.get(tmp_url)

        try:
            from selenium.webdriver.common.keys import Keys
            from selenium.common.exceptions import NoSuchElementException   # 没有找到元素的异常


            try:
                # self.driver.find_element_by_css_selector('div.tab-item:nth-child(2)').click()
                self.driver.find_elements_by_css_selector('div.tab-item')[1].click()

                # self.driver.find_elements_by_link_text('四五星').click()
                # _ = self.driver.find_element_by_css_selector('div.tab-item:nth-child(2)')
                # print(_.is_displayed())
                # _.send_keys(Keys.ENTER)
            except NoSuchElementException as e:
                print(e)
                return None

            _text = str(self.driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').text)
            print(_text)
            # if _text == '四五星(0)':
            assert _text != '四五星(0)', 'my assert error!'  # 通过断言来跳过执行下面的代码
            sleep(3)
            # 向下滚动10000像素
            js = 'document.body.scrollTop=10000'
            self.driver.execute_script(js)  # 每划一次，就刷6条
            sleep(4)
        except Exception as e:
            print(e)
        self.driver.save_screenshot('tmp_screen.png')

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass


goods_id = '1285007747'
_ = test(goods_id)
_.run()

sleep(60)
del _