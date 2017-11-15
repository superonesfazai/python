# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_spike.py
@Time    : 2017/11/14 13:54
@connect : superonesfazai@gmail.com
'''

from random import randint
import json
import requests
import re
from pprint import pprint
import gc
import pytz
from selenium import webdriver
import selenium.webdriver.support.ui as ui

import sys
sys.path.append('..')

from settings import HEADERS
from settings import PHANTOMJS_DRIVER_PATH

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class Zhe800Spike(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.zhe800.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        '''
        研究发现, 必须以浏览器的形式进行访问才能返回需要的东西
        常规requests模拟请求会被服务器过滤, 并返回请求过于频繁的无用页面
        '''
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH

        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def get_spike_goods_info(self):
        '''
        模拟构造得到data的url
        :return:
        '''
        tmp_url = 'https://zapi.zhe800.com/zhe800_n_api/xsq/get?sessionId=13688&page=1&per_page=1000'

        self.from_ip_pool_set_proxy_ip_to_phantomjs()
        self.driver.set_page_load_timeout(15)  # 设置成15秒避免数据出错

        try:
            self.driver.get(tmp_url)
            self.driver.implicitly_wait(15)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 15 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass
        body = self.driver.page_source
        body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        ip_list = self.get_proxy_ip_from_ip_pool().get('http')
        proxy_ip = ''
        try:
            proxy_ip = ip_list[randint(0, len(ip_list) - 1)]        # 随机一个代理ip
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
        # print('------>>>| 正在使用的代理ip: {} 进行爬取... |<<<------'.format(proxy_ip))
        proxy_ip = re.compile(r'http://').sub('', proxy_ip)     # 过滤'http://'
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
            pass

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            if item[2] > 7:
                tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
                result_ip_list['http'].append(tmp_url)
            else:
                delete_url = 'http://127.0.0.1:8000/delete?ip='
                delete_info = requests.get(delete_url + item[0])
        # pprint(result_ip_list)
        return result_ip_list

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    zhe_800_spike = Zhe800Spike()
    zhe_800_spike.get_spike_goods_info()
    # zhe_800_url = input('请输入待爬取的折800商品地址: ')
    # zhe_800_url.strip('\n').strip(';')
    # goods_id = zhe_800_spike.get_goods_id_from_url(zhe_800_url)
    # data = zhe_800_spike.get_goods_data(goods_id=goods_id)
    # zhe_800_spike.deal_with_data()
