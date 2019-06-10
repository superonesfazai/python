# coding:utf-8

'''
@author = super_fazai
@File    : ok_resources_spider.py
@connect : superonesfazai@gmail.com
'''

"""
ok资源采集
"""

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import *

class OkResourcesSpider(AsyncCrawler):
    """
    ok电影资源: https://www.okzyw.com
    """
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.num_retries = 3
        # 最新电影截止页
        self.max_latest_page_num = 20

    async def _fck_run(self):
        """
        main
        :return:
        """
        all_latest_video_info_list = await self._get_all_the_latest_video_info()
        # 获取其播放信息
        ok_video_id_list = [{
            'ok_video_id': item.get('ok_video_id', ''),
        } for item in all_latest_video_info_list if item.get('ok_video_id', '') != '']
        await self._get_all_video_play_info_by_ok_video_id_list(ok_video_id_list=ok_video_id_list)

    async def _get_all_the_latest_video_info(self) -> list:
        """
        获取最新的video信息
        :return:
        """
        tasks = []
        func_name = self._get_the_latest_video_info_by_page_num
        for page_num in range(1, self.max_latest_page_num + 1):
            print('create task[where page_num: {}]...'.format(page_num))
            func_args = [
                page_num,
            ]
            tasks.append(self.loop.create_task(unblock_func(
                func_name=func_name,
                func_args=func_args,
                default_res=[],)))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        # pprint(all_res)
        all_latest_video_info_list = []
        for i in all_res:
            for j in i:
                all_latest_video_info_list.append(j)
        pprint(all_latest_video_info_list)
        print('all_latest_video_info_list len: {}'.format(len(all_latest_video_info_list)))
        try:
            del all_res
        except:
            pass

        return all_latest_video_info_list

    async def _get_all_video_play_info_by_ok_video_id_list(self, ok_video_id_list: list) -> list:
        """
        获取所有ok_video_id_list的video info
        :return:
        """
        tasks = []
        func_name = self._get_video_page_info_by_ok_video_id
        for item in ok_video_id_list:
            try:
                ok_video_id = item.get('ok_video_id', '')
                assert ok_video_id != ''
            except AssertionError:
                continue
            print('create task[where ok_video_id: {}]...'.format(ok_video_id))
            func_args = [
                ok_video_id,
            ]
            tasks.append(self.loop.create_task(unblock_func(
                func_name=func_name,
                func_args=func_args,
                default_res=[],)))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        pprint(all_res)
        print('_ len: {}'.format(len(_)))
        # try:
        #     del all_res
        # except:
        #     pass

        return all_res

    def _get_video_page_info_by_ok_video_id(self, ok_video_id: str) -> dict:
        """
        根据ok_video_id来获取video_page_info
        :return:
        """
        def parse(ok_video_id, body) -> dict:
            """
            解析
            :param body:
            :return:
            """
            m3u8_li_sel = {
                'method': 'css',
                'selector': 'div[id="2"] ul li ::text',
            }
            before_info_sel = {
                'method': 're',
                'selector': '(.*)\$',
            }
            video_play_url_sel = {
                'method': 're',
                'selector': '\$(.*)',
            }
            m3u8_li = parse_field(
                parser=m3u8_li_sel,
                target_obj=body,
                is_print_error=False,
                is_first=False,)
            # pprint(m3u8_li)
            new_m3u8_li = []
            for item in m3u8_li:
                try:
                    before_info = parse_field(
                        parser=before_info_sel,
                        target_obj=item,
                        is_print_error=False,)
                    # before_info可为空值
                    video_play_url = parse_field(
                        parser=video_play_url_sel,
                        target_obj=item,
                        is_print_error=False,)
                    assert video_play_url != ''
                except AssertionError as e:
                    # print(e)
                    continue
                new_m3u8_li.append({
                    'before_info': before_info,
                    'video_play_url': video_play_url,
                })

            print('[{}] ok_video_id: {}'.format(
                '+' if new_m3u8_li != [] else '-',
                ok_video_id,
            ))

            return {
                'ok_video_id': ok_video_id,
                'm3u8_li': new_m3u8_li,
            }

        headers = self.get_random_pc_headers()
        headers.update({
            'authority': 'www.okzyw.com',
            'cache-control': 'max-age=0',
        })
        params = (
            ('m', 'vod-detail-id-{}.html'.format(ok_video_id)),
        )
        body = Requests.get_url_body(
            url='https://www.okzyw.com/',
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        res = parse(ok_video_id=ok_video_id, body=body)

        return res

    def _get_the_latest_video_info_by_page_num(self, page_num: int) -> list:
        """
        通过page_num获取最新的单页电影信息
        :return:
        """
        def parse_page_info(body) -> list:
            """
            解析页面信息
            :param body:
            :return:
            """
            video_name_sel = {
                'method': 'css',
                'selector': 'span.xing_vb4 a ::text',
            }
            video_url_sel = {
                'method': 'css',
                'selector': 'span.xing_vb4 a ::attr("href")',
            }
            video_type_sel = {
                'method': 'css',
                'selector': 'span.xing_vb5 ::text',
            }
            video_time_sel = {
                'method': 'css',
                'selector': 'span.xing_vb7 ::text',
            }
            ok_video_id_sel = {
                'method': 're',
                'selector': 'vod-detail-id-(\d+)\.',
            }
            li_sel = {
                'method': 'css',
                'selector': 'div.xing_vb ul li',
            }
            li_list = parse_field(
                parser=li_sel,
                target_obj=body,
                is_first=False,
                is_print_error=False)
            res = []
            for li in li_list:
                try:
                    video_name = parse_field(
                        parser=video_name_sel,
                        target_obj=li,
                        is_print_error=False,)
                    assert video_name != ''
                    video_url = parse_field(
                        parser=video_url_sel,
                        target_obj=li,
                        is_print_error=False,)
                    video_url = 'https://www.okzyw.com' + video_url \
                        if video_url != '' else ''
                    assert video_url != ''
                    ok_video_id = parse_field(
                        parser=ok_video_id_sel,
                        target_obj=li,
                        is_print_error=False,)
                    assert ok_video_id != ''
                    video_type = parse_field(
                        parser=video_type_sel,
                        target_obj=li,
                        is_print_error=False,)
                    assert video_type != ''
                    video_time = parse_field(
                        parser=video_time_sel,
                        target_obj=li,
                        is_print_error=False,)
                    assert video_time != ''
                except AssertionError as e:
                    # print(e)
                    continue

                res.append({
                    'ok_video_id': ok_video_id,
                    'video_name': video_name,
                    'video_url': video_url,
                    'video_type': video_type,
                    'video_time': video_time,
                })

            return res

        headers = self.get_random_pc_headers()
        headers.update({
            'authority': 'www.okzyw.com',
            'referer': 'https://www.okzyw.com/',
        })
        params = (
            ('m', 'vod-index-pg-{}.html'.format(page_num)),
        )
        url = 'https://www.okzyw.com/'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.num_retries,)
        # print(body)
        res = parse_page_info(body=body)
        print('[{}] page_num: {}'.format(
            '+' if res != [] else '-',
            page_num
        ))

        return res

    @staticmethod
    def get_random_pc_headers():
        return {
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
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
    _ = OkResourcesSpider()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())