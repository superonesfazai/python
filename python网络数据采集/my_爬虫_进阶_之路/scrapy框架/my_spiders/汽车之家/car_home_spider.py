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

import re
from gc import collect
from asyncio import get_event_loop
from fontTools.ttLib import TTFont

from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua

class CarHomeSpider(object):
    def __init__(self):
        self.font_base_save_path = '/Users/afa/myFiles/tmp/字体反爬/汽车之家/'

    async def _get_headers(self):
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
        headers = await self._get_headers()
        url = 'https://club.autohome.com.cn/bbs/thread/1f05b4da4448439b/76044817-1.html'
        body = Requests.get_url_body(url=url, headers=headers, cookies=None)
        # print(body)

        font_download_res = await self._download_font_file(body=body)
        if not font_download_res:
            return []

        font = TTFont(self.font_base_save_path+'x.ttf')
        font.saveXML(fileOrPath=self.font_base_save_path+'x.xml')

    async def _fck_run(self):
        await self._get_one_page_info()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = CarHomeSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())