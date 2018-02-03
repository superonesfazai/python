# coding:utf-8

'''
@author = super_fazai
@File    : bilibili_user.py
@Time    : 2018/1/10 10:03
@connect : superonesfazai@gmail.com
'''

import sys
# sys.path.append('....')
# sys.path.append('~/myFiles/python/my_flask_server')
sys.path.append('/Users/afa/myFiles/codeDoc/PythonDoc/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/阿里1688_淘宝_天猫_京东_折800_卷皮_拼多多_蜜芽_蘑菇街/my_flask_server/')

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

from requests.exceptions import ReadTimeout

reload(sys)

# 全局变量
index = 1

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()

def LoadUserAgents(uafile):
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

def get_proxy_ip_from_ip_pool():
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

def main_2():
    uas = LoadUserAgents("user_agents.txt")
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://space.bilibili.com/45388',
        'Origin': 'http://space.bilibili.com',
        'Host': 'space.bilibili.com',
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }

    time1 = time.time()

    my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

    for m in range(1, 9500):  # 1 ,9500
        urls = []

        for i in range(m * 100, (m + 1) * 100):
            url = 'https://space.bilibili.com/' + str(i)
            urls.append(url)

        def getsource(url):
            global index
            payload = {
                '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
                'mid': url.replace('https://space.bilibili.com/', '')
            }
            ua = random.choice(uas)
            head = {
                'User-Agent': ua,
                'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(
                    random.randint(10000, 50000))
            }

            # 设置ip代理
            proxies = get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
            proxy = proxies['http'][randint(0, len(proxies) - 1)]

            tmp_proxies = {
                'http': proxy,
            }

            try:
                jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo',
                          headers=head,
                          data=payload,
                          proxies=tmp_proxies,
                          timeout=8) \
                    .text
            except ReadTimeout:
                return None

            time2 = time.time()
            try:
                jsDict = json.loads(jscontent)
                statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
                if statusJson == True:
                    if 'data' in jsDict.keys():
                        jsData = jsDict['data']
                        mid = jsData['mid']
                        name = jsData['name']
                        # sex = jsData['sex']
                        face = jsData['face']
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

                        print("(索引值为: %d) Succeed: " % index + mid + "\t" + str(time2 - time1))

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
                    index += 1
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

        if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
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
                pool = ThreadPool(1)
                results = pool.map(getsource, urls)

            time.sleep(3)
        else:
            print('数据库连接失败!')
            pass

    try:
        pool.close()
        pool.join()
    except:
        pass

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
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        main_2()