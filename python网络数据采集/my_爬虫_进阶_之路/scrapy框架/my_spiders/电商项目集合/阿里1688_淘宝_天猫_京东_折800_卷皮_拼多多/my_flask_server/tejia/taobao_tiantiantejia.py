# coding:utf-8

'''
@author = super_fazai
@File    : taobao_tiantiantejia.py
@Time    : 2017/12/26 16:02
@connect : superonesfazai@gmail.com
'''

"""
淘宝天天特价板块抓取清洗入库
"""

import sys
sys.path.append('..')

import time
from random import randint
import json
import requests
import re
from pprint import pprint
from decimal import Decimal
from time import sleep
import datetime
import gc

from settings import HEADERS
from settings import PHANTOMJS_DRIVER_PATH, CHROME_DRIVER_PATH, IS_BACKGROUND_RUNNING
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline, SqlPools
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytz

from taobao_parse import TaoBaoLoginAndParse

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class TaoBaoTianTianTeJia(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'metrocity.taobao.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }
        self.result_data = {}
        self.init_phantomjs()

        self.main_sort = {
            '901': '时尚女装',
            '902': '舒适内衣',
            '903': '包包配饰',
            '904': '男鞋女鞋',
            '905': '品质男装',
            '906': '母婴儿童',
            '907': '日用百货',
            '908': '美食特产',
            '909': '数码家电',
            '910': '美容护肤',
            '911': '运动户外',
        }

    def get_all_goods_list(self):
        '''
        模拟构造得到天天特价的所有商品的list, 并且解析存入每个
        :return: sort_data  类型list
        '''
        # * 获取分类的name和extQuery的tagId的地址为 *(开始为在blockId=901开始)
        # https://metrocity.taobao.com/json/fantomasTags.htm?_input_charset=utf-8&appId=9&blockId=901
        sort_data = []
        for block_id in range(901, 914, 1):
            sort_url = 'https://metrocity.taobao.com/json/fantomasTags.htm?_input_charset=utf-8&appId=9&blockId=' + str(block_id)
            print(sort_url)
            sort_body = self.use_phantomjs_to_get_url_body(url=sort_url)
            # print(sort_body)

            if sort_body != '':
                tmp_sort_data = self.get_sort_data_list(body=sort_body)
                # print(tmp_sort_data)
                if str(block_id) in self.main_sort:
                    sort_name = self.main_sort[str(block_id)]
                    # print(sort_name)
                    tmp = {
                        block_id: sort_name,
                        'data': tmp_sort_data,
                    }
                    sort_data.append(tmp)
            sleep(.5)
        pprint(sort_data)

        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

        return sort_data

    def deal_with_all_goods_id(self, sort_data):
        '''
        获取每个详细分类的商品信息
        :param sort_data: 所有分类的商品信息(包括商品id跟特价开始时间跟结束时间)
        :return: None
        '''
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        # my_pipeline = SqlPools()
        index = 1
        if my_pipeline.is_connect_success:
            # 普通sql_server连接(超过3000无返回结果集)
            db_goods_id_list = [item[0] for item in list(my_pipeline.select_taobao_tiantian_tejia_all_goods_id())]
            print(db_goods_id_list)

            for item in sort_data:
                for key in item.keys():
                    if isinstance(key, int):  # 当key值类型为int时, 表示为详细分类的blockID的值
                        tmp_data = item.get('data', [])
                        for item_2 in tmp_data:
                            # &extQuery=tagId%3A1010142     要post的数据, 此处直接用get模拟
                            tmp_url = 'https://metrocity.taobao.com/json/fantomasItems.htm?appId=9&pageSize=1000&_input_charset=utf-8&blockId={0}&extQuery=tagId%3A{1}'.format(
                                str(key), item_2.get('extQuery', '')[6:]
                            )

                            tmp_body = self.get_url_body(url=tmp_url)
                            tejia_goods_list = self.get_tiantiantejia_goods_list(body=tmp_body)
                            print(tejia_goods_list)

                            for tmp_item in tejia_goods_list:
                                if tmp_item.get('goods_id', '') in db_goods_id_list:
                                    print('该goods_id已经存在于数据库中, 此处跳过')
                                    pass

                                else:
                                    if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                                        print('正在重置，并与数据库建立新连接中...')
                                        # try:
                                        #     del my_pipeline
                                        # except:
                                        #     pass
                                        # gc.collect()
                                        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                                        # my_pipeline = SqlPools()
                                        print('与数据库的新连接成功建立...')

                                    if my_pipeline.is_connect_success:
                                        tmp_url = 'https://item.taobao.com/item.htm?id=' + str(tmp_item.get('goods_id', ''))
                                        taobao = TaoBaoLoginAndParse()
                                        goods_id = taobao.get_goods_id_from_url(tmp_url)
                                        taobao.get_goods_data(goods_id=goods_id)
                                        goods_data = taobao.deal_with_data(goods_id=goods_id)

                                        if goods_data != {}:
                                            goods_data['goods_id'] = tmp_item.get('goods_id', '')
                                            goods_data['goods_url'] = tmp_url
                                            goods_data['schedule'] = [{
                                                'begin_time': tmp_item.get('start_time', ''),
                                                'end_time': tmp_item.get('end_time', ''),
                                            }]
                                            goods_data['tejia_begin_time'], goods_data['tejia_end_time'] = self.get_tejia_begin_time_and_tejia_end_time(schedule=goods_data.get('schedule', [])[0])
                                            goods_data['block_id'] = str(key)
                                            goods_data['tag_id'] = item_2.get('extQuery', '')[6:]
                                            goods_data['father_sort'] = self.main_sort[str(key)]
                                            goods_data['child_sort'] = item_2.get('name', '')
                                            # print(goods_data)

                                            taobao.insert_into_taobao_tiantiantejia_table(data=goods_data, pipeline=my_pipeline)
                                        else:
                                            sleep(4)    # 否则休息4秒
                                            pass
                                        sleep(2)
                                        index += 1
                                    else:
                                        print('数据库连接失败!')
                                        pass
                    else:
                        pass

        else:
            print('数据库连接失败!')
            pass
        gc.collect()

    def get_url_body(self, url):
        '''
        获取url的body
        :param url: 待抓取的地址url
        :return: str
        '''
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        # 更改Host
        tmp_headers = self.headers
        tmp_host = re.compile(r'https://(.*?)/.*').findall(url)[0]
        tmp_headers['Host'] = tmp_host
        try:
            response = requests.get(url, headers=tmp_headers, proxies=tmp_proxies, timeout=16)
            body = response.content.decode('utf-8')
            # print(body)
            body = re.compile(r'\n').sub('', body)
            body = re.compile(r'\t').sub('', body)
            body = re.compile(r'  ').sub('', body)
            # print(body)

            body = re.compile(r'\((.*)\)').findall(body)[0]
        except:
            print('requests.get()请求超时....')
            print('data为空!')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            body = '{}'

        return body

    def get_tejia_begin_time_and_tejia_end_time(self, schedule):
        '''
        返回拼团开始和结束时间
        :param miaosha_time:
        :return: tuple  tejia_begin_time, tejia_end_time
        '''
        tejia_begin_time = schedule.get('begin_time')
        tejia_end_time = schedule.get('end_time')
        # 将字符串转换为datetime类型
        tejia_begin_time = datetime.datetime.strptime(tejia_begin_time, '%Y-%m-%d %H:%M:%S')
        tejia_end_time = datetime.datetime.strptime(tejia_end_time, '%Y-%m-%d %H:%M:%S')

        return tejia_begin_time, tejia_end_time

    def use_phantomjs_to_get_url_body(self, url):
        '''
        通过phantomjs来获取url的body
        :return: data   str类型
        '''
        self.from_ip_pool_set_proxy_ip_to_phantomjs()
        try:
            self.driver.set_page_load_timeout(15)  # 设置成10秒避免数据出错
        except:
            return {}

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(20)  # 隐式等待和显式等待可以同时使用

            main_body = self.driver.page_source
            main_body = re.compile(r'\n').sub('', main_body)
            main_body = re.compile(r'\t').sub('', main_body)
            main_body = re.compile(r'  ').sub('', main_body)
            # print(main_body)
            data = re.compile(r'\((.*)\)').findall(main_body)[0]  # 贪婪匹配匹配所有
            # print(data)
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 15 seconds when loading page')
            print('报错如下: ', e)
            # self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            print('data为空!')
            self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
            data = ''

        return data

    def get_sort_data_list(self, body):
        '''
        获取到分类的list(对应name和extQuery的值的list)
        :param body: 待转换的json
        :return: sort_data  类型 list
        '''
        try:
            sort_data = json.loads(body)
        except Exception:
            print('在获取分类信息的list时, json.loads转换出错, 此处跳过!')
            sort_data = {}

        try:
            sort_data = sort_data.get('data', [])
        except:
            print('获取分类信息data中的key值data出错!')
            sort_data = []

        return sort_data

    def get_tiantiantejia_goods_list(self, body):
        '''
        将str类型的body转换为需求的list
        :param body:
        :return: a list
        '''
        try:
            data = json.loads(body)
        except Exception:
            print('在获取天天特价商品id的list时, json.loads转换出错, 此处跳过!')
            data = {}

        try:
            data = data.get('data', [])
        except Exception:
            print('获取data中的key值data出错!')
            data = []

        if data != []:
            # 处理得到需要的数据
            tejia_goods_list = [{
                'goods_id': item.get('itemId', ''),
                'start_time': self.deal_with_time_to_regulartime(item.get('activityStartTime', '')),
                'end_time': self.deal_with_time_to_regulartime(item.get('activityEndTime', '')),
            } for item in data]
        else:
            tejia_goods_list = []

        return tejia_goods_list

    def deal_with_time_to_regulartime(self, tmp_time):
        '''
        处理得到规范的时间
        :param tmp_time: str    eg: '20171225000000'
        :return: str    规律的人眼可识别的时间 2609-03-15 14:03:20
        '''
        return tmp_time[0:4] + '-' + tmp_time[4:6] + '-' + tmp_time[6:8] + ' ' + tmp_time[8:10] + ':' + tmp_time[10:12] + ':' + tmp_time[12:14]

    def init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        '''
        研究发现, 必须以浏览器的形式进行访问才能返回需要的东西
        常规requests模拟请求会被阿里服务器过滤, 并返回请求过于频繁的无用页面
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

        wait = ui.WebDriverWait(self.driver, 20)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

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
        # self.driver.quit()
        gc.collect()

def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    '''
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:     # 父进程
            os._exit(0)
    except OSError as e:
        sys.stderr.write("first fork failed!!" + e.strerror)
        os._exit(1)

    # 子进程， 由于父进程已经退出，所以子进程变为孤儿进程，由init收养
    '''setsid使子进程成为新的会话首进程，和进程组的组长，与原来的进程组、控制终端和登录会话脱离。'''
    os.setsid()
    '''防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下'''
    os.chdir("/")
    '''设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的'''
    os.umask(0)

    try:
        pid = os.fork()  # 第二次进行fork,为了防止会话首进程意外获得控制终端
        if pid > 0:
            os._exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("second fork failed!!" + e.strerror)
        os._exit(1)

    # 孙进程
    #   for i in range(3, 64):  # 关闭所有可能打开的不需要的文件，UNP中这样处理，但是发现在python中实现不需要。
    #       os.close(i)
    sys.stdout.write("Daemon has been created! with pid: %d\n" % os.getpid())
    sys.stdout.flush()  # 由于这里我们使用的是标准IO，这里应该是行缓冲或全缓冲，因此要调用flush，从内存中刷入日志文件。

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        taobao_tiantaintejia = TaoBaoTianTianTeJia()
        sort_data = taobao_tiantaintejia.get_all_goods_list()
        taobao_tiantaintejia.deal_with_all_goods_id(sort_data=sort_data)
        # try:
        #     del taobao_tiantaintejia
        # except:
        #     pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

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