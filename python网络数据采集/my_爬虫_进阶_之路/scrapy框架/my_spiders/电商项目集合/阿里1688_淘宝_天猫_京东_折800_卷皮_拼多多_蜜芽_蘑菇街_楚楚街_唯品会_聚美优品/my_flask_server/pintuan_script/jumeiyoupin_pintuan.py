# coding:utf-8

'''
@author = super_fazai
@File    : jumeiyoupin_pintuan.py
@Time    : 2018/3/25 11:32
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from random import randint
import json
import requests
import re
import time
from pprint import pprint
import gc
import pytz
from time import sleep
import os
import pytz, datetime
from logging import INFO, ERROR
import asyncio, aiohttp

from settings import HEADERS, MY_SPIDER_LOGS_PATH
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import IS_BACKGROUND_RUNNING, JUMEIYOUPIN_SLEEP_TIME
import datetime
from jumeiyoupin_pintuan_parse import JuMeiYouPinPinTuanParse
from my_logging import set_logger
from my_aiohttp import MyAiohttp

class JuMeiYouPinPinTuan(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 's.h5.jumei.com',
            'Referer': 'http://s.h5.jumei.com/yiqituan/list',
            'User-Agent': HEADERS[randint(0, len(HEADERS)-1)],  # 随机一个请求头
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.msg = ''
        self.my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/聚美优品/拼团/' + self.get_log_file_name_from_time() + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )
        self.tab_dict = {
            '母婴健康': 'coutuan_baby',
            '家居': 'coutuan_furniture',
            '饰品配饰': 'coutuan_jewellery',
            '内衣': 'coutuan_underwear',
            '食品保健': 'coutuan_food',
            '美妆': 'coutuan_makeup',
            '女装': 'coutuan_ladies',
            '礼品箱包': 'coutuan_bag',
            '数码家电': 'coutuan_3c',
            '鞋类': 'coutuan_shose',
            '下期预告': 'coutuan_pre',
        }

    async def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时拼团商品信息
        :return:
        '''
        goods_list = []
        for key in self.tab_dict:
            self.msg = '正在抓取的分类为: ' + key
            self.my_lg.info(self.msg)
            for index in range(1, 20):
                self.msg = '正在抓取第' + str(index) + '页...'
                self.my_lg.info(self.msg)
                tmp_url = 'http://s.h5.jumei.com/yiqituan/tab_list?tab={0}&page={1}&per_page=20'.format(
                    self.tab_dict[key],
                    str(index)
                )

                # 常规requests被过滤, aiohttp成功
                body = await MyAiohttp.aio_get_url_body(url=tmp_url, headers=self.headers)
                # self.my_lg.info(body)

                if body == '':
                    self.msg = '获取到的body为空str!' + ' 出错地址: ' + tmp_url
                    self.my_lg.error(self.msg)
                    pass
                else:
                    one_data = await self.json_2_dict(json_str=body)
                    if one_data == {}:
                        self.msg = '出错地址: ' + tmp_url
                        self.my_lg.error(self.msg)
                        continue
                    else:
                        if one_data.get('data', []) == []:
                            break

                        tmp_item_list = one_data.get('data', [])
                        item_list = [{
                            'goods_id': item.get('item_id', ''),
                            'pintuan_time': {
                                'begin_time': await self.timestamp_to_regulartime(item.get('start_time', '0')),
                                'end_time': await self.timestamp_to_regulartime(item.get('end_time', '0'))
                            },
                            'type': item.get('type', ''),
                            'sort': key,
                            'page': index,
                            'tab': self.tab_dict[key],
                        } for item in tmp_item_list if item.get('status', '') != 'soldout']
                        # self.my_lg.info(str(item_list))

                        for item in item_list:
                            goods_list.append(item)

                        # await asyncio.sleep(.5)

        self.my_lg.info(str(goods_list))
        self.my_lg.info('本次抓到所有拼团商品个数为: ' + str(len(goods_list)))
        await asyncio.sleep(3)

        return goods_list

    async def deal_with_data(self):
        '''
        处理并存储相关拼团商品的数据
        :return:
        '''
        jumeiyoupin = JuMeiYouPinPinTuanParse()
        goods_list = await self.get_pintuan_goods_info()

        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            db_goods_id_list = [item[0] for item in list(await my_pipeline.select_jumeiyoupin_pintuan_all_goods_id(logger=self.my_lg))]
            # self.my_lg.info(str(db_goods_id_list))

            for item in goods_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    self.my_lg.info('该goods_id已经存在于数据库中, 此处跳过')
                    pass
                else:
                    goods_id = item.get('goods_id', '')
                    tmp_url = 'https://s.h5.jumei.com/yiqituan/detail?item_id={0}&type={1}'.format(goods_id, item.get('type', ''))

                    tmp_url_s = tmp_url + '&'   # 防止筛选goods_id的时候报错退出
                    s_time = time.time()

                    goods_data = await jumeiyoupin.deal_with_data(jumei_pintuan_url=tmp_url_s)

                    if goods_data == {} or goods_data.get('is_delete', 0) == 1:
                        pass
                    else:
                        # 规范化
                        goods_data['goods_id'] = goods_id
                        goods_data['pintuan_time'] = item.get('pintuan_time', {})
                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = await self.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=item.get('pintuan_time', {}))
                        goods_data['sort'] = item.get('sort')
                        goods_data['page'] = item.get('page')
                        goods_data['tab'] = item.get('tab')

                        # pprint(goods_data)
                        # print(goods_data)

                        await jumeiyoupin.insert_into_jumeiyoupin_pintuan_table(data=goods_data, pipeline=my_pipeline)

                    try: del jumeiyoupin
                    except: pass

                    e_time = time.time()
                    if e_time - s_time > JUMEIYOUPIN_SLEEP_TIME:    # 使其更智能点
                        pass
                    else:
                        await asyncio.sleep(JUMEIYOUPIN_SLEEP_TIME)

        else:
            self.my_lg.error('数据库连接失败，此处跳过!')
            pass

        gc.collect()

    async def aio_get_url_body(self, url, headers, params=None, timeout=12, num_retries=8):
        '''
        异步获取url的body(定制版)
        :param url:
        :param headers:
        :param params:
        :param had_proxy:
        :param num_retries: 出错重试次数
        :return:
        '''
        proxy = await MyAiohttp.get_proxy()

        # 连接池不能太大, < 500
        conn = aiohttp.TCPConnector(verify_ssl=True, limit=150, use_dns_cache=True)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                async with session.get(url=url, headers=headers, params=params, proxy=proxy, timeout=timeout) as r:
                    result = await r.text(encoding=None)
                    result = await MyAiohttp.wash_html(result)
                    # print('success')
                    try:
                        tab = re.compile(r'tab=(.*?)&.*').findall(url)[0]
                        page = re.compile(r'page=(\d+)').findall(url)[0]
                    except IndexError:
                        return ('', '', '')

                    return (tab, int(page), result)
            except Exception as e:
                # print('出错:', e)
                if num_retries > 0:
                    # 如果不是200就重试，每次递减重试次数
                    return await self.aio_get_url_body(url=url, headers=headers, params=params, num_retries=num_retries - 1)
                else:
                    return ('', '', '')

    async def json_2_dict(self, json_str):
        '''
        异步json_2_dict
        :param json_str:
        :return: {} | {...}
        '''
        try:
            tmp = json.loads(json_str)
        except Exception:
            self.my_lg.error('json转换json_str时出错,请检查!')
            tmp = {}
        return tmp

    async def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(int(timestamp))
        # print(time_local)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt

    async def get_pintuan_begin_time_and_pintuan_end_time(self, pintuan_time):
        '''
        返回拼团开始和结束时间
        :param pintuan_time:
        :return: tuple  pintuan_begin_time, pintuan_end_time
        '''
        pintuan_begin_time = pintuan_time.get('begin_time')
        pintuan_end_time = pintuan_time.get('end_time')
        # 将字符串转换为datetime类型
        pintuan_begin_time = datetime.datetime.strptime(pintuan_begin_time, '%Y-%m-%d %H:%M:%S')
        pintuan_end_time = datetime.datetime.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')

        return pintuan_begin_time, pintuan_end_time

    def get_log_file_name_from_time(self):
        '''
        得到log文件的时间名字
        :return: 格式: 2016-03-25 类型str
        '''
        # 时区处理，时间处理到上海时间
        # pytz查询某个国家时区
        country_timezones_list = pytz.country_timezones('cn')
        # print(country_timezones_list)

        tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
        now_time = datetime.datetime.now(tz)
        # print(type(now_time))

        # 处理为精确到秒位，删除时区信息
        now_time = re.compile(r'\..*').sub('', str(now_time))
        # 将字符串类型转换为datetime类型
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        # print(now_time)

        return str(now_time)[0:10]

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
        except:
            pass
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
        jumeiyoupin_pintuan = JuMeiYouPinPinTuan()
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(jumeiyoupin_pintuan.deal_with_data())
        except RuntimeError:
            pass
        try:
            del jumeiyoupin_pintuan
            loop.close()
        except: pass
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