# coding:utf-8

'''
@author = super_fazai
@File    : mogujie_pintuan.py
@Time    : 2018/2/3 16:26
@connect : superonesfazai@gmail.com
'''

import json
import re
import time
from pprint import pprint
import gc
from time import sleep

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    IS_BACKGROUND_RUNNING,
    MOGUJIE_SLEEP_TIME,
    PHANTOMJS_DRIVER_PATH,)
import datetime
from mogujie_parse import MoGuJieParse

from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
)
from fzutils.linux_utils import daemon_init
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_phantomjs import MyPhantomjs

class MoGuJiePinTuan(object):
    def __init__(self):
        self._set_headers()
        self._set_fcid_dict()

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'api.mogujie.com',
            'Referer': 'https://pintuan.mogujie.com/ptpt/app/pd?acm=3.mce.1_10_1fvsk.51827.0.mUTadqIzS9Pbg.m_370494-pos_2-mf_4537_796033&ptp=m1._mf1_1239_4537._keyword_51827.0.xLt0G92',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _set_fcid_dict(self):
        self.fcid_dict = {
            '女装': 10053171,
            # '精选': 10053172,
            '男友': 10053173,
            '内衣': 10053174,
            '女鞋': 10053175,
            '包包': 10053176,
            '美妆': 10053177,
            '生活': 10053178,
            '配饰': 10053179,
            '母婴': 10053180,
            '食品': 10053181,
        }

    def get_pintuan_goods_info(self):
        '''
        模拟构造得到data的url，得到近期所有的限时拼团商品信息
        :return: None
        '''
        goods_list = []

        '''
        方法一: 蘑菇街手机版拼团商品列表获取签名暂时无法破解，所以不用手机端的方法来获取数据
        '''
        # mw_appkey = '100028'
        # mw_t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
        # mw_uuid = '956bf265-90a4-45b0-bfa8-31040782f99e'
        # mw_ttid = 'NMMain%40mgj_h5_1.0'
        #
        # _ = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位
        #
        # data = {
        #     "pid": "93745",
        #     "platform": "m",
        #     "cKey": "mwp_mait",
        #     "fcid": "",
        # }
        #
        # params = {
        #     'data': data
        # }
        #
        # # https://api.mogujie.com/h5/mwp.darwin.get/3/?mw-appkey=100028&mw-t=1517647409632&mw-uuid=956bf265-90a4-45b0-bfa8-31040782f99e&mw-ttid=NMMain%40mgj_h5_1.0&mw-sign=abde92f778e47bce98a3ed25fd71eb1a&data=%7B%22pid%22%3A%2293745%22%2C%22platform%22%3A%22m%22%2C%22cKey%22%3A%22mwp_mait%22%2C%22fcid%22%3A%22%22%7D&callback=mwpCb1&_=1517647409648
        # # https://api.mogujie.com/h5/mwp.darwin.get/3/?mw-appkey=100028&mw-t=1517647893930&mw-uuid=956bf265-90a4-45b0-bfa8-31040782f99e&mw-ttid=NMMain%40mgj_h5_1.0&callback=mwpCb1&_=1517647893748&data=pid&data=platform&data=cKey&data=fcid
        #
        # tmp_url = 'https://api.mogujie.com/h5/mwp.darwin.get/3/?mw-appkey={0}&mw-t={1}&mw-uuid={2}&mw-ttid={3}&callback=mwpCb1&_={4}'.format(
        #     mw_appkey, mw_t, mw_uuid, mw_ttid, _
        # )
        #
        # # 设置代理ip
        # ip_object = MyIpPools()
        # self.proxies = ip_object.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        # self.proxy = self.proxies['http'][randint(0, len(self.proxies) - 1)]
        #
        # tmp_proxies = {
        #     'http': self.proxy,
        # }
        #
        # try:
        #     response = requests.post(tmp_url, headers=self.headers, data=data, proxies=tmp_proxies, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
        #     body = response.content.decode('utf-8')
        #     print(body)
        # except Exception:
        #     print('requests.get()请求超时....')
        #     print('data为空!')
        #     self.result_data = {}  # 重置下，避免存入时影响下面爬取的赋值
        #     return {}

        '''
        方法二: 通过pc端来获取拼团商品列表
        '''
        self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)
        for key in self.fcid_dict:
            print('正在抓取的分类为: ', key)
            for index in range(1, 100):
                if index % 5 == 0:
                    try: del self.my_phantomjs
                    except: pass
                    gc.collect()
                    self.my_phantomjs = MyPhantomjs(executable_path=PHANTOMJS_DRIVER_PATH)

                fcid = self.fcid_dict[key]
                tmp_url = 'http://list.mogujie.com/search?page={0}&fcid={1}&algoKey=pc_tuan_book_pop&cKey=pc-tuan'.format(
                    str(index), fcid
                )
                # requests请求数据被过滤(起初能用)，改用phantomjs
                # body = MyRequests.get_url_body(url=tmp_url, headers=self.headers, had_referer=True)
                body = self.my_phantomjs.use_phantomjs_to_get_url_body(url=tmp_url)
                # print(body)

                try:
                    body = re.compile(r'<pre.*?>(.*?)</pre>').findall(body)[0]
                    tmp_data = json.loads(body)
                except:
                    print('json.loads转换body时出错, 请检查')
                    continue

                if tmp_data.get('result', {}).get('wall', {}).get('docs', []) == []:
                    # 表示拼团数据为空则跳出循环
                    break

                # pprint(tmp_data)
                # print(tmp_data)

                tmp_item_list = tmp_data.get('result', {}).get('wall', {}).get('docs', [])
                # print(tmp_item_list)
                # pprint(tmp_item_list)

                begin_time_timestamp = int(time.time())     # 开始拼团的时间戳
                item_list = [{
                    'goods_id': item.get('tradeItemId', ''),
                    'pintuan_time': {
                        'begin_time': timestamp_to_regulartime(timestamp=begin_time_timestamp),
                        'end_time': timestamp_to_regulartime(self.get_pintuan_end_time(begin_time_timestamp, item.get('leftTimeOrg', ''))),
                    },
                    'all_sell_count': str(item.get('salesVolume', 0)),
                    'fcid': fcid,
                    'page': index,
                    'sort': key,
                } for item in tmp_item_list]
                print(item_list)

                for item_1 in item_list:
                    goods_list.append(item_1)

                sleep(MOGUJIE_SLEEP_TIME)

        # 处理goods_list数据
        print(goods_list)
        self.deal_with_data(goods_list)
        sleep(5)

    def deal_with_data(self, *params):
        '''
        处理并存储相关拼团商品的数据
        :param params: 待传参数
        :return:
        '''
        goods_list = params[0]

        mogujie = MoGuJieParse()
        my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

        if my_pipeline.is_connect_success:
            sql_str = r'select goods_id, miaosha_time, fcid, page from dbo.mogujie_pintuan where site_id=23'
            db_goods_id_list = [item[0] for item in list(my_pipeline._select_table(sql_str=sql_str))]
            print(db_goods_id_list)

            for item in goods_list:
                if item.get('goods_id', '') in db_goods_id_list:
                    print('该goods_id已经存在于数据库中, 此处跳过')
                    pass

                else:
                    goods_id = str(item.get('goods_id', ''))
                    tmp_url = 'https://shop.mogujie.com/detail/' + str(goods_id)

                    mogujie.get_goods_data(goods_id=str(goods_id))
                    goods_data = mogujie.deal_with_data()

                    if goods_data == {}:  # 返回的data为空则跳过
                        pass

                    else:  # 否则就解析并且插入
                        # 规范化
                        tmp_price_info_list = goods_data['price_info_list']
                        price_info_list = [{
                            'spec_value': item_4.get('spec_value'),
                            'pintuan_price': item_4.get('detail_price'),
                            'normal_price': item_4.get('normal_price'),
                            'img_url': item_4.get('img_url'),
                            'rest_number': item_4.get('rest_number'),
                        } for item_4 in tmp_price_info_list]

                        goods_data['price_info_list'] = price_info_list
                        goods_data['goods_url'] = tmp_url
                        goods_data['goods_id'] = str(goods_id)
                        goods_data['pintuan_time'] = item.get('pintuan_time', {})
                        goods_data['pintuan_begin_time'], goods_data['pintuan_end_time'] = self.get_pintuan_begin_time_and_pintuan_end_time(pintuan_time=item.get('pintuan_time', {}))
                        goods_data['all_sell_count'] = item.get('all_sell_count', '')
                        goods_data['fcid'] = str(item.get('fcid'))
                        goods_data['page'] = str(item.get('page'))
                        goods_data['sort'] = str(item.get('sort', ''))

                        # pprint(goods_data)
                        # print(goods_data)
                        _r = mogujie.insert_into_mogujie_pintuan_table(data=goods_data, pipeline=my_pipeline)
                        if _r:  # 更新
                            db_goods_id_list.append(goods_id)
                            db_goods_id_list = list(set(db_goods_id_list))

                        sleep(MOGUJIE_SLEEP_TIME)  # 放慢速度

        else:
            print('数据库连接失败，此处跳过!')
            pass

        try:
            del mogujie
        except:
            pass
        gc.collect()

    def get_pintuan_end_time(self, begin_time, left_time):
        '''
        处理并得到拼团结束时间
        :param begin_time: 秒杀开始时间戳
        :param left_time: 剩余时间字符串
        :return: end_time 时间戳(int)
        '''
        # 'leftTimeOrg': '6天13小时'
        # 'leftTimeOrg': '13小时57分'

        had_day = re.compile(r'天').findall(left_time)
        had_hour = re.compile(r'小时').findall(left_time)
        had_min = re.compile(r'分').findall(left_time)

        tmp = re.compile(r'\d+').findall(left_time)
        if had_day != [] and had_hour != []:    # left_time 格式为 '6天13小时'
            day, hour, min = int(tmp[0]), int(tmp[1]), 0

        elif had_day == [] and had_hour != []:  # left_time 格式为 '13小时57分'
            day, hour, min = 0, int(tmp[0]), int(tmp[1])

        elif had_day == [] and had_hour == []:  # left_time 格式为 '36分'
            print('left_time = ', left_time)
            day, hour, min = 0, 0, int(tmp[0])

        else:               # 无天, 小时, 分
            print('day, hour, min = 0, 0, 0', 'left_time = ', left_time)
            day, hour, min = 0, 0, 0

        left_end_time_timestamp = \
            day * 24 * 60 * 60 + \
            hour * 60 * 60 + \
            min * 60

        return begin_time + left_end_time_timestamp

    def get_pintuan_begin_time_and_pintuan_end_time(self, pintuan_time):
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

    def __del__(self):
        try: del self.my_phantomjs
        except: pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        mogujie_pintuan = MoGuJiePinTuan()
        mogujie_pintuan.get_pintuan_goods_info()
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