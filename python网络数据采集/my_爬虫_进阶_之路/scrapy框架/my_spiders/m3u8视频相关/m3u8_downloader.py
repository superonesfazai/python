# coding:utf-8

'''
@author = super_fazai
@File    : m3u8_downloader.py
@connect : superonesfazai@gmail.com
'''

import os
from glob import iglob
from urllib.parse import urljoin
from time import time
from requests import get

from m3u8 import load as m3u8_load
from m3u8.model import M3U8
from natsort import natsorted

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class M3U8Downloader(AsyncCrawler):
    def __init__(self, m3u8_url: str, file_name: str):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,)
        self.m3u8_url = m3u8_url
        self.file_name = file_name
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.file_name = 'new_m3u8.mp4' if not self.file_name else file_name

    def get_ts_url(self):
        m3u8_obj: M3U8 = m3u8_load(self.m3u8_url)
        # m3u8_obj = m3u8_load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri

        for seg in m3u8_obj.segments:
            print(seg)
            yield urljoin(base_uri, seg.uri)

    def download_single_ts(self, url_info):
        url, ts_name = url_info
        response = get(
            url=url,
            headers=self._get_random_pc_headers(),)
        content = response.content
        with open(ts_name, 'wb') as fp:
            fp.write(content)

    def download_all_ts(self):
        ts_urls = self.get_ts_url()
        for index, ts_url in enumerate(ts_urls):
            print(ts_url)
            self.thread_pool.submit(self.download_single_ts, [ts_url, f'{index}.ts'])

        self.thread_pool.shutdown()
        print('all ts downloaded !!')

    @func_time
    def run(self):
        """
        main
        :return:
        """
        self.download_all_ts()
        ts_path = '*.ts'
        with open(self.file_name, 'wb') as fn:
            for ts in natsorted(iglob(ts_path)):
                with open(ts, 'rb') as ft:
                    sc_line = ft.read()
                    fn.write(sc_line)

        for ts in iglob(ts_path):
            os.remove(ts)

    @staticmethod
    def _get_random_pc_headers():
        # return {
        #     'Connection': 'keep-alive',
        #     'Cache-Control': 'max-age=0',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': get_random_pc_ua(),
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        # }

        return {
            'User-Agent': get_random_pc_ua(),
        }

if __name__ == '__main__':
    # method 1:
    # m3u8_url = 'https://zk.wb699.com/2019/03/06/aLdpUIBeHC48HGTk/playlist.m3u8'
    # 接口: live_detail
    m3u8_url = 'http://liveng.alicdn.com/mediaplatform/134bc927-1b9a-408f-bd1e-70678b5d6859.m3u8?auth_key=1561795607-0-0-49754f7495460020bd75e74bd9799464'
    file_name = ''

    M3U8 = M3U8Downloader(m3u8_url=m3u8_url, file_name=file_name)
    M3U8.run()