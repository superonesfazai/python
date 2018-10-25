# coding:utf-8

'''
@author = super_fazai
@File    : hornet_nest_spider.py
@connect : superonesfazai@gmail.com
'''

"""
马蜂窝爬虫
"""

from gc import collect
from requests import session
from fzutils.spider.async_always import *

class HornetNestSpider(object):
    def __init__(self):
        self.loop = get_event_loop()
        self.max_page_num = 60

    async def _get_phone_headers(self):
        return {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://m.mafengwo.cn/',
            'authority': 'm.mafengwo.cn',
            'x-requested-with': 'XMLHttpRequest',
        }

    async def _get_pc_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Referer': 'http://www.mafengwo.cn/flight/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _get_one_page_recommend_strategy_list(self, page_num:int) -> list:
        '''
        获取一页推荐攻略列表
        :return:
        '''
        params = (
            ('category', 'get_info_flow_list'),
            ('page', str(page_num)),
        )
        url = 'https://m.mafengwo.cn/'
        article_list = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_phone_headers(), params=params))\
            .get('data', {}).get('list', [])

        return article_list

    async def _get_all_recommend_strategy_list(self) -> list:
        '''
        获取所有推荐攻略列表
        :return:
        '''
        tasks = []
        for page_num in range(0, self.max_page_num + 1):
            print('[+] create task: {}'.format(page_num))
            tasks.append(self.loop.create_task(self._get_one_page_recommend_strategy_list(page_num=page_num)))

        all_strategy_list = []
        all_res = await async_wait_tasks_finished(tasks=tasks)
        for item in all_res:
            all_strategy_list += item
        pprint(all_strategy_list)
        print('获取到的推荐攻略总个数为: {}'.format(len(all_strategy_list)))

        return all_strategy_list

    async def _get_city_name_for_short(self, city_name:str) -> dict:
        '''
        获取city的英文缩写(eg: '杭州' -> 'HGH)
        :param city_name:
        :return:
        '''
        params = (
            ('filter[prefix]', city_name),
        )
        # 非代理模式有数据
        with session() as s:
            ex = json_2_dict(s.get(url='http://www.mafengwo.cn/flight/rest/citySuggest/', headers=await self._get_pc_headers(), params=params).text)\
                .get('data', {}).get('ex', [])

        _short = ''
        try:
            _short = ex[0].get('c', '')
        except IndexError:
            print('获取到的ex为空list!')

        return {
            'city_name': city_name,
            'short': _short,
        }

    async def _get_city_code(self, start_city, end_city, all_res):
        '''
        从结果集中提取code
        :param start_city:
        :param end_city:
        :param all_res:
        :return:
        '''
        start_city_code, end_city_code = '', ''
        for item in all_res:
            city_name = item.get('city_name', '')
            short = item.get('short', '')
            if start_city == city_name:
                start_city_code = short

            if end_city == city_name:
                end_city_code = short

        return start_city_code, end_city_code

    async def _search_flights(self, start_city:str, end_city:str, departure_date:str, ota_id:str='102'):
        '''
        航班搜索
        :param start_city: 出发城市
        :param end_city: 目的地
        :param departure_date: 出发日期 eg: '2018-10-26'
        :param ota_id: '102' or '101'
        :return:
        '''
        # TODO m站sign签名加密 转向 爬取pc站的
        # 先获取city code
        tasks = [self.loop.create_task(self._get_city_name_for_short(city_name=item)) for item in (start_city, end_city)]
        all_res = await async_wait_tasks_finished(tasks=tasks)
        # pprint(all_res)
        start_city_code, end_city_code = await self._get_city_code(start_city, end_city, all_res)
        print('{}:{}, {}:{}'.format(start_city, start_city_code, end_city, end_city_code))

        params = (
            ('filter[departCity]', start_city),
            ('filter[departCode]', start_city_code),
            ('filter[destCity]', end_city),
            ('filter[destCode]', end_city_code),
            ('filter[departDate]', departure_date),
            ('filter[destDate]', ''),
            ('filter[otaId]', ota_id),
        )
        url = 'http://www.mafengwo.cn/flight/rest/flightlist/'
        with session() as s:
            data = json_2_dict(s.get(url=url, headers=await self._get_pc_headers(), params=params).text)\
                .get('data', {}).get('ex', {}).get('flights', [])
            # pprint(data)

        return data

    async def _fck_run(self):
        # await self._get_all_recommend_strategy_list()

        start_city = '杭州'
        end_city = '北京'
        departure_date = '2018-10-26'

        res = await self._search_flights(start_city=start_city, end_city=end_city, departure_date=departure_date)
        print('发现航班数: {}'.format(len(res)))

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = HornetNestSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())