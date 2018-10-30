# coding:utf-8

'''
@author = super_fazai
@File    : youtube_downloader.py
@connect : superonesfazai@gmail.com
'''

"""
youtube downloader
"""

from gc import collect
from requests import get
from shutil import copyfileobj
from urllib.parse import parse_qs
from fzutils.spider.crawler import AsyncCrawler
from fzutils.spider.async_always import *

class YouTuBeDownloader(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(self, *params, **kwargs)
        self.movie_save_path = '/Users/afa/Downloads/'   # 视频存储路径

    async def _download(self, url) -> bool:
        '''
        下载视频文件
        :param url: 视频地址
        :return:
        '''
        print('movie_url: {}'.format(url))
        try:
            v = re.compile('v=(\w+)').findall(url)[0]
        except IndexError:
            print('获取v失败!')
            return False

        params = (
            ('v', v),
        )
        # 带头访问乱码，所有不带头
        response = get('https://www.youtube.com/watch', headers=None, params=params)
        body = Requests._wash_html(response.text)
        # print(body)

        data = {}
        try:
            data = json_2_dict(re.compile('ytplayer.config = (.*?);ytplayer.load').findall(body)[0])
            # pprint(data)
        except IndexError as e:
            print(e)
        url_encoded_fmt_stream_map = data.get('args', {}).get('url_encoded_fmt_stream_map', '')
        # print(url_encoded_fmt_stream_map)
        try:
            movie_url = parse_qs(url_encoded_fmt_stream_map).get('url', [])[0]
            print('获取到视频地址: {}'.format(movie_url))
        except IndexError:
            print('获取movie_url失败!')
            return False

        # 本地存储视频
        file_save_path = self.movie_save_path + str(v) + '.mp4'
        with open(file_save_path, 'wb') as f:
            with get(url=movie_url, stream=True) as response:
                copyfileobj(response.raw, f)

        return True

if __name__ == '__main__':
    _ = YouTuBeDownloader()
    loop = get_event_loop()
    url = 'https://www.youtube.com/watch?v=2NpKvmzYKro'
    res = loop.run_until_complete(_._download(url=url))