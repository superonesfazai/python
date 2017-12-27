# coding:utf-8

'''
@author = super_fazai
@File    : pinduoduo_miaosha_real-times_update.py
@Time    : 2017/11/27 14:20
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from pinduoduo_parse import PinduoduoParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
import os, re, pytz, datetime
import json
from pprint import pprint
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from random import randint
from settings import HEADERS
import requests
from settings import IS_BACKGROUND_RUNNING, PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST, PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST

from settings import PHANTOMJS_DRIVER_PATH
import datetime

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

'''
实时更新拼多多秒杀信息
'''

class Pinduoduo_Miaosha_Real_Time_Update(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.juanpi.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }
        self.init_phantomjs()

    def run_forever(self):
        '''
        这个实时更新的想法是只更新当天未来2小时的上架商品的信息，再未来信息价格(全为原价)暂不更新
        :return:
        '''
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server.select_pinduoduo_xianshimiaosha_all_goods_id())
        except TypeError as e:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            pinduoduo_miaosha = PinduoduoParse()
            for item in result:  # 实时更新数据
                # 对于拼多多先拿到该商品的结束时间点
                miaosha_end_time = json.loads(item[1]).get('miaosha_end_time')
                miaosha_end_time = int(str(time.mktime(time.strptime(miaosha_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                # print(miaosha_end_time)

                if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    if self.is_recent_time(miaosha_end_time) == 0:
                        tmp_sql_server.delete_pinduoduo_expired_goods_id(goods_id=item[0])
                        print('过期的goods_id为(%s)' % item[0], ', 限时秒杀结束时间为(%s), 删除成功!' % json.loads(item[1]).get('miaosha_end_time'))

                    elif self.is_recent_time(miaosha_end_time) == 2:
                        # break       # 跳出循环
                        pass          # 此处应该是pass,而不是break，因为数据库传回的goods_id不都是按照顺序的

                    else:  # 返回1，表示在待更新区间内
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))

                        all_miaosha_goods_list = self.get_all_miaosha_goods_list()

                        # 其中所有goods_id的list
                        miaosha_goods_all_goods_id = [i.get('goods_id') for i in all_miaosha_goods_list]
                        # print(miaosha_goods_all_goods_id)

                        if item[0] not in miaosha_goods_all_goods_id:  # 内部已经下架的
                            '''
                            表示其中没有了该goods_id
                            '''
                            tmp_sql_server.delete_pinduoduo_expired_goods_id(goods_id=item[0])
                            print('该商品[goods_id为(%s)]已被下架限时秒杀活动，此处将其删除' % item[0])
                            pass

                        else:       # 未下架的
                            for item_1 in all_miaosha_goods_list:
                                if item_1.get('goods_id', '') == item[0]:
                                    # # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
                                    # pinduoduo_miaosha = PinduoduoParse()
                                    pinduoduo_miaosha.get_goods_data(goods_id=item[0])
                                    goods_data = pinduoduo_miaosha.deal_with_data()

                                    if goods_data == {}:  # 返回的data为空则跳过
                                        pass
                                    else:  # 否则就解析并且插入
                                        goods_data['stock_info'] = item_1.get('stock_info')
                                        goods_data['goods_id'] = item_1.get('goods_id')
                                        # goods_data['username'] = '18698570079'
                                        if item_1.get('stock_info').get('activity_stock') > 0:
                                            goods_data['price'] = item_1.get('price')  # 秒杀前的原特价
                                            goods_data['taobao_price'] = item_1.get('taobao_price')  # 秒杀价
                                        else:
                                            pass
                                        goods_data['sub_title'] = item_1.get('sub_title', '')
                                        goods_data['miaosha_time'] = item_1.get('miaosha_time')
                                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=item_1.get('miaosha_time'))

                                        if item_1.get('stock_info').get('activity_stock') <= 1:
                                            # 实时秒杀库存小于等于1时就标记为 已售罄
                                            print('该秒杀商品已售罄...')
                                            goods_data['is_delete'] = 1

                                        # print(goods_data)
                                        pinduoduo_miaosha.to_update_pinduoduo_xianshimiaosha_table(data=goods_data, pipeline=tmp_sql_server)
                                    sleep(.4)
                                else:
                                    pass

                    index += 1
                    gc.collect()

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time_hour() == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(3)
        # del ali_1688
        gc.collect()

    def get_all_miaosha_goods_list(self):
        # 今日秒杀
        tmp_url = 'http://apiv4.yangkeduo.com/api/spike/v2/list/today?page=0&size=2000'
        # print('待爬取的今日限时秒杀数据的地址为: ', tmp_url)
        # today_data = self.get_url_body(tmp_url=tmp_url)
        today_data = self.phantomjs_get_url_body(tmp_url=tmp_url)
        today_data = self.json_to_dict(tmp_data=today_data)

        # 明日的秒杀
        tmp_url_2 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/tomorrow?page=0&size=2000'
        # print('待爬取的明日限时秒杀数据的地址为: ', tmp_url_2)
        # tomorrow_data = self.get_url_body(tmp_url=tmp_url_2)
        tomorrow_data = self.phantomjs_get_url_body(tmp_url=tmp_url_2)
        tomorrow_data = self.json_to_dict(tmp_data=tomorrow_data)

        # 未来的秒杀
        tmp_url_3 = 'http://apiv4.yangkeduo.com/api/spike/v2/list/all_after?page=0&size=2000'
        # print('待爬取的未来限时秒杀数据的地址为: ', tmp_url_3)
        # all_after_data = self.get_url_body(tmp_url=tmp_url_3)
        all_after_data = self.phantomjs_get_url_body(tmp_url=tmp_url_3)
        all_after_data = self.json_to_dict(tmp_data=all_after_data)

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
        # print('当前所有限时秒杀商品list为: ', all_miaosha_goods_list)

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

    def get_miaoshao_goods_info_list(self, data):
        '''
        得到秒杀商品有用信息
        :param data: 待解析的data
        :return: 有用信息list
        '''
        miaosha_goods_list = []
        for item in data:
            tmp = {}
            miaosha_begin_time = str(self.timestamp_to_regulartime(int(item.get('data', {}).get('start_time'))))
            tmp_hour = miaosha_begin_time[-8:-6]
            if tmp_hour in PINDUODUO_MIAOSHA_SPIDER_HOUR_LIST:
                if tmp_hour in PINDUODUO_MIAOSHA_BEGIN_HOUR_LIST:
                    '''
                    # 这些起始的点秒杀时间只有30分钟
                    '''
                    miaosha_end_time = str(self.timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*30))
                else:
                    miaosha_end_time = str(self.timestamp_to_regulartime(int(item.get('data', {}).get('start_time')) + 60*60))

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

    def get_url_body(self, tmp_url):
        '''
        得到url的body
        :param tmp_url: 待爬取的url
        :return: str
        '''
        # 设置代理ip
        self.proxies = self.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
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
            times = [str(self.timestamp_to_regulartime(int(item))) for item in data.get('times', [])]
            data = data.get('items', [])
            # print(data)
            # print(times)
        except:
            print('json.loads转换data的时候出错，data为空')
            data = []
        return data

    def is_recent_time(self, timestamp):
        '''
        判断是否在指定的日期差内
        :param timestr: 时间戳
        :return: 0: 已过期恢复原价的 1: 待更新区间内的 2: 未来时间的
        '''
        time_1 = int(timestamp)
        time_2 = int(time.time())  # 当前的时间戳

        diff_time = time_1 - time_2
        if diff_time <= 0:
            return 0    # 已过期恢复原价的
        elif diff_time > 0 and diff_time <= 7200:   # 未来2小时的
            return 1    # 表示是昨天跟今天的也就是待更新的
        else:
            return 2    # 未来时间的暂时不用更新

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

        self.driver = webdriver.PhantomJS(executable_path=EXECUTABLE_PATH, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
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

def get_shanghai_time_hour():
    '''
    时区处理，时间处理到上海时间
    '''
    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time.hour

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
        print('一次大更新即将开始'.center(30, '-'))
        tmp = Pinduoduo_Miaosha_Real_Time_Update()
        tmp.run_forever()
        try:
            del tmp
        except:
            pass
        gc.collect()
        print('一次大更新完毕'.center(30, '-'))

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