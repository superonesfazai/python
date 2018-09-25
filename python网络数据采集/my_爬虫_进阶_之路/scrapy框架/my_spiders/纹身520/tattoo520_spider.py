# coding:utf-8

'''
@author = super_fazai
@File    : tattoo520_spider.py
@connect : superonesfazai@gmail.com
'''

"""
异步高并发实现抓取纹身520
"""

from gc import collect
import asyncio
from asyncio import CancelledError
from scrapy.selector import Selector
from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua

class Tattoo520Spider(object):
    def __init__(self):
        self.max_page_num = 20
        self.loop = asyncio.get_event_loop()

    async def _get_headers(self):
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://www.wenshen520.com/s.php?k=%E5%8E%9F%E7%A8%BF%E5%9B%BE&p=1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_one_page(self, page_num) -> str:
        '''
        抓取一个页面
        :return:
        '''
        headers = await self._get_headers()
        params = (
            ('k', '原稿图'),
            ('p', str(page_num)),
        )
        url = 'https://www.wenshen520.com/s.php'
        body = Requests.get_url_body(url=url, headers=headers, params=params, cookies=None)
        # print(body)

        return body

    async def _parse_page(self, page_num) -> list:
        '''
        解析页面
        :param page_num:
        :return:
        '''
        body = await self._get_one_page(page_num=page_num)

        p_l_a = Selector(text=body).css('p#l a').extract() or []
        all = []
        for item in p_l_a:
            # print(item)
            try:
                img_url = Selector(text=item).css('img ::attr("src")').extract_first()
                assert img_url is not None, 'img_url为None!'
                name = Selector(text=item).css('i ::text').extract_first()
                assert name is not None, 'name为None!'
                num = Selector(text=item).css('em ::text').extract_first() or ''
                num = int(num.replace('张', '')) if num != '' else 1
            except (AssertionError, Exception) as e:
                # print(e)
                continue
            all.append({
                'tattoo_name': name,
                'img_url': img_url,
                'img_num': num,
            })

        return all

    async def _fck_run(self):
        tasks = []
        for page_num in range(1, self.max_page_num):
            print('创建task: {}'.format(page_num))
            tasks.append(self.loop.create_task(self._parse_page(page_num=page_num)))

        print('请耐心等待所有任务完成...')
        success_jobs, fail_jobs = await asyncio.wait(tasks)
        print('success_num: {}, fail_num: {}'.format(len(success_jobs), len(fail_jobs)))
        all_res = [r.result() for r in success_jobs]
        # pprint(all_res)
        print('总长度为: {}'.format(len(all_res)))

        # TODO
        # all_res = []
        # while tasks != []:
        #     for task in tasks:
        #         # print(task)
        #         # print(task.__class__)     # <class '_asyncio.Task'>
        #         if task.done():
        #             one = await task.result()
        #             print('[+]')
        #             try:
        #                 tasks.remove(task)
        #             except:
        #                 pass
        #         else:
        #             pass

        return all_res

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = Tattoo520Spider()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(_._fck_run())
    try:
        del loop
    except:
        pass