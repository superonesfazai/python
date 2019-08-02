# coding:utf-8

'''
@author = super_fazai
@File    : ealover_spider.py
@connect : superonesfazai@gmail.com
'''

"""
恩爱情侣网: http://www.ealover.com/
"""

from fzutils.ip_pools import tri_ip_pool
from fzutils.exceptions import catch_exceptions
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import *

class EALoverSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.req_num_retries = 6
        self.max_pnbd_page_num = 30
        self.concurrency = 10

    async def _fck_run(self):
        res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=list(range(1, self.max_pnbd_page_num + 1)),
            func_name_where_get_create_task_msg=self.get_create_task_msg,
            func_name=self.get_pnbd_info_by_page_num,
            func_name_where_get_now_args=self.get_now_args,
            func_name_where_handle_one_res=self.handle_one_res,
            one_default_res=[],
            step=self.concurrency,)
        # pprint(res)
        print('len_res: {}'.format(len(res)))

    def get_create_task_msg(self, k) -> str:
        return 'create task[where page_num: {}]...'.format(k)

    def get_now_args(self, k) -> list:
        return [
            k,
        ]

    async def handle_one_res(self, one_res):
        print('len_one_res: {}'.format(len(one_res)))

    @catch_exceptions(default_res=[])
    def get_pnbd_info_by_page_num(self, page_num: int) -> list:
        """
        获取单页泡妞宝典info
        :param page_num:
        :return:
        """
        def parse(body) -> list:
            title_sel = {
                'method': 'css',
                'selector': 'p.list_tit a ::text',
            }
            url_sel = {
                'method': 'css',
                'selector': 'p.list_tit a ::attr("href")',
            }
            desc_sel = {
                'method': 'css',
                'selector': 'p.desc.left ::text',
            }
            title_list = parse_field(
                parser=title_sel,
                target_obj=body,
                is_first=False,
            )
            # pprint(title_list)
            url_list = parse_field(
                parser=url_sel,
                target_obj=body,
                is_first=False,
            )
            # pprint(url_list)
            desc_list = parse_field(
                parser=desc_sel,
                target_obj=body,
                is_first=False,
            )
            # pprint(desc_list)
            _ = list(zip(title_list, url_list, desc_list))
            # pprint(_)

            return [{
                'title': item[0],
                'url': item[1],
                'desc': item[2],
            } for item in _]

        headers = self.get_random_pc_headers()
        headers.update({
            'Referer': 'http://www.ealover.com/paoniubaodian/',
        })
        url = 'http://www.ealover.com/paoniubaodian/list_2_{}.html'.format(page_num)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            encoding='gb2312',)
        # print(body)
        assert body != ''

        res = parse(body=body)
        # pprint(res)
        print('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    @staticmethod
    def get_random_pc_headers():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    @staticmethod
    def get_random_phone_headers():
        return {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    ealover = EALoverSpider()
    loop = get_event_loop()
    loop.run_until_complete(ealover._fck_run())