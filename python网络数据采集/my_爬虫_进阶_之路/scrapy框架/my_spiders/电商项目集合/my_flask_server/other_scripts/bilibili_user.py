# coding:utf-8

'''
@author = super_fazai
@File    : bilibili_user.py
@Time    : 2018/1/10 10:03
@connect : superonesfazai@gmail.com
'''

"""
抓取B站用户信息
"""

import sys
sys.path.append('..')

import requests
import json
import random
# import pymysql
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool
from random import randint
from pprint import pprint
import re, gc

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import IS_BACKGROUND_RUNNING

from requests.exceptions import ReadTimeout, ConnectionError
# from requests_futures.sessions import FuturesSession

import asyncio
import aiohttp

from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import daemon_init
from fzutils.ip_pools import MyIpPools

reload(sys)

class BiLiBiLiUser(object):
    def __init__(self):
        self.index = 1      # 全局变量
        self.uas = self.LoadUserAgents("user_agents.txt")
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://space.bilibili.com/45388',
            'Origin': 'http://space.bilibili.com',
            'Host': 'space.bilibili.com',
            'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        tmp__ = SqlServerMyPageInfoSaveItemPipeline()
        print('正在获取db中的所有nick_name....耐心等待....')
        sql_str = r'select nick_name from dbo.sina_weibo'
        _ = tmp__._select_table(sql_str=sql_str)
        self.db_nick_name_list = [item[0] for item in _] if _ is not None else []
        # self.db_nick_name_list = []
        print(len(self.db_nick_name_list))
        print('完成')

    def datetime_to_timestamp_in_milliseconds(self, d):
        def current_milli_time():
            return int(round(time.time() * 1000))

        return current_milli_time()

    def LoadUserAgents(self, uafile):
        """
        uafile : string
            path to text file of user agents, one per line
        """
        uas = []
        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1 - 1])
        random.shuffle(uas)
        return uas

    async def test(self, payload, tmp_proxies):
        try:
            async with aiohttp.request(
                    method='POST',
                    url='http://space.bilibili.com/ajax/member/GetInfo',
                    headers=self.head,
                    data=payload,
                    proxy=tmp_proxies['http'],
            ) as r:
                tmp_ = await r.text()
                return tmp_
        except Exception:
            print('aiohttp异步请求出错, 请检查!')
            return None

    def run_forever(self):
        time1 = time.time()

        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        for m in range(6000, 9500):  # 1 ,9500
            urls = []

            for i in range(m * 100, (m + 1) * 100):
                url = 'https://space.bilibili.com/' + str(i)
                urls.append(url)

            def getsource(url):
                payload = {
                    '_': self.datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
                    'mid': url.replace('https://space.bilibili.com/', '')
                }
                ua = random.choice(self.uas)
                self.head['User-Agent'] = ua
                self.head['Referer'] = 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))

                # 设置ip代理
                ip_object = MyIpPools()
                proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
                if proxies == []:   # 避免报错跳出
                    return None

                proxy = proxies['http'][randint(0, len(proxies) - 1)]

                tmp_proxies = {
                    'http': proxy,
                }

                try:
                    jscontent = requests.session().post(
                        url='http://space.bilibili.com/ajax/member/GetInfo',
                        headers=self.head,
                        data=payload,
                        proxies=tmp_proxies,
                        timeout=8
                    ).text
                except Exception:
                    return None

                time2 = time.time()
                try:
                    try:
                        jsDict = json.loads(jscontent)
                        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
                    except:
                        return None

                    if statusJson == True:
                        if 'data' in jsDict.keys():
                            jsData = jsDict['data']
                            try:
                                mid = jsData['mid']
                                name = jsData['name']
                                # sex = jsData['sex']
                                face = jsData['face']
                            except:
                                return None
                            # coins = jsData['coins']
                            # spacesta = jsData['spacesta']
                            # birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                            # place = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                            # description = jsData['description']
                            # article = jsData['article']
                            # playnum = jsData['playNum']
                            # sign = jsData['sign']
                            # level = jsData['level_info']['current_level']
                            # exp = jsData['level_info']['current_exp']
                            # pprint(jsData)

                            if re.compile(r'5d2c92beb774a4bb30762538bb102d23670ae9c0.gif').findall(face) != []:
                                return None

                            if re.compile(r'noface.gif').findall(face) != []:
                                return None

                            if name in self.db_nick_name_list:
                                print('[%d]该nick_name已存在于db中' % self.index)
                                self.index += 1
                                return None

                            print("(索引值为: %d) Succeed: " % self.index + mid + "\t" + str(time2 - time1))

                            bozhu = {
                                'nick_name': name,
                                'sina_type': 'bilibili',
                                'head_img_url': face,
                            }
                            print('---->> ', [name, 'bilibili', face])

                            my_pipeline.insert_into_sina_weibo_table(item=bozhu)
                            gc.collect()

                            # try:
                            #     res = requests.get('https://api.bilibili.com/x/space/navnum?mid=' + str(mid) + '&jsonp=jsonp', headers=head, proxies=tmp_proxies).text
                            #     js_fans_data = json.loads(res)
                            #     following = js_fans_data['data']['following']
                            #     fans = js_fans_data['data']['follower']
                            # except:
                            #     following = 0
                            #     fans = 0
                        else:
                            print('no data now')
                        self.index += 1
                        # try:
                        #     conn = pymysql.connect(
                        #         host='localhost', user='root', passwd='123456', db='bilibili', charset='utf8')
                        #     cur = conn.cursor()
                        #     cur.execute('INSERT INTO bilibili_user_info(mid, name, sex, face, coins, spacesta, \
                        #     birthday, place, description, article, following, fans, playnum, sign, level, exp) \
                        #     VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                        #                 % (
                        #                     mid, name, sex, face, coins, spacesta,
                        #                     birthday, place, description, article,
                        #                     following, fans, playnum, sign, level, exp
                        #                 ))
                        #     conn.commit()
                        # except Exception:
                        #     print("MySQL Error")
                    else:
                        print("Error: " + url)
                except ValueError:
                    pass

            if self.index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                print('正在重置，并与数据库建立新连接中...')
                my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                print('与数据库的新连接成功建立...')

            if my_pipeline.is_connect_success:
                pool = ThreadPool(1)

                try:
                    results = pool.map(getsource, urls)
                except Exception:
                    print('ConnectionError')
                    pool.close()
                    pool.join()
                    time.sleep(3)

                    try:
                        pool = ThreadPool(1)
                        results = pool.map(getsource, urls)
                    except:
                        break

                time.sleep(3)

            else:
                print('数据库连接失败!')
                pass

        try:
            pool.close()
            pool.join()
        except:
            pass

def main_2():
    while True:
        tmp___ = BiLiBiLiUser()
        tmp___.run_forever()

        try:
            del tmp___
        except:
            pass
        gc.collect()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    main_2()

if __name__ == '__main__':
    # if IS_BACKGROUND_RUNNING:
    #     main()
    # else:
    main_2()