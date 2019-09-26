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

from settings import (
    IS_BACKGROUND_RUNNING,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from multiplex_code import _get_new_db_conn
from taobao_parse import TaoBaoLoginAndParse

from sql_str_controller import (
    tb_select_str_6,
)
from fzutils.spider.async_always import *

class TaoBaoTianTianTeJia(AsyncCrawler):
    def __init__(self, logger=None):
        AsyncCrawler.__init__(
            self,
            logger=logger,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/天天特价/',)
        self._set_headers()
        self.msg = ''
        self._set_main_sort()
        # 最大截止抓取页(原先是300)
        self.max_crawl_page_num = 5
        self.is_real_times_update_call = True

    def _set_headers(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'h5api.m.taobao.com',
            'User-Agent': get_random_pc_ua(),  # 随机一个请求头
        }

    def _set_main_sort(self):
        self.main_sort = {
            '495000': ['时尚女装', 'mtopjsonp2'],
            '496000': ['潮流男装', 'mtopjsonp4'],
            '499000': ['性感内衣', 'mtopjsonp5'],
            '508000': ['家居百货', 'mtopjsonp6'],
            '502000': ['品质母婴', 'mtopjsonp7'],
            '503000': ['食品饮料', 'mtopjsonp8'],
            '497000': ['男女鞋品', 'mtopjsonp9'],  # ['497000', '498000']
            '498000': ['男女鞋品', 'mtopjsonp9'],
            '505000': ['美容美妆', 'mtopjsonp10'],
            '500000': ['箱包配饰', 'mtopjsonp11'],  # ['500000', '501000']
            '501000': ['箱包配饰', 'mtopjsonp11'],
            '504000': ['数码电器', 'mtopjsonp12'],
            '506000': ['户外运动', 'mtopjsonp13'],  # ['506000', '507000']
            '507000': ['户外运动', 'mtopjsonp13'],
        }

    async def get_all_goods_list(self):
        '''
        模拟构造得到天天特价的所有商品的list, 并且解析存入每个
        :return: sort_data  类型list
        '''
        sort_data = []
        for category in self.main_sort.keys():
            self.lg.info('正在抓取的分类为: ' + self.main_sort[category][0])
            for current_page in range(1, self.max_crawl_page_num, 1):
                self.lg.info('正在抓取第 ' + str(current_page) + ' 页...')

                body = await self.get_one_api_body(
                    current_page=current_page,
                    category=category)
                if body == '':
                    self.msg = '获取到的body为空str! 出错category为: ' + category
                    self.lg.error(self.msg)
                    continue

                try:
                    body = re.compile(r'\((.*?)\)').findall(body)[0]
                except IndexError:
                    self.msg = 're筛选body时出错, 请检查! 出错category为: ' + category
                    self.lg.error(self.msg)
                    continue
                tmp_sort_data = await self.get_sort_data_list(body=body)
                if tmp_sort_data == 'no items':
                    break

                # self.lg.info(tmp_sort_data)
                sort_data.append({
                    'category': category,
                    'current_page': current_page,
                    'data': tmp_sort_data,
                })

            #     break   # 下面2行用于测试, 避免全抓完太慢
            # break
        self.lg.info(str(sort_data))
        collect()

        return sort_data

    async def deal_with_all_goods_id(self):
        '''
        获取每个详细分类的商品信息
        :return: None
        '''
        sort_data = await self.get_all_goods_list()
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        index = 1
        if sql_cli.is_connect_success:
            # 普通sql_server连接(超过3000无返回结果集)
            self.lg.info('正在获取天天特价db原有goods_id, 请耐心等待...')
            db_ = list(sql_cli._select_table(sql_str=tb_select_str_6))
            db_goods_id_list = [[item[0], item[2]] for item in db_]
            self.lg.info('获取完毕!!!')
            # print(db_goods_id_list)
            db_all_goods_id = [i[0] for i in db_goods_id_list]

            for item in sort_data:
                tejia_goods_list = await self.get_tiantiantejia_goods_list(data=item.get('data', []))
                self.lg.info(str(tejia_goods_list))

                for tmp_item in tejia_goods_list:
                    if tmp_item.get('goods_id', '') in db_all_goods_id:    # 处理如果该goods_id已经存在于数据库中的情况
                        tmp_end_time = ''
                        try:
                            tmp_end_time = [i[1] for i in db_goods_id_list if tmp_item.get('goods_id', '')==i[0]][0]
                            # print(tmp_end_time)
                        except:
                            pass

                        if tmp_end_time != '' \
                                and tmp_end_time < get_shanghai_time():
                            '''
                            * 处理由常规商品又转换为天天特价商品 *
                            '''
                            self.lg.info('##### 该商品由常规商品又转换为天天特价商品! #####')
                            # 先删除，再重新插入
                            _ = await sql_cli.delete_taobao_tiantiantejia_expired_goods_id(
                                goods_id=tmp_item.get('goods_id', ''),
                                logger=self.lg)
                            if _ is False:
                                continue

                            index = await self.insert_into_table(
                                tmp_item=tmp_item,
                                category=item['category'],
                                current_page=item['current_page'],
                                sql_cli=sql_cli,
                                index=index,)

                        else:
                            self.lg.info('该goods_id已经存在于数据库中, 此处跳过')
                            pass

                    else:
                        sql_cli = await _get_new_db_conn(
                            db_obj=sql_cli,
                            index=index,
                            logger=self.lg,)
                        if sql_cli.is_connect_success:
                            index = await self.insert_into_table(
                                tmp_item=tmp_item,
                                category=item['category'],
                                current_page=item['current_page'],
                                sql_cli=sql_cli,
                                index=index,)

                        else:
                            self.lg.error('数据库连接失败!')
                            pass

        else:
            self.lg.error('数据库连接失败!')
            pass
        collect()

        return True

    async def insert_into_table(self, tmp_item, category, current_page, sql_cli, index):
        '''
        执行插入到淘宝天天特价的操作
        :param tmp_item:
        :param category:
        :param current_page:
        :param sql_cli:
        :param index:
        :return: index 加1
        '''
        tmp_url = 'https://item.taobao.com/item.htm?id=' + str(tmp_item.get('goods_id', ''))
        taobao = TaoBaoLoginAndParse(
            logger=self.lg,
            is_real_times_update_call=self.is_real_times_update_call)
        goods_id = taobao.get_goods_id_from_url(tmp_url)
        try:
            taobao.get_goods_data(goods_id=goods_id)
            goods_data = taobao.deal_with_data(goods_id=goods_id)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            index += 1

            return index

        if goods_data != {}:
            goods_data['goods_id'] = tmp_item.get('goods_id', '')
            goods_data['goods_url'] = tmp_url
            goods_data['schedule'] = [{
                'begin_time': tmp_item.get('start_time', ''),
                'end_time': tmp_item.get('end_time', ''),
            }]
            goods_data['tejia_begin_time'], goods_data['tejia_end_time'] = get_miaosha_begin_time_and_miaosha_end_time(miaosha_time=goods_data.get('schedule', [])[0])
            goods_data['block_id'] = str(category)
            goods_data['tag_id'] = str(current_page)
            goods_data['father_sort'] = self.main_sort[category][0]
            goods_data['child_sort'] = ''
            # pprint(goods_data)

            await taobao.insert_into_taobao_tiantiantejia_table(data=goods_data, pipeline=sql_cli)
        else:
            await async_sleep(4)  # 否则休息4秒
        index += 1
        # await async_sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)

        return index

    async def get_one_api_body(self, **kwargs):
        '''
        获取一个api接口的数据
        :param kwargs:
        :return:
        '''
        current_page = kwargs.get('current_page')
        category = kwargs.get('category')

        base_url = 'https://h5api.m.taobao.com/h5/mtop.ju.data.get/1.0/'

        data = dumps({
            'bizCode': 'tejia_004',
            'currentPage': current_page,
            'optStr': dumps({
                # 切记: priceScope这里不需要json.dumps, 否则请求不到数据
                'priceScope': {
                    "lowerLimit": 1,
                    "upperLimit": 9999,
                },
                'category': [category],
                'includeForecast': 'false',
                'topItemIds': [],
            }),
            'pageSize': 20,
            'salesSites': 9,  # 这为默认推荐
        })

        params = {
            "jsv": "2.4.8",
            "appKey": "12574478",
            # "t": t,
            # "sign": sign,
            "api": "mtop.ju.data.get",
            "v": "1.0",
            "type": "jsonp",
            "dataType": "jsonp",
            "callback": self.main_sort[category][1],
            "data": data,
        }

        result_1 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            logger=self.lg,
            ip_pool_type=self.ip_pool_type
        )
        _m_h5_tk = result_1[0]

        if _m_h5_tk == '':
            self.msg = '获取到的_m_h5_tk为空str! 出错category为: ' + category
            self.lg.error(self.msg)
            return ''

        # 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
        result_2 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            _m_h5_tk=_m_h5_tk,
            session=result_1[1],
            logger=self.lg,
            ip_pool_type=self.ip_pool_type,)
        body = result_2[2]
        # self.lg.info(str(body))

        return body

    async def get_sort_data_list(self, body):
        '''
        获取到分类的list(对应name和extQuery的值的list)
        :param body: 待转换的json
        :return: 'no items' 表示没有items了 | sort_data  类型 list
        '''
        sort_data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg,)

        if sort_data.get('data', {}).get('data', {}).get('TjGetItems', '') == 'tejia_004 error : no items':
            return 'no items'

        sort_data = sort_data.get('data', {}).get('data', {}).get('itemList', [])

        return sort_data

    async def get_tiantiantejia_goods_list(self, data):
        '''
        将data转换为需求的list
        :param data:
        :return: a list
        '''
        tejia_goods_list = []
        if data != []:
            # 处理得到需要的数据
            try:
                tejia_goods_list = [{
                    'goods_id': item.get('baseinfo', {}).get('itemId', ''),
                    'start_time': timestamp_to_regulartime(int(item.get('baseinfo', {}).get('ostime', '')[0:10])),
                    'end_time': timestamp_to_regulartime(int(item.get('baseinfo', {}).get('oetime', '')[0:10])),
                } for item in data]
            except Exception as e:
                self.lg.exception(e)

        return tejia_goods_list

    def __del__(self):
        try:
            del self.lg
            del self.msg
            del self.loop
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        tb = TaoBaoTianTianTeJia()
        loop = get_event_loop()
        loop.run_until_complete(tb.deal_with_all_goods_id())
        try:
            del tb
            del loop
        except:
            pass
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60 * 5)

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()