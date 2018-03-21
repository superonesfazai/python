# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_spike.py
@Time    : 2018/3/18 09:42
@connect : superonesfazai@gmail.com
'''

"""
聚美优品每日10点上新限时秒杀，商品信息抓取
"""

from random import randint
import json
import requests
import re
import time
from pprint import pprint
import gc
import pytz
from time import sleep
import os, datetime
from decimal import Decimal

import sys
sys.path.append('..')

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import HEADERS
from jumeiyoupin_parse import JuMeiYouPinParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_ip_pools import MyIpPools
from settings import IS_BACKGROUND_RUNNING, JUMEIYOUPIN_SLEEP_TIME, PHANTOMJS_DRIVER_PATH

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class JuMeiYouPinSpike(object):
    def __init__(self):
        self.headers = {
            'Accept': 'application/json,text/javascript,text/plain,*/*;q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'h5.jumei.com',
            'Referer': 'https://h5.jumei.com/',
            'Cache-Control': 'max-age=0',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': HEADERS[randint(0, 34)],  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        all_goods_list = []
        self.init_phantomjs()
        cookies = self.get_cookies_from_session(url='https://h5.jumei.com/')
        try: self.driver.quit()
        except: pass
        if cookies == '':
            print('!!! 获取cookies失败 !!!')
            return False

        print('获取cookies成功!')
        self.headers.update(Cookie=cookies)

        for page in range(1, 50):   # 1, 开始
            tmp_url = 'https://h5.jumei.com/index/ajaxDealactList?card_id=4057&page={0}&platform=wap&type=formal&page_key=1521336720'.format(str(page))
            print('正在抓取的page为:', page, ', 接口地址为: ', tmp_url)
            body = self.get_url_body(tmp_url=tmp_url)
            # print(body)

            try:
                json_body = json.loads(body)
                # print(json_body)
            except:
                print('json.loads转换body时出错!请检查')
                json_body = {}
                pass

            this_page_item_list = json_body.get('item_list', [])
            if this_page_item_list == []:
                print('@@@@@@ 所有接口数据抓取完毕 !')
                break

            for item in this_page_item_list:
                if item.get('item_id', '') not in [item_1.get('item_id', '') for item_1 in all_goods_list]:
                    item['page'] = page
                    all_goods_list.append(item)

            sleep(.5)

        all_goods_list = [{
            'goods_id': str(item.get('item_id', '')),
            'type': item.get('type', ''),
            'page': item.get('page')
        } for item in all_goods_list if item.get('item_id') is not None]
        print(all_goods_list)
        print('本次抓取到共有限时商品个数为: ', all_goods_list.__len__())

        self.deal_with_data(all_goods_list)

        return True

    def deal_with_data(self, *params):
        '''
        处理并存储相关秒杀商品数据
        :param params: 相关参数
        :return:
        '''
        item_list = params[0]
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            db_goods_id_list = [item[0] for item in list(my_pipeline.select_jumeiyoupin_xianshimiaosha_all_goods_id())]
            # print(db_goods_id_list)

            for item in item_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass
                else:
                    jumei = JuMeiYouPinParse()
                    goods_id = item.get('goods_id', '')
                    type = item.get('type', '')
                    tmp_url = 'https://h5.jumei.com/product/detail?item_id={0}&type={1}'.format(goods_id, type)
                    jumei.get_goods_data(goods_id=[goods_id, type])
                    goods_data = jumei.deal_with_data()

                    if goods_data == {}:
                        pass

                    elif goods_data.get('is_delete', 0) == 1:
                        print('------>>>| 该商品库存为0，已被抢光!')
                        pass

                    else:   # 否则就解析并且插入
                        goods_data['goods_url'] = tmp_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': goods_data['schedule'].get('begin_time', ''),
                            'miaosha_end_time': goods_data['schedule'].get('end_time', ''),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                        goods_data['page'] = item.get('page')

                        # pprint(goods_data)
                        # print(goods_data)
                        jumei.insert_into_jumeiyoupin_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        sleep(JUMEIYOUPIN_SLEEP_TIME)  # 放慢速度   由于初始化用了phantomjs时间久，于是就不睡眠

                    try: del jumei
                    except: pass

        else:
            print('数据库连接失败，此处跳过!')
            pass

        gc.collect()

    def get_cookies_from_session(self, url, css_selector=''):
        '''
        从session中获取cookies
        :param url:
        :return:
        '''
        print('正在获取cookies...请耐心等待...')
        change_ip_result = self.from_ip_pool_set_proxy_ip_to_phantomjs()
        if change_ip_result == '':
            return ''

        try:
            self.driver.set_page_load_timeout(15)  # 设置成10秒避免数据出错
        except:
            return ''

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
                    print('div.d-content已经加载完毕')

            cookies = self.get_right_str_cookies(self.driver.get_cookies())
            # print(cookies)

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 15 seconds when loading page')
            print('报错如下: ', e)
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            cookies = ''

        return cookies

    def get_url_body(self, tmp_url):
        '''
        根据url得到body
        :param tmp_url:
        :return: body   类型str
        '''
        # 设置代理ip
        ip_object = MyIpPools()
        self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]

        tmp_proxies = {
            'http': self.proxy,
        }
        # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(self.proxy))

        tmp_headers = self.headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(tmp_url)[0]
        # tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'

        s = requests.session()
        try:
            response = s.get(tmp_url, headers=tmp_headers, proxies=tmp_proxies, timeout=12)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            body = response.content.decode('utf-8')

            body = re.compile('\t').sub('', body)
            body = re.compile('  ').sub('', body)
            body = re.compile('\r\n').sub('', body)
            body = re.compile('\n').sub('', body)
            # print(body)
        except Exception:
            print('requests.get()请求超时....')
            print('data为空!')
            body = ''

        return body

    def init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        # print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 9)]  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies
        tmp_execute_path = EXECUTABLE_PATH

        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 20)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        # print('------->>>初始化完毕<<<-------')

    def from_ip_pool_set_proxy_ip_to_phantomjs(self):
        '''
        给phantomjs设置代理ip
        :return: '' 表示切换代理ip出错 | None
        '''
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
            return ''

        return None

    def get_right_str_cookies(self, cookies):
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

    def __del__(self):
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
        jumeiyoupin_spike = JuMeiYouPinSpike()
        jumeiyoupin_spike.get_spike_hour_goods_info()
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*2)

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