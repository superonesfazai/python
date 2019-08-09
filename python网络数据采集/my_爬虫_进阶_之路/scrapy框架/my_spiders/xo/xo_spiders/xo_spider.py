# coding:utf-8

'''
@author = super_fazai
@File    : xo_spider.py
@connect : superonesfazai@gmail.com
'''

"""
xo spiders
"""

from items import VideoListItem
from fzutils.ip_pools import tri_ip_pool
from fzutils.exceptions import catch_exceptions_with_class_logger
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.selector import parse_field
from fzutils.spider.fz_requests import (
    PROXY_TYPE_HTTP,
    PROXY_TYPE_HTTPS,
)
from fzutils.spider.async_always import *

class XOSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
            log_print=True,
            log_save_path='/Users/afa/myFiles/my_spider_logs/xo/',
        )
        self.concurrency = 10
        self.req_num_retries = 5
        # total 210
        self.max_s63_chinese_captions_page_num = 10

    async def _fck_run(self):
        await self.s69zy3_spider()

    async def s69zy3_spider(self):
        """
        target_url: http://www.s69zy3.com
        :return:
        """
        # todo 其播放页的video标签 src是blob格式的, 但其介绍页m3u8地址即为播放地址(https)
        self.parser_obj = self.get_parser_obj()['s69']
        await self.get_all_chinese_captions_video_list()

    async def get_all_chinese_captions_video_list(self) -> list:
        """
        获取所有中文字幕的video list
        :return:
        """
        def get_tasks_params_list():
            tasks_params_list = []
            for page_num in range(1, self.max_s63_chinese_captions_page_num + 1):
                tasks_params_list.append({
                    'page_num': page_num,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where type: {}, page_num: {}] ...'.format(
                '中文字幕',
                k['page_num'],
            )

        def get_now_args(k) -> list:
            return [
                k['page_num'],
            ]

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_chinese_captions_video_list_by_page_num,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
            one_default_res=[],
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,)
        pprint(all_res)
        print('获取中文字幕video_all_res_num: {}'.format(len(all_res)))
        # 不采用request, 不管page_num怎么变都只拿到首页数据, 改用driver
        all_res = list_remove_repeat_dict_plus(
            target=all_res,
            repeat_key='video_name',)
        print('实际获取中文字幕video_all_res_num: {}'.format(len(all_res)))

        return all_res

    @catch_exceptions_with_class_logger(default_res=[])
    def get_chinese_captions_video_list_by_page_num(self, page_num: int) -> list:
        """
        根据page_num获取单页中文字幕信息
        :param page_num:
        :return:
        """
        # todo 并发采集容易被503禁止, 需周期性运行
        headers = get_random_headers()
        headers.update({
            'Referer': 'http://www.s69zy3.com/list/?36{}.html'.format(
                '-{}'.format(page_num-1 if page_num-1 > 0 else '')),
        })
        params = (
            ('36-{}.html'.format(page_num), ''),
        )
        url = 'http://www.s69zy3.com/list/'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,)
        # self.lg.info(body)
        assert body != ''

        res = self.parse_s63_video_list_page_body(body=body)
        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    @catch_exceptions_with_class_logger(default_res=[])
    def parse_s63_video_list_page_body(self, body) -> list:
        """
        解析s63电影列表页的body
        :param body:
        :return:
        """
        video_name_list = parse_field(
            parser=self.parser_obj['chinese_captions']['video_name'],
            target_obj=body,
            logger=self.lg,
            is_first=False,)
        assert video_name_list != []
        # pprint(video_name_list)
        video_region_list = parse_field(
            parser=self.parser_obj['chinese_captions']['video_region'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(video_region_list)
        assert video_region_list != []
        video_type_list = parse_field(
            parser=self.parser_obj['chinese_captions']['video_type'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(video_type_list)
        assert video_type_list != []
        url_list = parse_field(
            parser=self.parser_obj['chinese_captions']['url'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(url_list)
        assert url_list != []
        create_time_list = parse_field(
            parser=self.parser_obj['chinese_captions']['create_time'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(create_time_list)
        assert create_time_list != []

        _ = list(zip(
            video_name_list,
            video_region_list,
            video_type_list,
            url_list,
            create_time_list,))
        res = []
        for item in _:
            try:
                url = 'http://www.s69zy3.com' + item[3] if item[3] != '' else ''
                assert url != ''
                video_list_item = VideoListItem()
                video_list_item['video_name'] = item[0]
                video_list_item['video_region'] = item[1]
                video_list_item['video_type'] = item[2]
                video_list_item['url'] = url
                video_list_item['create_time'] = date_parse(item[4])
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue
            res.append(dict(video_list_item))

        try:
            del _
        except:
            pass

        return res

    @staticmethod
    def get_parser_obj() -> dict:
        """
        获取解析对象
        :return:
        """
        return {
            's69': {
                'chinese_captions': {
                    'video_name': {
                        'method': 'css',
                        'selector': 'ul.videoContent li a.videoName ::text',
                    },
                    'video_region': {
                        'method': 'css',
                        'selector': 'ul.videoContent li span.region ::text',
                    },
                    'video_type': {
                        'method': 'css',
                        'selector': 'ul.videoContent li span.category ::text',
                    },
                    'url': {
                        'method': 'css',
                        'selector': 'ul.videoContent li a.address ::attr("href")',
                    },
                    'create_time': {
                        'method': 'css',
                        'selector': 'ul.videoContent li span.time ::text',
                    },
                },
            },
        }

    def __del__(self):
        try:
            del self.lg
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    xo = XOSpider()
    loop = get_event_loop()
    loop.run_until_complete(xo._fck_run())