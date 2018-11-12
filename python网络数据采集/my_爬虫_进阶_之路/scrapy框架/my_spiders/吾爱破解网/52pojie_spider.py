# coding:utf-8

'''
@author = super_fazai
@File    : 52pojie_spider.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from items import PostItem
from time import time
from fzutils.spider.async_always import *

class _52PoJieSpider(AsyncCrawler):
    """吾爱破解网爬虫"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=4&page=2&mobile=2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_one_page_list_in_reverse_resource_area(self, page_num) -> list:
        '''
        获取逆向资源单页面信息
        :return:
        '''
        async def _parse(body) -> list:
            """解析页面"""
            _ = []
            for item in Selector(text=body).css('div.threadlist li').extract() or []:
                _i = PostItem()
                try:
                    title = Selector(text=item).css('a ::text').extract_first() or ''
                    # print(title)
                    assert title != '', 'title为空值!'

                    author = Selector(text=item).css('a span.by ::text').extract_first() or ''
                    assert author != '', 'author为空值!'

                    comment_num = int(Selector(text=item).css('a span.num ::text').extract_first() or '')
                    post_url = Selector(text=item).css('a ::attr("href")').extract_first() or ''
                    assert post_url != '', 'post_url为空值!'
                    post_url = 'https://www.52pojie.cn/' + post_url

                except (AssertionError, ValueError, Exception) as e:
                    print(e)
                    continue

                oo = PostItem()
                oo['title'] = title
                oo['author'] = author
                oo['comment_num'] = comment_num
                oo['post_url'] = post_url

                _.append(dict(oo))

            return _

        params = (
            ('mod', 'forumdisplay'),
            ('fid', '4'),               # 逆向区
            ('page', str(page_num)),
            ('mobile', '2'),
        )
        url = 'https://www.52pojie.cn/forum.php'
        body = Requests.get_url_body(url=url, headers=await self._get_phone_headers(), params=params, cookies=None)
        # print(body)
        assert body != '', 'body为空'

        return await _parse(body=body)

    async def _get_all_reverse_resource_area_article_list(self) -> list:
        '''
        获取所有逆向板块文章
        :return:
        '''
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=range(1, 201), step=self.concurrency)
        _ = []
        s_time = time()
        while True:
            try:
                aa = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for page_num in aa:
                print('create task: {}'.format(page_num))
                tasks.append(self.loop.create_task(self._get_one_page_list_in_reverse_resource_area(page_num=page_num)))
                # pprint(one)

            all_res = await async_wait_tasks_finished(tasks=tasks)
            for item in all_res:
                for i in item:
                    _.append(i)

        pprint(_)
        print('总耗时: {}s, 总长度: {}'.format(time() - s_time, len(_)))

        return _

    async def _fck_run(self):
        await self._get_all_reverse_resource_area_article_list()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = _52PoJieSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
