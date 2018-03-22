# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_pintuan.py
@Time    : 2017/12/23 14:30
@connect : superonesfazai@gmail.com
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

from settings import HEADERS, IS_BACKGROUND_RUNNING
from juanpi_parse import JuanPiParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_requests import MyRequests
import datetime

class JuanPiPinTuan(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'tuan.juanpi.com',
            'User-Agent': HEADERS[randint(0, 34)]  # 随机一个请求头
        }

    def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url, 得到近期所有的限时拼团商品信息
        :return:
        '''
        pintuan_goods_id_list = []
        for page in range(0, 100):
            tmp_url = 'https://tuan.juanpi.com/pintuan/get_goods_list?page={0}&pageSize=20&cid=pinhaohuo_sx&show_type=wap'.format(
                str(page)
            )
            print('正在抓取的页面地址为: ', tmp_url)

            body = MyRequests.get_url_body(url=tmp_url, headers=self.headers)
            if body == '': body = '{}'
            try:
                tmp_data = json.loads(body)
                tmp_data = tmp_data.get('data', {}).get('goods', [])
            except:
                print('json.loads转换tmp_data时出错!')
                tmp_data = []

            # print(tmp_data)
            sleep(.3)

            if tmp_data == []:
                print('该tmp_url得到的goods为空list, 此处跳过!')
                break

            tmp_pintuan_goods_id_list = [{
                'goods_id': item.get('goods_id', ''),
                'begin_time': self.timestamp_to_regulartime(int(item.get('start_time', ''))),
                'end_time': self.timestamp_to_regulartime(int(item.get('end_time', ''))),
                'all_sell_count': str(item.get('join_number_int', '')),
                'page': page,
            } for item in tmp_data]
            # print(tmp_pintuan_goods_id_list)

            for item in tmp_pintuan_goods_id_list:
                if item.get('goods_id', '') not in [item2.get('goods_id', '') for item2 in pintuan_goods_id_list]:
                    pintuan_goods_id_list.append(item)

        print('该pintuan_goods_id_list的总个数为: ', len(pintuan_goods_id_list))
        print(pintuan_goods_id_list)

        juanpi_pintuan = JuanPiParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        index = 1
        if my_pipeline.is_connect_success:
            db_goods_id_list = [item[0] for item in list(my_pipeline.select_juanpi_pintuan_all_goods_id())]
            # print(db_goods_id_list)
            for item in pintuan_goods_id_list:
                if index % 5 == 0:
                    # 此处避免脚本占用大量内存
                    try:
                        del juanpi_pintuan
                    except:
                        pass
                    juanpi_pintuan = JuanPiParse()
                    gc.collect()

                if db_goods_id_list != []:
                    if item.get('goods_id', '') in db_goods_id_list:
                        print('该goods_id已经存在于数据库中, 此处跳过')
                        pass
                    else:
                        # * 注意卷皮的拼团时间跟它原先抓到的上下架时间是同一个时间 *
                        ## 所以就不用进行替换
                        goods_data = self.get_pintuan_goods_data(
                            juanpi_pintuan=juanpi_pintuan,
                            goods_id=item.get('goods_id', ''),
                            all_sell_count=item.get('all_sell_count', ''),
                            page=item.get('page', 0)
                        )

                        if goods_data == {}:    # 返回的data为空则跳过
                            pass
                        else:
                            # print(goods_data)
                            juanpi_pintuan.insert_into_juuanpi_pintuan_table(data=goods_data, pipeline=my_pipeline)
                            pass

                        sleep(.6)
                        index += 1

                else:
                    goods_data = self.get_pintuan_goods_data(
                        juanpi_pintuan=juanpi_pintuan,
                        goods_id=item.get('goods_id', ''),
                        all_sell_count=item.get('all_sell_count', ''),
                        page=item.get('page', 0)
                    )
                    if goods_data == {}:  # 返回的data为空则跳过
                        pass
                    else:
                        # print(goods_data)
                        juanpi_pintuan.insert_into_juuanpi_pintuan_table(data=goods_data, pipeline=my_pipeline)
                        pass
                    sleep(.6)
                    index += 1

        else:
            pass
        try:
            del juanpi_pintuan
        except:
            pass
        gc.collect()

    def get_pintuan_goods_data(self, juanpi_pintuan, goods_id, all_sell_count, page):
        '''
        得到goods_data
        :param juanpi_pintuan:
        :param goods_id: 商品id
        :param page:
        :return: a dict
        '''
        tmp_url = 'http://shop.juanpi.com/deal/' + str(goods_id)
        goods_id = juanpi_pintuan.get_goods_id_from_url(tmp_url)

        juanpi_pintuan.get_goods_data(goods_id=goods_id)
        goods_data = juanpi_pintuan.deal_with_data()

        if goods_data == {}:  # 返回的data为空则跳过
            pass

        else:
            goods_data['goods_id'] = str(goods_id)
            goods_data['spider_url'] = 'https://web.juanpi.com/pintuan/shop/' + str(goods_id)
            goods_data['username'] = '18698570079'
            goods_data['all_sell_count'] = all_sell_count
            goods_data['page'] = page
            goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = self.get_pintuan_begin_time_and_pintuan_end_time(schedule=goods_data.get('schedule', [])[0])

        gc.collect()
        return goods_data

    def get_pintuan_begin_time_and_pintuan_end_time(self, schedule):
        '''
        返回拼团开始和结束时间
        :param miaosha_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = schedule.get('begin_time')
        pintuan_end_time = schedule.get('end_time')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

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
        juanpi_pintuan = JuanPiPinTuan()
        juanpi_pintuan.get_pintuan_goods_info()
        # try:
        #     del juanpi_pintuan
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