# coding:utf-8

'''
@author = super_fazai
@File    : meijutt_spider.py
@connect : superonesfazai@gmail.com
'''

"""
美剧天堂爬虫
"""

from gc import collect
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

class MeiJuTTSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool,
        )
        self.concurrency = 25

    async def _fck_run(self):
        all_ranking_list = await self._get_ranking_list()
        pprint(all_ranking_list)
        if all_ranking_list == []:
            print('获取到all_ranking_list为空值!')
            return None

        new_all_ranking_list = await self._get_all_ranking_tv_play_detail_info(all_ranking_list)
        pprint(new_all_ranking_list)

    async def _get_ranking_list(self) -> list:
        '''
        获取美剧天堂的排行榜
        :return: [{'hot_label': xxx:str, 'ranking_info': xxx:list}, ...]
        '''
        async def _parse_ranking_list(body) -> list:
            '''解析排行榜'''
            hot_label_list = Selector(text=body).css('div.view-filter.ldgtabhot a ::text').extract() or []
            hot_label_ul_list = Selector(text=body).css('ul.fn-clear').extract() or []
            all = []
            for index, item in enumerate(hot_label_ul_list):
                _ = []
                for li in Selector(text=item).css('li').extract() or []:
                    try:
                        video_url = Selector(text=li).css('li a ::attr("href")').extract_first() or ''
                        assert video_url != '', 'video_url为空值!'
                        video_url = 'https://m.meijutt.com' + video_url
                        title = Selector(text=li).css('li a span.l ::text').extract_first() or ''
                        assert title != '', 'title为空值!'
                        ranking = int(re.compile('(\d+) .*?').findall(title)[0])
                        title = re.compile(' .*').findall(title)[0].replace(' ', '', 1)     # 去除左边的' '
                        score_big = Selector(text=li).css('li a span.m strong ::text').extract_first() or ''
                        score_small = Selector(text=li).css('li a span.m span ::text').extract_first() or ''
                        score = round(float(score_big + score_small), 2)
                        progress = Selector(text=li).css('li a span.r font ::text').extract_first() or ''
                        assert progress != '', 'progress为空值!'
                    except (AssertionError, IndexError, ValueError) as e:
                        print(e)
                        continue

                    _.append({
                        'video_url': video_url,
                        'title': title,
                        'ranking': ranking,         # 排名
                        'score': score,             # 分值
                        'progress': progress,       # 进度
                    })

                all.append({
                    'hot_label': hot_label_list[index],
                    'ranking_info': _
                })

            return all

        url = 'https://m.meijutt.com/alltop_hit.html'
        body = await unblock_request(url=url, headers=await self._get_phone_headers(), encoding='gb2312')
        # print(body)
        if body == '':
            print('获取到的body为空值!')
            return []

        return await _parse_ranking_list(body)

    async def _get_all_ranking_tv_play_detail_info(self, all_ranking_list) -> list:
        '''
        获取排名中所有tv play的详情
        :return:
        '''
        async def _get_tasks_params_list() -> list:
            '''获取任务参数'''
            nonlocal all_ranking_list

            tasks_params_list = []
            for item in all_ranking_list:
                ranking_info = item['ranking_info']
                for i in ranking_info:
                    i['update_time'] = ''
                    tasks_params_list.append((i['title'], i['video_url']))

            return tasks_params_list

        tasks_args_list_obj = TasksParamsListObj(
            tasks_params_list=await _get_tasks_params_list(),
            step=self.concurrency)
        all = []
        while True:
            try:
                slice_args_list = tasks_args_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for item in slice_args_list:
                print('create task[where title is {}] ...'.format(item[0]))
                tasks.append(self.loop.create_task(self._get_one_tv_play_detail_info(title=item[0], video_url=item[1])))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            for i in one_res:
                if i[1] != {}:
                    all.append(i)

        print(len(all))
        # 更新all_ranking_list
        for item in all:
            title = item[0]
            detail_info = item[1]
            for i in all_ranking_list:
                for j in i.get('ranking_info', []):
                    if j.get('title', '') == title:
                        j['update_time'] = detail_info.get('update_time', '')

        return all_ranking_list

    async def _get_one_tv_play_detail_info(self, title, video_url) -> tuple:
        '''
        获取电视剧的详情
        :return: (title, dict)
        '''
        async def _parse_tv_play_detail_info(body) -> dict:
            '''解析电视剧的详情'''
            _ = {}
            try:
                try:
                    update_time = re.compile('更新时间：(.*?)</p>').findall(body)[0]
                except IndexError:
                    raise IndexError('获取update_time时索引异常!')
            except Exception as e:
                print(e)
                return {}

            _.update({
                'update_time': update_time,
            })

            return _

        body = await unblock_request(url=video_url, headers=await self._get_phone_headers(), encoding='gb2312')
        # print(body)
        if body == '':
            print('获取video_url: {} 的body为空值!'.format(video_url))
            return (title, {})

        return (title, await _parse_tv_play_detail_info(body=body))

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'https://www.meijutt.com/alltop_hit.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = MeiJuTTSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
