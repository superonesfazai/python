# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@connect : superonesfazai@gmail.com
'''

"""
启动:
1. celery -A tasks worker -l info -P eventlet -c 15
2. python3 main.py
"""

from tasks import (
    _test,
)
from gc import collect
from fzutils.spider.async_always import *
from fzutils.celery_utils import *

class Test(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        self.concurrency = 10

    async def _create_one_driver_tasks_obj(self, item):
        '''
        创建一个task对象
        :param item:
        :return:
        '''
        async_obj = _test.apply_async(
            args=[],
            expires=5 * 60,
            retry=False,)  # 避免无限重试

        return async_obj

    async def _get_all_async_handle_res(self, tasks_params_list) -> list:
        '''
        获取所有异步的结果
        :param tasks_params_list: 所有待处理的任务参数list
        :return:
        '''
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:  # 全部提取完毕, 正常退出
                break
            tasks = []
            for item in slice_params_list:
                print('创建task: {}...'.format(item))
                async_obj = await self._create_one_driver_tasks_obj(item=item)
                tasks.append(async_obj)

            one = await _get_celery_async_results(tasks=tasks)
            for i in one:
                all.append(i)

        return all

    async def _fck_run(self):
        tasks_params_list = range(20)
        all = await self._get_all_async_handle_res(tasks_params_list=tasks_params_list)
        # pprint(all)
        print('all个数:{}'.format(len(all)))

    def __del__(self):
        collect()

def main():
    _ = Test()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()