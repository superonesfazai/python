# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_spike.py
@Time    : 2018/1/30 18:34
@connect : superonesfazai@gmail.com
'''

'''
蘑菇街秒杀抓取
'''

from random import randint
import json
import re
import time
from pprint import pprint
import gc
import pytz
from time import sleep
import os

import sys
sys.path.append('..')

from settings import HEADERS
from mogujie_miaosha_parse import MoGuJieMiaoShaParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_requests import MyRequests
from settings import IS_BACKGROUND_RUNNING, MOGUJIE_SLEEP_TIME
import datetime
from decimal import Decimal

class MoGuJieSpike(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.mogujie.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

    def get_spike_hour_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时秒杀商品信息
        :return:
        '''
        for item in self.get_today_hour_timestamp():
            self.traversal_hour_timestamp(item=item)

        # 明日的商品列表
        tomorrow_hour_timestamp = [item + 1*86400 for item in self.get_today_hour_timestamp()]
        for item in tomorrow_hour_timestamp:
            self.traversal_hour_timestamp(item=item)

        # 后天的商品列表
        tomorrow_hour_timestamp = [item + 2*86400 for item in self.get_today_hour_timestamp()]
        for item in tomorrow_hour_timestamp:
            self.traversal_hour_timestamp(item=item)

    def deal_with_data(self, *param):
        '''
        处理并存储相关秒杀商品的数据
        :param param: 相关参数
        :return:
        '''
        print(60 * '*')
        event_time = param[0]
        print('秒杀开始时间:', self.timestamp_to_regulartime(event_time), '\t', '对应时间戳为: ', event_time)
        print(60 * '*')

        item_list = param[1]

        mogujie = MoGuJieMiaoShaParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            db_goods_id_list = [item[0] for item in list(my_pipeline.select_mogujie_xianshimiaosha_all_goods_id())]
            # print(db_goods_id_list)

            for item in item_list:
                if item.get('iid', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = str(item.get('iid', ''))
                    tmp_url = item.get('link', '')

                    try:
                        object_id = re.compile(r'objectId=(.*?)&').findall(tmp_url)[0]
                    except IndexError:      # 表示匹配到的地址不是秒杀商品的地址
                        print('+++++++ 这个url不是秒杀的url: ', tmp_url)
                        continue

                    tmp_url = 'https://shop.mogujie.com/rushdetail/{0}?objectId={1}&type=rush'.format(goods_id, object_id)

                    tmp_ = mogujie.get_goods_id_from_url(tmp_url)
                    mogujie.get_goods_data(goods_id=tmp_)
                    goods_data = mogujie.deal_with_data()

                    if goods_data == {}:  # 返回的data为空则跳过
                        pass

                    else:   # 否则就解析并且插入
                        goods_data['goods_url'] = tmp_url
                        goods_data['goods_id'] = str(goods_id)

                        # price设置为原价
                        try:
                            tmp_price_list = sorted([round(float(item_4.get('normal_price', '')), 2) for item_4 in goods_data['price_info_list']])
                            price = Decimal(tmp_price_list[-1]).__round__(2)  # 商品原价
                            goods_data['price'] = price
                        except:
                            print('设置price为原价时出错!请检查')
                            continue

                        goods_data['miaosha_time'] = {
                            'miaosha_begin_time': self.timestamp_to_regulartime(int(item.get('startTime', 0))),
                            'miaosha_end_time': self.timestamp_to_regulartime(int(item.get('endTime', 0))),
                        }
                        goods_data['miaosha_begin_time'], goods_data['miaosha_end_time'] = self.get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data['miaosha_time'])
                        goods_data['event_time'] = str(event_time)

                        # pprint(goods_data)
                        # print(goods_data)
                        mogujie.insert_into_mogujie_xianshimiaosha_table(data=goods_data, pipeline=my_pipeline)
                        sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mogujie
        except:
            pass
        gc.collect()

    def traversal_hour_timestamp(self, item):
        '''
        遍历每个需求的整点时间戳
        :param item:
        :return:
        '''
        # 先遍历today的需求的整点时间戳
        tmp_url = 'https://qiang.mogujie.com//jsonp/fastBuyListActionLet/1?eventTime={0}&bizKey=rush_main'.format(str(item))
        body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
        # print(body)

        if body == '':
            print('item为: ', item)
            print('获取到的body为空值! 此处跳过')

        else:
            try:
                body = re.compile('null\((.*)\)').findall(body)[0]
            except Exception:
                print('re匹配body中的数据时出错!')
                body = '{}'

            try:
                tmp_data = json.loads(body)
            except:
                print('json.loads转换body时出错, 此处跳过!')
                tmp_data = {}

            if tmp_data == {}:
                print('tmp_data为空{}!')
                pass
            else:
                # pprint(tmp_data)
                # print(tmp_data)

                event_time = item
                item_list = tmp_data.get('data', {}).get('list', [])

                self.deal_with_data(event_time, item_list)
                sleep(MOGUJIE_SLEEP_TIME)

    def get_today_hour_timestamp(self):
        '''
        得到today的整点时间戳(需求的整点为: 9-16点)
        :return:today_hour_timestamp_list 类型 list
        '''
        today_hour_timestamp_list = []
        for hour in range(9, 17):  # 循环需求的整点时间
            a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % hour  # strftime格式化,%2d以2位的固定位宽获取int型的数值，由此获得整点字符串
            time_array = time.strptime(a, "%Y-%m-%d %H:%M:%S")  # 把一个时间字符串解析为时间元组，返回struct_time对象。
            timestamp = int(time.mktime(time_array))            # 接收struct_time对象，返回时间的浮点数
            today_hour_timestamp_list.append(timestamp)

        return today_hour_timestamp_list

    def timestamp_to_regulartime(self, timestamp):
        '''
        把时间戳转成字符串形式
        :param time_stamp: 时间戳
        :return:
        '''
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

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
        mogujie_spike = MoGuJieSpike()
        mogujie_spike.get_spike_hour_goods_info()
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