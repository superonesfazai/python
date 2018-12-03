# coding:utf-8

'''
@author = super_fazai
@File    : delicious_food_spider.py
@connect : superonesfazai@gmail.com
'''

"""
美团美食爬虫
"""

from gc import collect
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

class MTDFSpider(AsyncCrawler):
    """美团美食spider[当前定位]"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool,
        )
        self.concurrency = 16

    async def _get_phone_headers(self):
        return {
            'Origin': 'http://meishi.meituan.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            # 'Referer': 'http://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'x-requested-with': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        }

    async def _get_df_nearby_one_page_info(self, **kwargs):
        '''
        获取美食附近单页商家信息
        :return:
        '''
        offset:int = kwargs['offset']

        headers = await self._get_phone_headers()
        headers.update({
            'Referer': 'http://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt/homepage/category1/1',
        })
        data = dumps({
            'app': '',
            'areaId': 0,
            'cateId': 1,
            'deal_attr_23': '',
            'deal_attr_24': '',
            'deal_attr_25': '',
            'limit': 15,
            'lineId': 0,
            'offset': offset,  # 0, 15, 30, 45
            'optimusCode': 10,
            'originUrl': 'http://meishi.meituan.com/i/?ci=50&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'partner': 126,
            'platform': 3,
            'poi_attr_20033': '',
            'poi_attr_20043': '',
            'riskLevel': 1,
            'sort': 'default',
            'stationId': 0,
            # 'uuid': '4ad8035a0bb84f15a56c.1543547045.1.0.0',
            'version': '8.2.0'
        })
        url = 'http://meishi.meituan.com/i/api/channel/deal/list'
        # 非阻塞(一并发就跳验证码, 可采用driver, 模拟滑动, 再解析最后的html)
        body = await unblock_request(method='post', url=url, headers=headers, data=data, ip_pool_type=self.ip_pool_type, num_retries=3)
        # print(body)

        # body = Requests.get_url_body(method='post', url=url, headers=headers, data=data, ip_pool_type=self.ip_pool_type, num_retries=3)
        # print(body)
        data = json_2_dict(body).get('data', {}).get('poiList', {}).get('poiInfos', [])
        # pprint(data)
        label, success_or_fail = ('+', 'success') if data != [] else ('-', 'fail')
        print('[{}] task[where offset:{}] {}'.format(label, offset, success_or_fail))

        return data

    async def _get_df_nearby_all_seller_info(self) -> list:
        '''
        获取美食附近所有商家信息
        :return:
        '''
        tasks = []
        RANGE = range(0, 200, 15)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=RANGE, step=self.concurrency)
        all_res = []
        while True:
            try:
                next_slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            for offset in next_slice_params_list:
                # offset步长为15
                print('create task[where offset:{}]...'.format(offset))
                tasks.append(self.loop.create_task(self._get_df_nearby_one_page_info(offset=offset)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            for item in one_res:
                for i in item:
                    if i != []:
                        all_res.append(i)

        return all_res

    async def _fck_run(self):
        nearby_all_seller_info_list = await self._get_df_nearby_all_seller_info()
        print('总商家个数: {}'.format(len(nearby_all_seller_info_list)))

    def __del__(self):
        try:
            del self.loop
        except:
            pass

        collect()

if __name__ == '__main__':
    _ = MTDFSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
