# coding:utf-8

'''
@author = super_fazai
@File    : maoyan_films_spider.py
@connect : superonesfazai@gmail.com
'''

"""
猫眼电影爬虫(可获取影院信息，电影信息，票房[字体反爬])
"""

import re
from gc import collect
from asyncio import get_event_loop
from pprint import pprint
from fontTools.ttLib import TTFont
from scrapy.selector import Selector
from xmltodict import parse

from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import (
    get_random_phone_ua,
    get_random_pc_ua,)
from fzutils.common_utils import (
    json_2_dict,
    save_base64_img_2_local,)
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,)
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
        '''
        获取电影及其影院信息
        :return:
        '''
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

    async def _get_char_dict(self, font_path, font_xml_save_path) -> dict:
        '''
        获取字符字典
        :param font_path: 字体路径(.tff/.otf)
        :param font_xml_save_path: font文件转xml后的存储路径(用于分析规则)
        :return:
        '''
        # 补充一点: 就是你每次访问加载的字体文件中的字符的编码可能是变化的，就是说网站有多套的字体文件。(采用: 动态加载反爬)
        # 可利用fontTools可以获取每一个字符对象，这个对象你可以简单的理解为保存着这个字符的形状信息。而且编码可以作为这个对象的id，具有一一对应的关系。

        # 像猫眼电影，虽然字符的编码是变化的，但是字符的形状是不变的，也就是说这个对象是不变的。
        font = TTFont(font_path)
        # 字体文件->xml格式，以便打开查看里面的数据结构。
        # xml文件中, 这里我们用到的标签是<GlyphOrder...>和<glyf...>
        # <GlyphOrder...> 内包含着所有编码信息
        # <glyf...> 内包含着每一个字符对象<TTGlyph>
        # <TTGlyph>对象，里面是一些坐标点的信息，用来描绘字体形状的
        font.saveXML(fileOrPath=font_xml_save_path)

        # 获取所有字符的对象，去除第一个和最后一个
        obj_list = font.getGlyphNames()[1:-1]  # eg: ['uniE19B', ...]
        # 获取所有编码，去除前2个
        uni_list = font.getGlyphOrder()[2:]
        # pprint(obj_list)
        # pprint(uni_list)

        # 字典
        '''跟源代码中对应验证一下可以得出他们的位置对应关系如下。'''
        """
        # 下面是变化的(错误)
        <GlyphOrder>
            <!-- The 'id' attribute is only for humans; it is ignored when parsed. -->
            <GlyphID id="0" name="glyph00000" />
            <GlyphID id="1" name="x" />
            <GlyphID id="2" name="uniEC55" />	2(值)
            <GlyphID id="3" name="uniF1CF" />	6
            <GlyphID id="4" name="uniE347" />	8
            <GlyphID id="5" name="uniF660" />	5
            <GlyphID id="6" name="uniEC3F" />	4
            <GlyphID id="7" name="uniEC2E" />	9
            <GlyphID id="8" name="uniEBDC" />	1
            <GlyphID id="9" name="uniE366" />	0
            <GlyphID id="10" name="uniECC7" />	7
            <GlyphID id="11" name="uniE1FD" />	3
        </GlyphOrder>
        # 正确顺序位置在
        <hmtx>
            <mtx name="glyph00000" width="1024" lsb="0" />
            <mtx name="uniE0F2" width="556" lsb="0" />
            <mtx name="uniE59B" width="556" lsb="0" />
            <mtx name="uniE796" width="556" lsb="0" />
            <mtx name="uniE8DC" width="556" lsb="0" />
            <mtx name="uniE992" width="556" lsb="0" />
            <mtx name="uniEBDD" width="556" lsb="0" />
            <mtx name="uniED60" width="556" lsb="0" />
            <mtx name="uniF279" width="556" lsb="0" />
            <mtx name="uniF46D" width="556" lsb="0" />
            <mtx name="uniF69C" width="556" lsb="0" />
            <mtx name="x" width="100" lsb="0" />
        </hmtx>
        """
        with open(font_xml_save_path, 'r') as f:
            xml_content = f.read()

        xml_dict = dict(parse(xml_input=xml_content))
        # pprint(xml_dict)
        _ = xml_dict['ttFont']['hmtx']['mtx'][1:-1]
        a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        _ = [dict(item).get('@name') for item in _]
        _ = list(zip(_, a))
        # pprint(_)

        all_font_list = {}
        for item in _:
            all_font_list.update({
                item[0].lower().replace('uni', ''): str(item[1])
            })
        # pprint(all_font_list)

        return all_font_list

    async def _get_today_films_box_office_info(self) -> list:
        '''
        获取今日票房信息
        :return:
        '''
        async def _wash_body(body) -> str:
            '''清洗body'''
            # 先不取值, 先把原先的html全部替换再操作
            for key, value in char_dict.items():
                _ = '&#x' + key + ';'
                body = re.compile(_).sub(value, body)
            # print(body)

            return body

        async def _handle_films_box_office_info(body) -> list:
            '''处理票房信息'''
            ul_part_list = list(Selector(text=body).css('ul.canTouch').extract())
            # pprint(ul_part_list)
            all_res = []
            for item in ul_part_list:
                try:
                    film_name = Selector(text=item).css('li.c1 b ::text').extract_first() or ''
                    assert film_name != '', 'film_name为空值!'
                    show_time = Selector(text=item).css('li.c1 em ::text').extract()[0] or ''
                    assert show_time != '', 'show_time为空值!'
                    all_box_office = Selector(text=item).css('li.c1 em i ::text').extract_first() or ''
                    assert all_box_office != '', 'all_box_office为空值!'
                    real_time_box_office = Selector(text=item).css('li.c2 b i ::text').extract_first() or ''
                    assert real_time_box_office != '', 'real_time_box_office为空值!'
                    box_office_ratio = Selector(text=item).css('li.c3 i ::text').extract_first() or ''
                    assert box_office_ratio != '', 'box_office_ratio为空值!'
                    ranking_ratio = Selector(text=item).css('li.c4 i ::text').extract_first() or ''
                    assert ranking_ratio != '', 'ranking_ratio为空值!'
                    upper_seat_rate = Selector(text=item).css('li.c5 i ::text').extract_first() or ''
                    assert upper_seat_rate != '', 'upper_seat_rate为空值!'
                except AssertionError as e:
                    print(e)
                    continue

                all_res.append({
                    'film_name': film_name,
                    'show_time': show_time,                         # 上映时间
                    'all_box_office': all_box_office,               # 总票房
                    'real_time_box_office': real_time_box_office,   # 实时票房
                    'box_office_ratio': box_office_ratio,           # 票房占比
                    'ranking_ratio': ranking_ratio,                 # 排名占比
                    'upper_seat_rate': upper_seat_rate,             # 上座率
                })

            return all_res

        headers = {
            'authority': 'piaofang.maoyan.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        params = (
            ('ver', 'normal'),
        )
        url = 'https://piaofang.maoyan.com/'
        body = Requests.get_url_body(url=url, headers=headers, params=params)
        # &#xf1f6;&#xf1f6;&#xf8d8;&#xf8a3;&#xecaf;.&#xf614;万
        # print(body)

        if body == '':
            print('获取到的body为空值!')
            return []

        # 找到字体文件, 并保存到本地(mac 查看是.otf | win 查看是.tff) 此处统一为.tff
        try:
            font_base64_str = re.compile('src:url\((.*?)\)').findall(body)[0]
            # print(font_base64_str)
        except IndexError:
            print('获取font_base64_str时索引异常!')
            font_base64_str = ''

        save_path = '/Users/afa/Desktop/x.ttf'
        if font_base64_str != '':
            save_font_res = save_base64_img_2_local(save_path=save_path, base64_img_str=font_base64_str)
            if not save_font_res:
                print('保存字体文件失败!')
                return []

        font_xml_save_path = '/Users/afa/Desktop/x.xml'
        char_dict = await self._get_char_dict(font_path=save_path, font_xml_save_path=font_xml_save_path)
        pprint(char_dict)

        # origin_all_res = await _handle_films_box_office_info(body=body)
        # print('原始数据'.center(100, '-'))
        # pprint(origin_all_res)
        # pprint(origin_all_res[0])
        # print('-'.center(100, '-'))
        body = await _wash_body(body=body)
        all_res = await _handle_films_box_office_info(body=body)
        print('新数据'.center(100, '-'))
        pprint(all_res)
        # pprint(all_res[0])
        print('-'.center(100, '-'))

        return all_res

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = MaoYanFilmsSpider()
    loop = get_event_loop()
    # loop.run_until_complete(_._fck_run())
    loop.run_until_complete(_._get_today_films_box_office_info())