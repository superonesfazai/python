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
import time
from pprint import pprint
import gc
import pytz
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from time import sleep

import sys
sys.path.append('..')

from settings import HEADERS, BASE_SESSION_ID, MAX_SESSION_ID
from settings import PHANTOMJS_DRIVER_PATH
from zhe_800_parse import Zhe800Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

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
            'Host': 'zhe800.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

        self.init_phantomjs()   # 初始化phantomjs

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        base_session_id = BASE_SESSION_ID
        while base_session_id < MAX_SESSION_ID:
            print('待抓取的session_id为: ', base_session_id)
            tmp_url = 'https://zapi.zhe800.com/zhe800_n_api/xsq/get?sessionId={0}&page=1&per_page=1000'.format(
                str(base_session_id),
            )

            body = self.get_url_body(url=tmp_url)

            body_1 = re.compile(r'<pre.*?>(.*)</pre>').findall(body)
            if body_1 != []:
                data = body_1[0]
                data = json.loads(data)
                # pprint(data)

                if data.get('status') == 0:     # session_id不存在
                    print('该session_id不存在，此处跳过')
                    pass

                else:                           # 否则session_id存在
                    begin_times = data.get('begin_times')[0]
                    print('秒杀时间为: ', begin_times)
                    begin_times_timestamp = int(time.mktime(time.strptime(begin_times, '%Y-%m-%d %H:%M:%S'))) # 将如 "2017-09-28 10:00:00"的时间字符串转化为时间戳，然后再将时间戳取整

                    if self.is_recent_time(timestamp=begin_times_timestamp):    # 说明秒杀日期合法
                        data = data.get('jsons', [])
                        if data != []:  # 否则说明里面有数据
                            miaosha_goods_list = self.get_miaoshao_goods_info_list(data=data)

                            zhe_800 = Zhe800Parse()
                            my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                            if my_pipeline.is_connect_success:
                                db_goods_id_list = [item[0] for item in list(my_pipeline.select_zhe_800_xianshimiaosha_all_goods_id())]
                                for item in miaosha_goods_list:
                                    if item.get('zid', '') in db_goods_id_list:
                                        print('该goods_id已经存在于数据库中, 此处跳过')
                                        pass
                                    else:
                                        tmp_url = 'https://shop.zhe800.com/products/' + str(item.get('zid', ''))
                                        goods_id = zhe_800.get_goods_id_from_url(tmp_url)

                                        zhe_800.get_goods_data(goods_id=goods_id)
                                        goods_data = zhe_800.deal_with_data()

                                        if goods_data == {}:    # 返回的data为空则跳过
                                            pass
                                        else:       # 否则就解析并且插入
                                            goods_data['stock_info'] = item.get('stock_info')
                                            goods_data['goods_id'] = str(item.get('zid'))
                                            goods_data['spider_url'] = tmp_url
                                            goods_data['username'] = '18698570079'
                                            goods_data['price'] = item.get('price')
                                            goods_data['taobao_price'] = item.get('taobao_price')
                                            goods_data['sub_title'] = item.get('sub_title')
                                            # goods_data['is_baoyou'] = item.get('is_baoyou')
                                            goods_data['miaosha_time'] = item.get('miaosha_time')
                                            goods_data['session_id'] = str(base_session_id)

                                            # print(goods_data)
                                            zhe_800.insert_into_zhe_800_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                                            sleep(.7)   # 放慢速度

                                sleep(5)
                            else:
                                pass
                            try:
                                del zhe_800
                            except:
                                pass
                            gc.collect()

                        else:       # 说明这个sessionid没有数据
                            print('该sessionid没有相关key为jsons的数据')
                            # return {}
                            pass
                    else:
                        pass

            else:
                print('获取到的data为空!')
                # return {}
                pass
            base_session_id += 2

    def init_phantomjs(self):
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

    def get_url_body(self, url):
        '''
        返回url的html代码
        :param url: 待抓取的url
        :return: str
        '''
        self.from_ip_pool_set_proxy_ip_to_phantomjs()
        self.driver.set_page_load_timeout(15)  # 设置成15秒避免数据出错

        try:
            self.driver.get(url)
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

        return body

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            # pprint(item)
            tmp = {}
            # 秒杀开始时间和结束时间
            tmp['miaosha_time'] = {
                'miaosha_begin_time': self.timestamp_to_regulartime(int(str(item.get('begin_time'))[0:10])),
                'miaosha_end_time': self.timestamp_to_regulartime(int(str(item.get('end_time'))[0:10])),
            }

            # 折800商品地址
            tmp['zid'] = item.get('zid')
            # 是否包邮
            # tmp['is_baoyou'] = item.get('is_baoyou', 0)
            # 限时秒杀的库存信息
            tmp['stock_info'] = {
                'activity_stock': item.get('xianshi', {}).get('activity_stock', 0),  # activity_stock为限时抢的剩余数量
                'stock': item.get('xianshi', {}).get('stock', 0),  # stock为限时秒杀的总库存
            }
            # 原始价格
            tmp['price'] = item.get('xianshi', {}).get('list_price')
            # 秒杀的价格, float类型
            tmp['taobao_price'] = item.get('xianshi', {}).get('price')
            # 子标题
            tmp['sub_title'] = item.get('xianshi', {}).get('description', '')
            miaosha_goods_list.append(tmp)
            # pprint(miaosha_goods_list)

        return miaosha_goods_list

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestamp: 时间戳
        :return: True or False
        '''
        time_1 = int(timestamp)
        time_2 = time.time()  # 当前的时间戳
        time_1 = time.localtime(time_1)
        time_2 = time.localtime(time_2)
        if time_1.tm_year == time_2.tm_year:
            if time_1.tm_mon >= time_2.tm_mon:  # 如果目标时间的月份时间 >= 当前月份(月份合法, 表示是当前月份或者是今年其他月份)
                if time_1.tm_mday >= time_2.tm_mday-2:  # 这样能抓到今天的前两天的信息
                    if time_1.tm_hour >= 8 and time_1.tm_hour <= 16:    # 规定到8点到16点的商品信息
                        print('合法时间')
                        # diff_days = abs(time_1.tm_mday - time_2.tm_mday)
                        return True
                    else:
                        print('该小时在8点到16点以外，此处不处理跳过')
                        return False
                else:
                    print('该日时间已过期, 此处跳过')
                    return False
            else:  # 月份过期
                print('该月份时间已过期，此处跳过')
                return False

        else:
            print('非本年度的限时秒杀时间，此处跳过')
            return False

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

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    zhe_800_spike = Zhe800Spike()
    zhe_800_spike.get_spike_hour_goods_info()
