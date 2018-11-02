# coding:utf-8

'''
@author = super_fazai
@File    : first_time_house_spider.py
@connect : superonesfazai@gmail.com
'''

"""
第一时间房源网爬虫
"""

from gc import collect
from fzutils.ip_pools import sesame_ip_pool
from fzutils.spider.async_always import *

class FirstTimeHouseSpider(AsyncCrawler):
    def __init__(self, *pawams, **kwargs):
        AsyncCrawler.__init__(self, *pawams, **kwargs)
        self.loop = get_event_loop()
        self._t = lambda : str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        self.ip_pool_type = sesame_ip_pool
        self.city_info_list = None          # 城市信息

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'http://m.01fy.cn/bj/rent/list_2_0_0_0-0_0_0-0_0_2_0_2_.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_pc_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://www.01fy.cn/index.htm',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _get_all_city_info(self) -> list:
        '''
        获取所有城市的信息
        :return:
        '''
        # http://www.01fy.cn/index.htm
        url = 'http://www.01fy.cn/ajax/index.php'
        params = (
            ('action', 'get_all_city_website'),
            ('t', self._t()),
        )
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_pc_headers(), params=params, ip_pool_type=self.ip_pool_type)).\
            get('data', [])
        # pprint(data)
        self.city_info_list = data if data != [] else []

        return data

    async def _get_some_city_personal_houses_one_page_info(self,
                                                           page_num,
                                                           city_name='bj',
                                                           rent_type=2,
                                                           house_price_range:str='600-1000',
                                                           house_type=0,
                                                           type=0,
                                                           section='0_0',) -> list:
        '''
        获取某城市个人房源单页信息
        :param page_num: 页面number
        :param city_name: 城市name
        :param rent_type: 房源类型 : 0 全部 | 1 经纪人 | 2 个人 | 3 合作房源 | 4 品牌公寓
        :param house_price_range: 价格范围 : '0-0' 不限价格 | '0-600' 600元以下 | ... | '8000-0' 8000元以上
        :param house_type: 户型 : 0 不限 | ... | 10 九室以上
        :param type: 方式 : 0 不限 | 1 整租 | 2 合租
        :param section: 具体地段: 0_0 表示比如全北京 | 其他看具体给的参数 格式都是 'xx_xx'
        :return:
        '''
        # eg: http://m.01fy.cn/bj/rent/list_4_502_3704_0-600_0_0-0_1_2_0_1_.html
        url = 'http://m.01fy.cn/{city_name}/rent/list_{rent_type}_{section}_{house_price_range}_{house_type}_0-0_{type}_2_0_{page_num}_.html'.format(
            city_name=city_name,
            rent_type=rent_type,
            page_num=page_num,
            house_price_range=house_price_range,
            house_type=house_type,
            section=section,
            type=type)
        body = Requests.get_url_body(url=url, headers=await self._get_phone_headers(), ip_pool_type=self.ip_pool_type)
        # print(body)

        return []

    async def _fck_run(self):
        # await self._get_all_city_info()
        await self._get_some_city_personal_houses_one_page_info(page_num=3)

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = FirstTimeHouseSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

