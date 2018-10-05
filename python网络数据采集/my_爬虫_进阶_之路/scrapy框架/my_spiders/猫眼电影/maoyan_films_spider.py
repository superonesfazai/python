# coding:utf-8

'''
@author = super_fazai
@File    : maoyan_films_spider.py
@connect : superonesfazai@gmail.com
'''

"""
猫眼电影爬虫
"""

from gc import collect
from asyncio import get_event_loop, wait
from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_phone_ua
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import get_shanghai_time, datetime_to_timestamp
from fzutils.common_utils import get_random_int_number
from fzutils.aio_utils import async_wait_tasks_finished

class MaoYanFilmsSpider(object):
    def __init__(self):
        self.movies_id_list = []
        self.movies_info_list = []
        self.loop = get_event_loop()
        self.city_id = '50'

    async def _get_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _get_being_on_the_heat(self) -> list:
        '''
        获取正在热映的电影list
        :return:
        '''
        headers = await self._get_headers()
        headers.update({
            'Referer': 'http://m.maoyan.com/',
        })
        params = (
            ('token', ''),
        )
        url = 'http://m.maoyan.com/ajax/movieOnInfoList'
        data = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params, cookies=None))
        # pprint(data)
        if data == {}:
            print('获取到的data为空dict, 跳过!')
            return []

        self.movies_id_list = data.get('movieIds', [])
        print('正在热映的电影个数: {}'.format(len(self.movies_id_list)))
        movies_list = data.get('movieList', [])
        [self.movies_info_list.append(item) for item in movies_list]
        [self.movies_id_list.remove(item.get('id')) for item in self.movies_info_list]
        print('待抓取的热映电影个数: {}'.format(len(self.movies_id_list)))

        # 抓取剩余所有movies info
        url = 'http://m.maoyan.com/ajax/moreComingList'
        params = (
            ('token', ''),
            # ('movieIds', '342412,1208342,1198213,1203575,1235235,1217434,1203098,1207707,1200486,1229963'),
            ('movieIds', ','.join([str(i) for i in self.movies_id_list])),
        )
        coming = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params, cookies=None)).get('coming', [])
        print('抓取到的个数为: {}'.format(len(coming)))
        [self.movies_info_list.append(item) for item in coming]
        print('总共采集到正在热映的电影个数: {}'.format(len(self.movies_info_list)))

        return self.movies_info_list

    async def _get_one_movie_detail_info(self, movie_id) -> dict:
        '''
        获取一个电影内容的详细信息
        :return:
        '''
        headers = await self._get_headers()
        params = (
            ('movieId', str(movie_id)),
        )
        data = json_2_dict(Requests.get_url_body(url='http://m.maoyan.com/ajax/detailmovie', headers=headers, params=params, cookies=None)).get('detailMovie', {})

        return data

    async def _get_this_movie_cinemas_info(self, movie_id, movie_day, city_id) -> dict:
        '''
        得到该电影的所有影院信息
        :return:
        '''
        t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        headers = await self._get_headers()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://m.maoyan.com/cinema/movie/{}?$from=canary'.format(movie_id),
        })
        params = (
            ('forceUpdate', t),
        )
        data = {
            'movieId': str(movie_id),
            'day': str(movie_day),      # 2018-10-05
            'offset': '20',
            'limit': '20',
            'districtId': '-1',
            'lineId': '-1',
            'hallType': '-1',
            'brandId': '-1',
            'serviceId': '-1',
            'areaId': '-1',
            'stationId': '-1',
            'item': '',
            'updateShowDay': 'false',
            'reqId': t,
            'cityId': city_id,
        }
        data = json_2_dict(Requests.get_url_body(url='http://m.maoyan.com/ajax/movie', headers=headers, params=params, cookies=None, data=data))
        # print(data)

        return data

    async def _fck_run(self):
        all_movies_info_list = await self._get_being_on_the_heat()
        # pprint(all_movies_info_list)
        tasks = []
        for item in all_movies_info_list:
            movie_id = item.get('id')
            tasks.append(self.loop.create_task(self._get_one_movie_detail_info(movie_id=movie_id)))
            print('[+] 创建task {}'.format(movie_id))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        # pprint(all_res)
        print('总长度为: {}'.format(len(all_res)))
        self.movies_info_list = all_res

        # TODO 下面就先不写了

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = MaoYanFilmsSpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())