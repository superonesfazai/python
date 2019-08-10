# coding:utf-8

'''
@author = super_fazai
@File    : xo_spider.py
@connect : superonesfazai@gmail.com
'''

"""
xo spiders
"""

from items import (
    VideoListItem,
    VideoItem,)
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
        self.max_n15_japan_page_num = 3
        self.max_n15_all_page_num = 20

    async def _fck_run(self):
        # await self.s69zy3_spider()
        await self.n15_spider()

    async def n15_spider(self):
        """
        target_url[七色]: https://7.n15.info
        :return:
        """
        self.parser_obj = self.get_parser_obj()['n15']
        all_video_list = await self.get_n15_some_label_all_video_list_by_label_name(
            label_name='所有分类',)
        await self.get_n15_all_video_info_by_video_list(
            video_list=all_video_list,)

    async def get_n15_some_label_all_video_list_by_label_name(self, label_name: str='日本') -> list:
        """
        根据label_name获取所有对应的video_list
        :return:
        """
        def get_tasks_params_list():
            tasks_params_list = []
            sort_name_dict = self.get_n15_all_sort_label_name_dict(sort_name=label_name)
            max_page_num = sort_name_dict.get('max_page_num', 0)
            sort_type = sort_name_dict.get('sort_type', '')
            assert sort_type != ''

            for page_num in range(1, max_page_num + 1):
                tasks_params_list.append({
                    'page_num': page_num,
                    'label_name': label_name,
                    'sort_type': sort_type,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where type: {}, page_num: {}] ...'.format(
                k['label_name'],
                k['page_num'],
            )

        def get_now_args(k) -> list:
            return [
                k['label_name'],
                k['sort_type'],
                k['page_num'],
            ]

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_n15_video_list_by_label_name_and_page_num,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
            one_default_res=[],
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,)
        pprint(all_res)
        print('获取{} video_all_res_num: {}'.format(label_name, len(all_res)))
        all_res = list_remove_repeat_dict_plus(
            target=all_res,
            repeat_key='video_name',)
        print('实际获取{} video_all_res_num: {}'.format(label_name, len(all_res)))

        return all_res

    def get_n15_all_sort_label_name_dict(self, sort_name: str) -> dict:
        """
        获取n15所有分类信息
        :return:
        """
        sort_info_dict = {
            '日本': {
                'label_name': '日本',
                'max_page_num': self.max_n15_japan_page_num,
                'sort_type': 'japan',
            },
            '所有分类': {
                'label_name': '所有分类',
                'max_page_num': self.max_n15_all_page_num,
                'sort_type': 'all',
            },
        }
        if sort_name not in sort_info_dict.keys():
            raise ValueError('sort_name value 异常!'.format(sort_name))

        return sort_info_dict.get(sort_name, {})

    async def get_n15_all_video_info_by_video_list(self, video_list: list) -> list:
        """
        根据video_list获取n15对应的所有video_info
        :return:
        """
        def get_tasks_params_list():
            tasks_params_list = []
            for item in video_list:
                tasks_params_list.append({
                    'video_url': item['url'],
                    'base_video_info': item,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where video_url: {}] ...'.format(
                k['video_url'],
            )

        def get_now_args(k) -> list:
            return [
                k['video_url'],
                k['base_video_info'],
            ]

        def add_one_res_2_all_res(one_res: list, all_res: list):
            for item in one_res:
                all_res.append(item)

            return all_res

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_n15_some_video_info_by_video_url,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=add_one_res_2_all_res,
            one_default_res={},
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,)
        pprint(all_res)
        print('all_res_num: {}'.format(len(all_res)))

        return all_res

    @catch_exceptions_with_class_logger(default_res={})
    def get_n15_some_video_info_by_video_url(self, video_url, base_video_info: dict) -> dict:
        """
        根据video_url获取video info
        :param url:
        :param base_video_info: 原先的video基础信息
        :return:
        """
        headers = get_random_headers(
            connection_status_keep_alive=False,)
        headers.update({
            'authority': '7.n15.info',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'none',
            # 'cookie': '_ga=GA1.2.458296239.1565329933; _gid=GA1.2.679615192.1565329933; XSRF-TOKEN=eyJpdiI6IjNtUkRiTVZqN09pTGVKS200c25Canc9PSIsInZhbHVlIjoibFJUeFdVU3g0KzhQcThtRlVuUE9zMXZoQVpsM28yUXh3aDN2UUZvR0VRc05EVHJncFA3QzBNNEN0UkNIUm1BUSIsIm1hYyI6ImZjMmE2NGY1N2E4NmQ5NDRhMTU1YTA1ZGFjOTM5ZDEyMWU5OGYwNjRkM2I5M2I4Y2ZmYmViYzljZThhOGI2MGQifQ%3D%3D; july_session=eyJpdiI6InZmRVVzWnpJTlowMDVNWnNMQys1OHc9PSIsInZhbHVlIjoidTZmRDBHQUI3TDZ2bUlRNkdRUW1pWmZ0bFE5Tmxrb0pPR2RHdzU4NFl0dWk4YTBJMWw4VnNsMWNBMmtYSUNMUSIsIm1hYyI6ImJiZTY2NTNkNzZhMGM3ZjA1ZmM0MjIzZDUwYmE5NzhjMjAwYTgwZWZiMjgyNTBmMGEwY2YzOGFkNDE4MTEyMDcifQ%3D%3D',
        })
        body = Requests.get_url_body(
            url=video_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,)
        # self.lg.info(body)
        assert body != ''

        res = self.parse_video_page_body_by_short_name(
            short_name='n15',
            body=body,)
        self.lg.info('[{}] video_url: {}'.format(
            '+' if res != {} else '-',
            video_url,
        ))
        # 增加base_video_info
        res.update({
            'base': base_video_info,
        })

        return res

    @catch_exceptions_with_class_logger(default_res=[])
    def get_n15_video_list_by_label_name_and_page_num(self, label_name: str, sort_type: str, page_num: int) -> list:
        """
        根据page_num获取单页中日本video信息
        :param page_num:
        :return:
        """
        headers = get_random_headers(
            connection_status_keep_alive=False,
            cache_control='',)
        headers.update({
            'authority': '7.n15.info',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'same-origin',
            # 'referer': 'https://7.n15.info/videos/japan/free',
            # 'cookie': '_ga=GA1.2.458296239.1565329933; _gid=GA1.2.679615192.1565329933; XSRF-TOKEN=eyJpdiI6ImVPdzJ5UldEZ3lqS3l3amJ4MTcwb2c9PSIsInZhbHVlIjoiczRpcmVRcHBKTWs5enNUN20xWTh2eDJQXC9ZSHcrc0dtTjlZUXY3QUpOUndBZ0hDaVN1RGh4VzVrZW51U3hUaWIiLCJtYWMiOiJkMTM2ODA4ODZhMTA0M2Q5NGE0MTgwNTYwOWM3ZTMwOTIzYjNjNjAyMGUwMWQwZmVkN2QxMjU5OWM0N2UzMTk1In0%3D; july_session=eyJpdiI6ImpcL0tpSFwvMlJRdVg1SmZcL21ZTSs5NlE9PSIsInZhbHVlIjoiNGllcm5LdEhSdlwvYjdqSGRSdmx1NWtja2tHUzk5cTBNYm5adVd2UVJZN2JYaVB2aUtcLytXWUdOd2lvUW5CY244IiwibWFjIjoiYmVhYTQ0YjRkYTU1OGQ2ZjU3MWVkODdkNjg2NTQzMTM5ZTZmOWJlM2Y2NmYyN2I3MGUwODlkYWU3YjUyZjRhMiJ9',
        })
        params = (
            ('page', str(page_num)),
        )
        url = 'https://7.n15.info/videos/{}/free'.format(sort_type)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,)
        # self.lg.info(body)
        assert body != ''

        res = self.parse_video_list_page_body_by_short_name(
            short_name='n15',
            label_name='日本',        # 所有分类解析对象跟日本的相同, 故取日本
            body=body)
        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    async def s69zy3_spider(self):
        """
        target_url: http://www.s69zy3.com
        :return:
        """
        # todo 其播放页的video标签 src是blob格式的, 但其介绍页m3u8地址即为播放地址(https)
        self.parser_obj = self.get_parser_obj()['s69']
        await self.get_s69_all_chinese_captions_video_list()

    async def get_s69_all_chinese_captions_video_list(self) -> list:
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
            func_name=self.get_s69_chinese_captions_video_list_by_page_num,
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
    def get_s69_chinese_captions_video_list_by_page_num(self, page_num: int) -> list:
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

        res = self.parse_video_list_page_body_by_short_name(
            short_name='s69',
            label_name='中文字幕',
            body=body)
        self.lg.info('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num,
        ))

        return res

    @catch_exceptions_with_class_logger(default_res={})
    def parse_video_page_body_by_short_name(self, short_name: str, body) -> dict:
        """
        解析单页video info
        :param short_name:
        :param body:
        :return:
        """
        def parse_video_name():
            video_name = parse_field(
                parser=self.parser_obj['video_info']['video_name'],
                target_obj=body,
                logger=self.lg, )
            assert video_name != ''

            return video_name

        def parse_static_img_url():
            static_img_url = parse_field(
                parser=self.parser_obj['video_info']['static_img_url'],
                target_obj=body,
                logger=self.lg,)

            if short_name == 'n15':
                static_img_url = 'https:' + static_img_url if static_img_url != '' else ''
            else:
                pass

            return static_img_url

        def parse_video_url():
            video_url = parse_field(
                parser=self.parser_obj['video_info']['video_url'],
                target_obj=body,
                logger=self.lg, )
            assert video_url != ''

            if short_name == 'n15':
                # 用http, 部分地址https无法正常显示
                video_url = 'http:' + video_url if video_url != '' else ''
            else:
                pass

            return video_url

        def parse_like_num():
            like_num = parse_field(
                parser=self.parser_obj['video_info']['like_num'],
                target_obj=body,
                logger=self.lg, )

            try:
                like_num = int(like_num)
            except:
                like_num = 0

            return like_num

        def parse_dislike_num():
            dislike_num = parse_field(
                parser=self.parser_obj['video_info']['dislike_num'],
                target_obj=body,
                logger=self.lg, )

            try:
                dislike_num = int(dislike_num)
            except:
                dislike_num = 0

            return dislike_num

        def parse_collected_num():
            collected_num = parse_field(
                parser=self.parser_obj['video_info']['collected_num'],
                target_obj=body,
                logger=self.lg,)

            try:
                collected_num = int(collected_num)
            except:
                collected_num = 0

            return collected_num

        video_item = VideoItem()
        video_item['video_name'] = parse_video_name()
        video_item['static_img_url'] = parse_static_img_url()
        video_item['video_url'] = parse_video_url()
        video_item['like_num'] = parse_like_num()
        video_item['dislike_num'] = parse_dislike_num()
        video_item['collected_num'] = parse_collected_num()

        return dict(video_item)

    @catch_exceptions_with_class_logger(default_res=[])
    def parse_video_list_page_body_by_short_name(self, short_name: str, label_name: str, body,) -> list:
        """
        解析s63电影列表页的body
        :param short_name:
        :param label_parser_obj_dict: 目标标签解析对象
        :param body:
        :return:
        """
        video_name_list = parse_field(
            parser=self.parser_obj[label_name]['video_name'],
            target_obj=body,
            logger=self.lg,
            is_first=False,)
        # pprint(video_name_list)
        video_region_list = parse_field(
            parser=self.parser_obj[label_name]['video_region'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(video_region_list)
        video_type_list = parse_field(
            parser=self.parser_obj[label_name]['video_type'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(video_type_list)
        url_list = parse_field(
            parser=self.parser_obj[label_name]['url'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(url_list)
        create_time_list = parse_field(
            parser=self.parser_obj[label_name]['create_time'],
            target_obj=body,
            logger=self.lg,
            is_first=False, )
        # pprint(create_time_list)

        res = []
        if short_name == 's69':
            assert video_name_list != []
            assert video_region_list != []
            assert video_type_list != []
            assert url_list != []
            assert create_time_list != []

            _ = list(zip(
                video_name_list,
                video_region_list,
                video_type_list,
                url_list,
                create_time_list, ))
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

        elif short_name == 'n15':
            assert video_name_list != []
            assert url_list != []

            _ = list(zip(video_name_list, url_list))
            for item in _:
                try:
                    url = 'https://7.n15.info' + item[1] if item[1] != '' else ''
                    assert url != ''
                    video_list_item = VideoListItem()
                    video_list_item['video_name'] = item[0]
                    video_list_item['video_region'] = '未知'
                    video_list_item['video_type'] = label_name
                    video_list_item['url'] = url
                    video_list_item['create_time'] = get_shanghai_time()
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue
                res.append(dict(video_list_item))

        else:
            raise NotImplemented

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
                '中文字幕': {
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
                'video_info': {
                },
            },
            'n15': {
                '日本': {
                    'video_name': {
                        'method': 'css',
                        'selector': 'div.video-elem a.title ::text',
                    },
                    'video_region': None,
                    'video_type': None,
                    'url': {
                        'method': 'css',
                        'selector': 'div.video-elem a.title ::attr("href")',
                    },
                    'create_time': None,
                },
                'video_info': {
                    'video_name': {
                        'method': 'css',
                        'selector': 'h4.container-title ::text',
                    },
                    'static_img_url': {
                        'method': 'css',
                        'selector': 'div video ::attr("data-poster")',
                    },
                    'video_url': {
                        'method': 'css',
                        'selector': 'div video ::attr("data-src")',
                    },
                    'like_num': {
                        'method': 'css',
                        'selector': 'span.likeBtn span ::text',
                    },
                    'dislike_num': {
                        'method': 'css',
                        'selector': 'span.dislikeBtn span ::text',
                    },
                    'collected_num': {
                        'method': 'css',
                        'selector': 'span.favoriteBtn span ::text',
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