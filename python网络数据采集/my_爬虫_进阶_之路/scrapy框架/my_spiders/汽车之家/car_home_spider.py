# coding:utf-8

'''
@author = super_fazai
@File    : car_home_spider.py
@connect : superonesfazai@gmail.com
'''

"""
汽车之家爬虫
    法1. 可以直接使用driver 禁止js运行, 避免字符被替换
    法2. 此处根据字体替换字符
"""

from gc import collect
from fontTools.ttLib import TTFont

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import *

class CarHomeSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.num_retries = 3
        self.font_base_save_path = '/Users/afa/myFiles/tmp/字体反爬/汽车之家/'

    async def _fck_run(self):
        # 获取给定地址的html info
        # await self._get_one_page_info()

        # 获取所有品牌的所有车型的价格
        await self._get_all_brand_all_car_price()

    async def _get_all_brand_all_car_price(self) -> list:
        """
        获取所有品牌所有车型的价格(https://car.m.autohome.com.cn/)
        :return:
        """
        brand_info_list = await self._get_all_brand_name_and_brand_id()
        # pprint(brand_info_list)
        assert brand_info_list != []

        tasks = []
        for k in brand_info_list:
            brand_name = k['brand_name']
            brand_id = k['brand_id']
            print('create task[where brand_id: {}, brand_name: {}] ...'.format(brand_id, brand_name,))
            func_args = [
                brand_id,
                brand_name,
            ]
            tasks.append(self.loop.create_task(unblock_func(
                func_name=self._get_all_car_info_by_brand_id,
                func_args=func_args,
            )))

        _ = await async_wait_tasks_finished(tasks=tasks)
        # pprint(_)
        all_res = []
        for i in _:
            for j in i:
                all_res.append(j)
        pprint(all_res)
        print('total car model num: {}'.format(len(all_res)))
        try:
            del _
        except:
            pass

        return []

    def _get_all_car_info_by_brand_id(self, brand_id: str, brand_name: str) -> list:
        """
        根据brand_id获取其所有car info
        :param brand_id:
        :return:
        """
        # 获取单个brand的所有车型及其价格
        headers = self.get_random_phone_headers()
        headers.update({
            'Referer': 'https://car.m.autohome.com.cn/',
            'X-Requested-With': 'XMLHttpRequest',
        })
        params = (
            ('r', '9'),         # 定值
            ('b', brand_id),    # brandId
        )
        url = 'https://car.m.autohome.com.cn/ashx/GetSeriesByBrandIdNew.ashx'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        data = json_2_dict(
            json_str=body,).get('result', {}).get('sellSeries', [])
        # pprint(data)

        print('[{}] brand_id: {}, brand_name: {}'.format(
            '+' if data != [] else '-',
            brand_id,
            brand_name,
        ))

        return data

    async def _get_all_brand_name_and_brand_id(self) -> list:
        """
        获取所有品牌名及其对应的brand_id
        :return:
        """
        headers = self.get_random_phone_headers()
        headers.update({
            'authority': 'car.m.autohome.com.cn',
            'referer': 'https://car.autohome.com.cn/',
        })
        url = 'https://car.m.autohome.com.cn/'
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries, )
        brand_name_selector = {
            'method': 'css',
            'selector': 'div#div_ListBrand ul li div span ::text',
        }
        brand_id_selector = {
            'method': 'css',
            'selector': 'div#div_ListBrand ul li div ::attr("v")',
        }
        brand_name_list = parse_field(
            parser=brand_name_selector,
            target_obj=body,
            is_first=False, )
        brand_id_list = parse_field(
            parser=brand_id_selector,
            target_obj=body,
            is_first=False, )
        tmp_brand_info_list = list(zip(brand_name_list, brand_id_list))
        # pprint(tmp_brand_info_list)

        brand_info_list = [{
            'brand_name': item[0],
            'brand_id': item[1],
        } for item in tmp_brand_info_list]
        # pprint(brand_info_list)

        return brand_info_list

    async def _download_font_file(self, body):
        '''
        下载字体文件
        :return:
        '''
        try:
            font_url = 'https:' + re.compile(',url\(\'(.*?)\'\) format\(\'woff\'\);').findall(body)[0]
            print('获取到的字体url: {}'.format(font_url))
        except IndexError:
            print('获取font_url时索引异常!')
            return False

        res = Requests._download_file(
            url=font_url,
            file_save_path=self.font_base_save_path+'x.ttf')

        return res

    async def _get_one_page_info(self) -> list:
        '''
        获取给与地址的页面html info
        :return:
        '''
        headers = self.get_random_pc_headers()
        url = 'https://club.autohome.com.cn/bbs/thread/1f05b4da4448439b/76044817-1.html'
        body = Requests.get_url_body(url=url, headers=headers, cookies=None)
        # print(body)

        font_download_res = await self._download_font_file(body=body)
        if not font_download_res:
            return []

        font = TTFont(self.font_base_save_path+'x.ttf')
        font.saveXML(fileOrPath=self.font_base_save_path+'x.xml')

    @staticmethod
    def get_random_phone_headers():
        return {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    @staticmethod
    def get_random_pc_headers():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://blog.csdn.net/xing851483876/article/details/82928607',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = CarHomeSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())