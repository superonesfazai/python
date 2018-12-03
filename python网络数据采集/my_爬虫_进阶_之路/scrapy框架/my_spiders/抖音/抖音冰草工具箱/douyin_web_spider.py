# coding:utf-8

'''
@author = super_fazai
@File    : douyin_web_spider.py
@connect : superonesfazai@gmail.com
'''

"""
基于冰草的抖音web爬虫(https://www.welltool.net/douyinweb)
"""

from items import (
    VideoItem,
    DouYinWeb,
)

from gc import collect
from mongoengine import (
    connect,
)
from mongoengine.errors import NotUniqueError
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

mongdb_cli = connect(db='fz_db', host='mongodb://127.0.0.1:27017/fz_db')

class BCDYSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool
        )
        self.concurrency = 16
        # 下一个cursor, 依赖于上一个resp返回的cursor
        self.next_cursor = None

    async def _fck_run(self):
        try:
            index = 1
            while True:
                print('{}'.format(index).center(20, '-'))
                cursor, one_list = await self._get_one_page_info()
                await async_sleep(1.)      # 避免请求频繁
                index += 1
                if cursor is None or one_list == []:
                    continue
                await self._insert_into_douyin(cursor=cursor, one_list=one_list)
        except KeyboardInterrupt:
            # 异常存储
            await self._record_cursor(cursor=self.next_cursor)
            print('KeyboardInterrupt')
            return None

    async def _insert_into_douyin(self, **kwargs) -> bool:
        '''
        插入数据到douyin
        :return:
        '''
        res = False
        cursor:str = kwargs['cursor']
        one_list:list = kwargs['one_list']

        try:
            _ = DouYinWeb(cursor=cursor, content=one_list, create_time=get_shanghai_time()).save()
            print('[+] cursor[{}] 存入db中success!'.format(cursor))
            res = True
        except NotUniqueError:
            print('[-] cursor[{}] 已存在于db中...'.format(cursor))
        except Exception as e:
            print(e)

        return res

    async def _select_douyin(self) -> list:
        '''
        查找所有数据
        :return:
        '''
        all_res = DouYinWeb.objects.all()
        all = []
        for item in all_res:
            cursor = item.cursor
            content = item.content
            all.append([cursor, content])

        return all

    async def _get_one_page_info(self) -> tuple:
        '''
        获取单页信息
        :return:
        '''
        async def _get_r_and_e(cursor, count) -> tuple:
            '''获取params中的r, e'''
            args = (
                cursor,
                count,
            )
            r = get_js_parser_res(
                './js/hook.js',
                'get_r',
                *args
            )
            url = "dbTest?cursor=" + cursor + "&count=" + count
            parseTempStr = url + '@&^' + r
            e = md5_encrypt(target_str=parseTempStr)

            return r, e

        async def _get_right_download_url(res) -> list:
            '''获取能正常播放的视频地址'''
            # js 找 getFeedVideo, downloadURL的生成方法js转python
            for item in res:
                try:
                    video_download_addr_uri = item.get('video', {}).get('download_addr', {}).get('uri', '')
                    assert video_download_addr_uri != '', 'video_download_addr_uri为空值!'
                    # 获取视频原始播放地址
                    download_url = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id={}&line=0'.format(
                        video_download_addr_uri)
                    download_url = download_url.replace("&watermark=1&", "&watermark=0&")
                    download_url = download_url.replace("720p", "")
                    # title
                    title = item.get('desc', '')
                    share_url = item.get('share_url', '')
                    assert share_url != '', 'share_url为空值!'
                    statistics = item.get('statistics', {})
                    praise_num = statistics.get('digg_count', 0)
                    comment_num = statistics.get('comment_count', 0)
                    share_num = statistics.get('share_count', 0)
                except AssertionError as e:
                    print(e)
                    continue

                print('download_url:{}, praise_num:{}, comment_num:{}, desc:{}'.format(download_url, praise_num, comment_num, title))
                item.update({
                    'download_url': download_url,
                })

            return res

        # 在js找dbTest接口
        # cursor下一个值在上个请求的答复中
        cursor = self.next_cursor if self.next_cursor is not None else await self._read_local_cursor()    # 起始值
        try:
            assert cursor != '', 'cursor为空值! 异常退出!'
        except AssertionError as e:
            await self._record_cursor(cursor=cursor)
            raise e

        count = '6'
        r, e = await _get_r_and_e(cursor, count)
        print('cursor: {}\nr: {}\ne: {}'.format(cursor, r, e))
        params = (
            ('cursor', cursor),
            ('count', '6'),
            ('e', e),
            ('r', r),
        )
        url = 'https://www.welltool.net/dbTest'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_phone_headers(), params=params, ip_pool_type=self.ip_pool_type))
        # pprint(data)
        if data == {}:
            return (self.next_cursor, [])

        self.next_cursor = data.get('cursor', '')
        res = data.get('data', [])

        return (self.next_cursor, await _get_right_download_url(res))

    async def _read_local_cursor(self) -> str:
        '''
        读取本地cursor
        :return:
        '''
        with open('./start_cursor.txt', 'r') as f:
            cursor = f.read().replace('\n', '')

        return cursor

    async def _record_cursor(self, cursor) -> None:
        '''
        记录下当前异常退出的cursor
        :return:
        '''
        with open('./start_cursor.txt', 'w') as f:
            f.write(cursor)

    async def _get_phone_headers(self) -> dict:
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.welltool.net/douyinweb?i=3',
            'Connection': 'keep-alive',
        }

    def __del__(self):
        try:
            del loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = BCDYSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

    # 查找所有数据
    # res = loop.run_until_complete(_._select_douyin())
    # pprint(res)

