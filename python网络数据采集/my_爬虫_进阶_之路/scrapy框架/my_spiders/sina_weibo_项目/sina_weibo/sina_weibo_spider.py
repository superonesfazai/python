# coding:utf-8

'''
@author = super_fazai
@File    : sina_weibo_spider.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from fzutils.ip_pools import fz_ip_pool
from fzutils.spider.async_always import *

class SinaWeiBoSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=fz_ip_pool
        )
        self.concurrency:int = 100
        # 某人的总微博数
        self.someone_all_blog_num:int = 0
        self.sema = Semaphore(self.concurrency)

    async def _get_phone_headers(self):
        return {
            'Accept': 'application/json, text/plain, */*',
            # 'Referer': 'https://m.weibo.cn/p/index?containerid=2304135370547595_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=2302835370547595',
            'MWeibo-Pwa': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': get_random_phone_ua(),
        }

    async def _fck_run(self):
        # 博主id
        # getIndex?containerid接口获取这两参数
        # container_id = '2304135370547595'
        # _value = '5370547595'
        container_id = '2304136004281123'
        _value = '6004281123'
        someone_all_blog = await self._get_someone_all_blog(container_id=container_id, _value=_value)
        print('该container_id: {}, 总微博数: {}'.format(container_id, len(someone_all_blog)))

    async def _get_someone_all_blog(self, container_id, _value) -> list:
        '''
        获取某人所有blog
        :return:
        '''
        async def _get_tasks_params_list() -> list:
            '''得到tasks_params_list'''
            nonlocal container_id, request_num, _value

            _ = [[container_id, _value, i] for i in range(1, request_num + 1)]

            return _

        # 先请求一次得到所有blog num
        await self._get_one_list_blog_info_from_all_blog(container_id=container_id, _value=_value, page_num=1)
        assert self.someone_all_blog_num != 0, 'someone_all_blog_num为0 !!'

        request_num = await self._get_request_num()
        print('someone_all_blog_num: {}, need request_num: {}'.format(self.someone_all_blog_num, request_num))

        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=await _get_tasks_params_list(),
            step=self.concurrency)
        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for item in slice_params_list:
                _value = item[1]
                page_num = item[2]
                print('create task[where page_num is {}]...'.format(page_num))
                tasks.append(self.loop.create_task(self._get_one_list_blog_info_from_all_blog(container_id=container_id, _value=_value, page_num=page_num)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            for item in one_res:
                if item != []:
                    all_res.append(item)

        return all_res

    async def _get_request_num(self) -> int:
        '''
        获取request数
        :return:
        '''
        async def _judge_float_type_behind_the_decimal_point_is_greater_than_zero(float_num: float) -> bool:
            '''
            判断某小数的小数点后面数字是否大于0
            :return:
            '''
            _ = int(re.compile('\.(\d+)').findall(str(float_num))[0])

            return True if _ > 0 else False

        # 需要进行的请求次数
        _ = self.someone_all_blog_num / 10
        _tmp = await _judge_float_type_behind_the_decimal_point_is_greater_than_zero(float_num=_)
        if _ < 1:
            request_num = 1
        else:
            if _tmp:
                request_num = int(_) + 1
            else:
                request_num = int(_)

        return request_num

    async def _get_one_list_blog_info_from_all_blog(self, container_id: str, _value:str, page_num: int) -> list:
        '''
        从全部微博中获取单页(list)微博信息
        :return:
        '''
        params = (
            ('containerid', '{}_-_WEIBO_SECOND_PROFILE_WEIBO'.format(container_id)),
            ('luicode', '10000011'),
            ('lfid', container_id),
            ('type', 'uid'),
            ('value', _value),
            ('page_type', '03'),
            ('page', page_num),
        )
        # getIndex?containerid
        url = 'https://m.weibo.cn/api/container/getIndex'
        with await self.sema:
            data = json_2_dict(await unblock_request(
                url=url,
                headers=await self._get_phone_headers(),
                params=params,
                ip_pool_type=self.ip_pool_type))
            self.someone_all_blog_num = data.get('data', {}).get('cardlistInfo', {}).get('total', 0) if self.someone_all_blog_num == 0 else self.someone_all_blog_num
            # pprint(data)
            cards = data.get('data', {}).get('cards', [])
            # 查看每次抓取状态
            try:
                print(cards[0]['mblog']['text'][:10])
            except Exception:
                pass
            label = '+' if cards != [] else '-'
            print('[{}] {}'.format(label, page_num))

            return cards

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = SinaWeiBoSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())