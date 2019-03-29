# coding:utf-8

'''
@author = super_fazai
@File    : fried_eggs_spider.py
@connect : superonesfazai@gmail.com
'''

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.selector import async_parse_field
from fzutils.iter_utils import itemgetter
from fzutils.spider.async_always import *

class FriedEggsSpider(AsyncCrawler):
    """煎蛋网spider"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.duanzi_max_page = 150
        self.concurrency = 50
        self.num_retries = 6

    async def _fck_run(self):
        # await self._crawl_all_latest_articles()
        await self._crawl_all_duanzi()

    async def _crawl_all_duanzi(self):
        """
        抓取所有段子
        :return:
        """
        async def get_tasks_params_obj():
            tasks_params_obj = []
            for page_num in range(1, self.duanzi_max_page):
                tasks_params_obj.append({
                    'page_num': page_num,
                })

            return tasks_params_obj

        async def _get_one_res(slice_params_obj) -> list:
            """
            获取one_res
            :param slice_params_obj:
            :return:
            """
            tasks = []
            for k in slice_params_obj:
                page_num = k['page_num']
                print('create task[where page_num: {}]'.format(page_num))
                tasks.append(self.loop.create_task(self._get_duanzi_one_page_info(
                    page_num=page_num,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        tasks_params_obj = await get_tasks_params_obj()
        tasks_params_obj = TasksParamsListObj(tasks_params_list=tasks_params_obj, step=self.concurrency)
        all_res = []
        while True:
            try:
                slice_params_obj = tasks_params_obj.__next__()
            except AssertionError:
                break
            one_res = await _get_one_res(slice_params_obj)

            for i in one_res:
                for j in i:
                    all_res.append(j)

        all_res = sorted(all_res, key=itemgetter('like_num'), reverse=False,)
        pprint(all_res)
        print('all_res_len: {}'.format(len(all_res)))

        return all_res

    async def _get_duanzi_one_page_info(self, page_num) -> list:
        """
        获取单页段子的所有内容
        :return:
        """
        async def parse(body) -> list:
            """解析"""
            li_selector = {
                'method': 'css',
                'selector': 'li[id*="comment-"]',
            }
            author_selector = {
                'method': 'css',
                'selector': 'strong.orange-name ::text',
            }
            content_p_selector = {
                'method': 'css',
                'selector': 'div.text p ::text',
            }
            like_num_selector = {
                'method': 'css',
                'selector': 'span.tucao-like-container span ::text',
            }
            unlike_num_selector = {
                'method': 'css',
                'selector': 'span.tucao-unlike-container span ::text',
            }

            li_list = await async_parse_field(
                parser=li_selector,
                target_obj=body,
                is_first=False,)
            # pprint(li_list)

            res = []
            for item in li_list:
                try:
                    author = await async_parse_field(
                        parser=author_selector,
                        target_obj=item,
                        is_print_error=False,)
                    assert author != '', 'author != ""'
                    # print(author)
                    content = ''
                    content_p_list = await async_parse_field(
                        parser=content_p_selector,
                        target_obj=item,
                        is_first=False,
                        is_print_error=False,)
                    # print(content_p_list)
                    assert content_p_list != [], 'content_p_list != []'
                    for p in content_p_list:
                        content += p + '\n'
                    like_num = int(await async_parse_field(
                        parser=like_num_selector,
                        target_obj=item,
                        is_print_error=False,))
                    # print(like_num)
                    unlike_num = int(await async_parse_field(
                        parser=unlike_num_selector,
                        target_obj=item,
                        is_print_error=False,))
                    # print(unlike_num)
                except (AssertionError, ValueError):
                    continue

                res.append({
                    'author': author,
                    'content': content,
                    'like_num': like_num,
                    'unlike_num': unlike_num,
                })

            return res

        headers = await self._get_random_pc_headers()
        headers.update({
            'Referer': 'http://jandan.net/duan',
        })
        url = 'http://jandan.net/duan/page-{}'.format(page_num)
        body = await AioHttp.aio_get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        res = await parse(body)
        # pprint(res)

        print('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    async def _get_one_page_articles(self, page_num) -> list:
        '''
        得到一个页面的所有文章
        :return:
        '''
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://jandan.net/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        url = 'http://jandan.net/page/{}'.format(page_num)
        body = Requests.get_url_body(url=url, headers=headers)
        # print(body)
        if body == '':
            return []

        part = list(Selector(text=body).css('div.post.f.list-post').extract())
        # pprint(part)
        _ = []
        for item in part:
            try:
                title = Selector(text=item).css('div.indexs h2 a ::text').extract_first() or ''
                assert title != '', '获取到的title为空值!'
                author = Selector(text=item).css('div.time_s a ::text').extract_first() or ''
                assert author != '', '获取到的author为空值!'
                tag = Selector(text=item).css('div.time_s strong a ::text').extract_first() or ''
                assert tag != '', '获取到的tag为空值!'
                img = Selector(text=item).css('div.thumbs_b a img ::attr("src")').extract_first() or ''
                img = 'http:' + img if img != '' else ''
                try:
                    comment_num = int(Selector(text=item).css('div.indexs span ::text').extract_first())
                except TypeError:
                    comment_num = 0
                # print(comment_num)
                sub_title = re.compile('<div class=\"indexs\">.*?</div>.*?</div>').findall(item)[0].replace('\n', '').replace(' ', '')
            except (AssertionError, IndexError, Exception) as e:
                print(e)
                continue

            _.append({
                'title': title,
                'author': author,
                'tag': tag,
                'img': img,
                'comment_num': comment_num,
                'sub_title': sub_title,
            })

        return _

    async def _crawl_all_latest_articles(self):
        '''
        抓取所有最新的新鲜事
        :return:
        '''
        all = []
        for page_num in range(1, 2500):
            one_res = await self._get_one_page_articles(page_num)
            # pprint(one_res)
            all += one_res
            label = '+' if one_res != [] else '-'
            print('[{}] 第{}页...'.format(label, page_num))

        return all

    @staticmethod
    async def _get_random_pc_headers():
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

if __name__ == '__main__':
    _ = FriedEggsSpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())