# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_spike.py
@Time    : 2017/11/25 15:22
@connect : superonesfazai@gmail.com
'''

from random import randint
import json
import requests
import re
from pprint import pprint
import gc
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from time import sleep

import sys
sys.path.append('..')

from pinduoduo_parse import PinduoduoParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import IS_BACKGROUND_RUNNING, PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST, PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST

from settings import PHANTOMJS_DRIVER_PATH, PINDUODUO_SLEEP_TIME
import datetime

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.ip_pools import MyIpPools

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class PinduoduoSpike(object):
    def __init__(self):
        self._set_headers()
        self.init_phantomjs()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.juanpi.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        all_miaosha_goods_list = self.get_all_miaosha_goods_list()
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

        pinduoduo = PinduoduoParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            sql_str = r'select goods_id, miaosha_time from dbo.pinduoduo_xianshimiaosha where site_id=16'
            if my_pipeline._select_table(sql_str=sql_str) is None:
                db_goods_id_list = []
            else:
                db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]

            for item in all_miaosha_goods_list:
                '''
                注意: 明日8点半抓取到的是页面加载中返回的是空值
                '''
                if item.get('goods_id') != 'None':    # 跳过goods_id为'None'
                    if item.get('goods_id', '') in db_goods_id_list:
                        print('该goods_id已经存在于数据库中, 此处跳过')
                        pass
                    else:
                        tmp_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=' + item.get('goods_id')
                        pinduoduo.get_goods_data(goods_id=item.get('goods_id'))
                        goods_data = pinduoduo.deal_with_data()

                        # print(goods_data)
                        if goods_data == {}:  # 返回的data为空则跳过
                            print('得到的goods_data为空值，此处先跳过，下次遍历再进行处理')
                            # sleep(3)
                            pass

                        else:  # 否则就解析并插入
                            goods_data['stock_info'] = item.get('stock_info')
                            goods_data['goods_id'] = item.get('goods_id')
                            goods_data['spider_url'] = tmp_url
                            goods_data['username'] = '18698570079'
                            goods_data['price'] = item.get('price')  # 秒杀前的原特价
                            goods_data['taobao_price'] = item.get('taobao_price')  # 秒杀价
                            goods_data['sub_title'] = item.get('sub_title', '')
                            goods_data['miaosha_time'] = item.get('miaosha_time')
                            goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item.get('miaosha_time'))

                            if item.get('stock_info').get('activity_stock') <= 2:
                                # 实时秒杀库存小于等于2时就标记为 已售罄
                                print('该秒杀商品已售罄...')
                                goods_data['is_delete'] = 1

                            pinduoduo.insert_into_pinduoduo_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        sleep(PINDUODUO_SLEEP_TIME)

                else:
                    print('该goods_id为"None", 此处跳过')
                    pass
            sleep(5)

        else:
            pass
        try:
            del pinduoduo
        except:
            pass
        gc.collect()

    def get_all_miaosha_goods_list(self):
        # 今日秒杀
        tmp_url = 'http://apiv4.yangkeduo.com/api/spike/v2/list/today?page=0&size=2000'
        print('待爬取的今日限时秒杀数据的地址为: ', tmp_url)
        # today_data = self.get_url_body(tmp_url=tmp_url)
        today_data = self.phantomjs_get_url_body(tmp_url=tmp_url)
        today_data = self.json_to_dict(tmp_data=today_data)
        sleep(PINDUODUO_SLEEP_TIME)

        # 明日的秒杀
        tmp_url_2 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/tomorrow?page=0&size=2000'
        print('待爬取的明日限时秒杀数据的地址为: ', tmp_url_2)
        # tomorrow_data = self.get_url_body(tmp_url=tmp_url_2)
        tomorrow_data = self.phantomjs_get_url_body(tmp_url=tmp_url_2)
        tomorrow_data = self.json_to_dict(tmp_data=tomorrow_data)
        sleep(PINDUODUO_SLEEP_TIME)

        # 未来的秒杀
        tmp_url_3 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/all_after?page=0&size=2000'
        print('待爬取的未来限时秒杀数据的地址为: ', tmp_url_3)
        # all_after_data = self.get_url_body(tmp_url=tmp_url_3)
        all_after_data = self.phantomjs_get_url_body(tmp_url=tmp_url_3)
        all_after_data = self.json_to_dict(tmp_data=all_after_data)
        sleep(PINDUODUO_SLEEP_TIME)

        if today_data != []:
            today_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=today_data)
            # print('今日限时秒杀的商品list为: ', today_miaosha_goods_list)

        else:
            today_miaosha_goods_list = []
            print('今日秒杀的items为[]')

        if tomorrow_data != []:
            tomorrow_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=tomorrow_data)
            # print('明日限时秒杀的商品list为: ', tomorrow_miaosha_goods_list)

        else:
            tomorrow_miaosha_goods_list = []
            print('明日秒杀的items为[]')

        if all_after_data != []:
            all_after_miaosha_goods_list = self.get_miaoshao_goods_info_list(data=all_after_data)
            # print('未来限时秒杀的商品list为: ', all_after_miaosha_goods_list)

        else:
            all_after_miaosha_goods_list = []
            print('未来秒杀的items为[]')

        all_miaosha_goods_list = today_miaosha_goods_list
        for item in tomorrow_miaosha_goods_list:
            all_miaosha_goods_list.append(item)
        for item in all_after_miaosha_goods_list:
            all_miaosha_goods_list.append(item)
        print('当前所有限时秒杀商品list为: ', all_miaosha_goods_list)

        return all_miaosha_goods_list

    def get_miaosha_begin_time_and_miaosha_end_time(self, miaosha_time):
        '''
        返回秒杀开始和结束时间
        :param miaosha_time:
        :return: tuple  miaosha_begin_time, miaosha_end_time
        '''
        miaosha_begin_time = miaosha_time.get('miaosha_begin_time')
        miaosha_end_time = miaosha_time.get('miaosha_end_time')
        # 将字符串转换为datetime类型
        miaosha_begin_time = datetime.datetime.strptime(miaosha_begin_time, '%Y-%m-%d %H:%M:%S')
        miaosha_end_time = datetime.datetime.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')

        return miaosha_begin_time, miaosha_end_time

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
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua()  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies

        self.driver = webdriver.PhantomJS(executable_path=EXECUTABLE_PATH, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        ip_object = MyIpPools()
        ip_list = ip_object.get_proxy_ip_from_ip_pool().get('http')
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

    def get_url_body(self, tmp_url):
        '''
        得到url的body
        :param tmp_url: 待爬取的url
        :return: str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        try:
            response = requests.get(tmp_url, headers=self.headers, proxies=tmp_proxies, timeout=10)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            data = response.content.decode('utf-8')
            # print(data)
        except Exception:
            print('requests.get()请求超时....')
            print('today的data为空!')
            data = '{}'
        return data

    def phantomjs_get_url_body(self, tmp_url):
        '''
        返回给与的url的body
        :param tmp_url:
        :return: str
        '''
        self.from_ip_pool_set_proxy_ip_to_phantomjs()
        self.driver.set_page_load_timeout(10)  # 设置成10秒避免数据出错

        try:
            self.driver.get(tmp_url)
            self.driver.implicitly_wait(15)
            body = self.driver.page_source
            body = re.compile(r'\n').sub('', body)
            body = re.compile(r'\t').sub('', body)
            body = re.compile(r'  ').sub('', body)
            # print(body)
            body = re.compile(r'<body>(.*)</body>').findall(body)[0]
            # print(body)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 10 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            body = '{}'

        return body

    def json_to_dict(self, tmp_data):
        try:
            data = json.loads(tmp_data)
            # pprint(data)
            times = [str(timestamp_to_regulartime(int(item))) for item in data.get('times', [])]
            data = data.get('items', [])
            # print(data)
            # print(times)
        except:
            print('json.loads转换data的时候出错，data为空')
            data = []
        return data

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            tmp = {}
            miaosha_begin_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time'))))
            tmp_hour = miaosha_begin_time[-8:-6]
            if tmp_hour in PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST:
                if tmp_hour in PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST:
                    '''
                    # 这些起始的点秒杀时间只有30分钟
                    '''
                    miaosha_end_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*30))
                else:
                    miaosha_end_time = str(timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*60))

                tmp['miaosha_time'] = {
                    'miaosha_begin_time': miaosha_begin_time,
                    'miaosha_end_time': miaosha_end_time,
                }
                # 卷皮商品的goods_id
                tmp['goods_id'] = str(item.get('data', {}).get('goods_id'))
                # 限时秒杀库存信息
                tmp['stock_info'] = {
                    'activity_stock': int(item.get('data', {}).get('all_quantity', 0) - item.get('data', {}).get('sold_quantity', 0)),
                    'stock': item.get('data', {}).get('all_quantity', 0),
                }
                # 原始价格
                tmp['price'] = round(float(item.get('data', {}).get('normal_price', '0'))/100, 2)
                tmp['taobao_price'] = round(float(item.get('data', {}).get('price', '0'))/100, 2)
                miaosha_goods_list.append(tmp)
            else:
                pass
        return miaosha_goods_list

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        pinduoduo_spike = PinduoduoSpike()
        pinduoduo_spike.get_spike_hour_goods_info()
        try:
            del pinduoduo_spike
        except:
            pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()