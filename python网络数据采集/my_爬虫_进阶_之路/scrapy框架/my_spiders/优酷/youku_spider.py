# coding:utf-8

'''
@author = super_fazai
@File    : youku_spider.py
@connect : superonesfazai@gmail.com
'''

"""
优酷视频爬虫
"""

from gc import collect
import json
from json import dumps
import requests
from fzutils.spider.async_always import *

class YouKuSpider(object):
    def __init__(self):
        self.loop = get_event_loop()
        self._t = lambda : str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        self.ua = get_random_phone_ua()
        self.movie_info_api_base_url = 'http://acs.youku.com/h5/mtop.youku.haixing.play.h5.detail/1.0/'

    async def _get_headers(self):
        return {
            'Origin': 'http://m.youku.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': self.ua,
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
        }

    async def _get_sign(self, _m_h5_tk:str, data:json) -> tuple:
        '''
        获取正确的sign
        :return:
        '''
        app_key = '24679788'
        t = self._t()

        e = _m_h5_tk + '&' + t + '&' + app_key + '&' + data
        sign = md5_encrypt(e)

        return sign, t

    async def _get_sign_and_api_body(self,
                                     base_url,
                                     params,
                                     data:json,
                                     _m_h5_tk='undefine',
                                     session=None) -> tuple:
        sign, t = await self._get_sign(_m_h5_tk=_m_h5_tk, data=data)
        # print(sign, t)
        params.update({  # 添加下面几个query string
            't': t,
            'sign': sign,
            'data': data,
        })
        session = requests.session() if session is None else session
        try:
            response = session.get(url=base_url, headers=await self._get_headers(), params=params,)
            _m_h5_tk = response.cookies.get('_m_h5_tk', '').split('_')[0]
            body = response.content.decode('utf-8')

        except Exception as e:
            print(e)
            _m_h5_tk = ''
            body = ''

        return (_m_h5_tk, session, body)

    async def _get_movie_id(self, movie_url) -> str:
        '''
        获取视频id
        :return: '' 表示出错
        '''
        id = ''
        try:
            id = re.compile('id_(\w+)').findall(movie_url)[0]
        except IndexError:
            print('获取视频id时索引异常!')

        return id

    async def _get_movie_info_api_params(self) -> dict:
        return tuple_or_list_params_2_dict_params((
            ('jsv', '2.4.16'),
            ('appKey', '24679788'),
            # ('t', '1540016600827'),
            # ('sign', 'd16de3308cf43ccf88505efdcb4d0294'),
            ('v', '1.0'),
            ('type', 'originaljson'),
            ('dataType', 'json'),
            ('api', 'mtop.youku.haixing.play.h5.detail'),
        ))

    async def _get_movie_info_api_post_data(self, movie_id) -> dict:
        return {
            'device': 'H5',
            'layout_ver': '100000',
            'system_info': dumps({
                'device': 'H5',
                'pid': '0d7c3ff41d42fcd9',  # 定值
                'guid': '1533803300785Vp7',
                'utdid': '1533803300785Vp7',
                'ver': '1.0.0.0',
                'userAgent': self.ua,
            }),
            'video_id': movie_id
        }

    async def _get_movie_info(self, movie_url) -> dict:
        '''
        获取视频信息
        :return:
        '''
        movie_id = await self._get_movie_id(movie_url)
        if movie_id == '':
            return {}

        params = await self._get_movie_info_api_params()
        # pprint(params)
        data = dumps(await self._get_movie_info_api_post_data(movie_id))

        # 第一次先获取到_m_h5_tk
        _m_h5_tk, s, body = await self._get_sign_and_api_body(base_url=self.movie_info_api_base_url, params=params, data=data)
        # print('_m_h5_tk: {}'.format(_m_h5_tk))
        # print('body: {}'.format(body))
        # 第二次带上_m_h5_tk请求得到数据
        _m_h5_tk, s, body = await self._get_sign_and_api_body(
            base_url=self.movie_info_api_base_url,
            params=params,
            data=data,
            _m_h5_tk=_m_h5_tk, session=s)
        # print('_m_h5_tk: {}'.format(_m_h5_tk))
        # print(body)

        data = json_2_dict(body)
        pprint(data)

        return data

    async def _fck_run(self):
        # movie_info = await self._get_movie_info()
        pass

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = YouKuSpider()
    loop = get_event_loop()
    # movie_url = 'http://m.youku.com/video/id_XMzEyOTc2NTc0NA==.html?spm=a2hww.11359951.m_41795.5~5%212~5~5~5~5~5~A&source=http%3A%2F%2Fwww.youku.com%2F'
    movie_url = 'http://v.youku.com/v_show/id_XMzg1NTAzMDk5Ng==.html?spm=a2hww.11359951.m_26664.5~5!2~5~5~5~5!2~5~5~A'
    res = loop.run_until_complete(_._get_movie_info(movie_url=movie_url))