# coding:utf-8

'''
@author = super_fazai
@File    : doutula_spider.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import parse_field
from fzutils.spider.fz_driver import (
    BaseDriver,
    PHONE,)
from fzutils.internet_utils import _get_url_contain_params
from fzutils.spider.async_always import *

class DouTuLaSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.max_home_page_page_num = 10
        self.request_num_retries = 5
        self.concurrency = 10

    async def _fck_run(self):
        await self.get_all_home_page_info()

    async def get_all_home_page_info(self):
        """
        获取主页所有图片
        :return:
        """
        async def get_tasks_params_list() -> list:
            tasks_params_list = []
            for page_num in range(1, self.max_home_page_page_num + 1):
                tasks_params_list.append({
                    'page_num': page_num
                })

            return tasks_params_list

        tasks = []
        func_name = self.get_home_page_info_by_page_num
        tasks_params_list = await get_tasks_params_list()
        tasks_params_list = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=self.concurrency,)

        all_res = []
        while True:
            try:
                slice_tasks_params_list = tasks_params_list.__next__()
            except AssertionError:
                break

            for k in slice_tasks_params_list:
                page_num = k['page_num']
                print('create task[where page_num: {}] ...'.format(page_num))
                func_args = [
                    page_num,
                ]
                tasks.append(self.loop.create_task(unblock_func(
                    func_name=func_name,
                    func_args=func_args,
                    default_res=[]
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            pprint(one_res)

    def get_home_page_info_by_page_num(self, page_num: int) -> list:
        """
        根据page_num获取单页的信息
        :param page_num:
        :return:
        """
        def parse_page_info(body) -> list:
            """
            解析
            :param body:
            :return:
            """
            # div item
            li_sel = {
                'method': 'css',
                'selector': 'div.center-wrap a.random_list',
            }
            title_sel = {
                'method': 'css',
                'selector': 'div.random_title ::text',
            }
            create_time_sel = {
                'method': 'css',
                'selector': 'div.date ::text',
            }
            article_img_url_sel = {
                'method': 'css',
                'selector': 'div.random_article img ::attr("data-original")',
            }
            article_img_name_sel = {
                'method': 'css',
                'selector': 'div.random_article img ::attr("alt")',
            }
            li_list = parse_field(
                parser=li_sel,
                target_obj=body,
                is_first=False,)
            res = []
            for item in li_list:
                # pprint(item)
                try:
                    title = parse_field(
                        parser=title_sel,
                        target_obj=item,)
                    assert title != ''
                    create_time = parse_field(
                        parser=create_time_sel,
                        target_obj=item,)
                    assert create_time != ''
                    article_img_url_list = parse_field(
                        parser=article_img_url_sel,
                        target_obj=item,
                        is_first=False,)
                    assert article_img_url_list != []
                    article_img_name_list = parse_field(
                        parser=article_img_name_sel,
                        target_obj=item,
                        is_first=False,)
                    assert article_img_name_list != []
                    article_img_list = list(zip(article_img_name_list, article_img_url_list))
                    article_img_list = [{
                        'img_name': i[0],
                        'img_url': i[1],
                    } for i in article_img_list]
                except (AssertionError, IndexError) as e:
                    # print(e)
                    continue

                res.append({
                    'title': title,
                    'create_time': create_time,
                    'article_img_list': article_img_list,
                })

            return res

        headers = self.get_random_phone_headers()
        headers.update({
            'authority': 'www.doutula.com',
            'referer': 'https://www.doutula.com/',
        })
        params = (
            ('page', str(page_num)),
        )
        url = 'https://www.doutula.com/article/list/'
        # TODO 用requests乱码
        # body = Requests.get_url_body(
        #     url=url,
        #     headers=headers,
        #     params=params,
        #     ip_pool_type=self.ip_pool_type,
        #     num_retries=self.request_num_retries,
        #     encoding='utf-8',)
        # print(body)
        # 改用driver
        d = BaseDriver(
            ip_pool_type=tri_ip_pool,
            user_agent_type=PHONE)
        body = d.get_url_body(url=_get_url_contain_params(url=url, params=params))
        # print(body)
        try:
            del d
        except:
            pass
        res = parse_page_info(body=body)
        print('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))
        collect()

        return res

    @staticmethod
    def get_random_phone_headers():
        return {
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = DouTuLaSpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())