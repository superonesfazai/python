# coding:utf-8

'''
@author = super_fazai
@File    : pressure_test.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.async_always import *

class YXPT(AsyncCrawler):
    """yiuxiu压测"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,)
        # 100个10s, 500个33s, 800个54s, 1500个100s
        self.concurrency = 500
        # 单次请求超时
        self.request_timeout = 9.
        # 控制网络请求并发量
        self.sema = Semaphore(self.concurrency + 1)

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _fck_run(self):
        await self._main_page_all()

    async def _main_page_all(self):
        '''
        main page all test
        :return:
        '''
        RANGE = range(1000)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=RANGE, step=self.concurrency)
        all = []
        success_count = 0
        while True:
            try:
                slice_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for index in slice_list:
                    print('create task [where is {}]'.format(index))
                    tasks.append(self.loop.create_task(_._main_page_one_test(index=index)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            for i in one_res:
                if i:
                    success_count += 1
                all.append(i)

        print('成功率: {}'.format(success_count/len(all)))

    async def _main_page_one_test(self, **kwargs) -> bool:
        '''
        main page one test
        :return:
        '''
        index = kwargs['index']

        res = False
        url = 'https://m.yiuxiu.com/'
        with await self.sema:
            body = await unblock_request(
                url=url,
                headers=await self._get_phone_headers(),
                timeout=self.request_timeout,
                ip_pool_type=self.ip_pool_type)
            # body = await AioHttp.aio_get_url_body(
            #     url=url,
            #     headers=await self._get_phone_headers(),
            #     timeout=self.request_timeout,
            #     ip_pool_type=self.ip_pool_type,
            #     verify_ssl=False,)
            # print(body)
            if '优秀网' in body:
                res = True

            label = '+' if res else '-'
            print('[{}] task index {}'.format(label, index))

            return res

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = YXPT()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())