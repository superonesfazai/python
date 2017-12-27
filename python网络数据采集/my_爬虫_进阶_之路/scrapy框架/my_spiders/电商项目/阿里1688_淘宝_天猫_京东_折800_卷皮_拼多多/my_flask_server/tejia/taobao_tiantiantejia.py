# coding:utf-8

'''
@author = super_fazai
@File    : taobao_tiantiantejia.py
@Time    : 2017/12/26 16:02
@connect : superonesfazai@gmail.com
'''

"""
淘宝天天特价板块
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
import pytz

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

    def get_goods_list_and_deal_with_data(self):
        '''
        模拟构造得到天天特价的所有商品的list, 并且解析存入每个
        :return:
        '''
        # * 获取分类的name和extQuery的tagId的地址为 *(开始为在blockId=902开始)
        # https://metrocity.taobao.com/json/fantomasTags.htm?_input_charset=utf-8&appId=9&blockId=902
        for block_id in range(902, 950, 2):
            sort_url = 'https://metrocity.taobao.com/json/fantomasTags.htm?_input_charset=utf-8&appId=9&blockId=' + str(block_id)
            print(sort_url)
            sort_body = self.get_url_body(url=sort_url)
            print(sort_body)

        tmp_url = 'https://metrocity.taobao.com/json/fantomasItems.htm?sort=null&appId=9&blockId=914&pageSize=1000&_input_charset=utf-8'

        tmp_body = self.get_url_body(url=tmp_url)
        tejia_goods_list = self.get_tiantiantejia_goods_list(body=tmp_body)
        print(tejia_goods_list)

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
        tmp_headers['cookie'] = 'UM_distinctid=16015e04f6d4ff-037c1f4e36bf3-17386d57-fa000-16015e04f6e555; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; ali_apache_id=11.228.45.44.1512376392548.274581.5; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLQKaueubXgKyDU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; t=567b173f0709a9279b1255b8cb39b2fc; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; miid=5767446262036433919; cna=ZyWpEl+kTywCAXHXsSxv8Ati; cookie2=15c1fda7973edcbe0105c74d28a4a51d; _tb_token_=8e33663a5306; v=0; mt=ci=-1_0; linezing_session=bJoeqtC38UdQyLARdXoeon1N_1514273311440Yq3z_1; _m_h5_tk=61ee4727021cbffa54957d35273006f5_1514276876357; _m_h5_tk_enc=c8213eca0b9d27725f3d105e9b7c27d6; l=AvT0JKUZDcPfSJZdxeTqrbhlRKlmzxnl; uc1=cookie14=UoTdf1MI%2FjVqdQ%3D%3D; isg=AtHRDIQhb6JI1oPWFHFLrKxu4NurlkTIWDcky7NiNxmhWvOs-I7KgKvwiBhH'
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
        taobao_tiantaintejia.get_goods_list_and_deal_with_data()
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