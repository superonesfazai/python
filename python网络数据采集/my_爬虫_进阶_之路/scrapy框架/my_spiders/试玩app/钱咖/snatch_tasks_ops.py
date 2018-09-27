# coding:utf-8

'''
@author = super_fazai
@File    : snatch_tasks_ops.py
@connect : superonesfazai@gmail.com
'''

"""
钱咖自动抢任务
"""

from gc import collect
from asyncio import get_event_loop, wait
from asyncio import sleep as async_sleep
from time import sleep
from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.common_utils import json_2_dict

class MoneyCaffeine(object):
    """钱咖"""
    def __init__(self):
        self.loop = get_event_loop()
        self.sleep_time = 5

    async def _get_cookies(self):
        return {
            'DIS4': 'cf31af399b8f444ab2feb7235a6d1d59',
            '_uab_collina': '153794227445918868865459',
            'ln': '1',
            'lu': '47204417',
            'user_redirct_subtask_list': '1',
        }

    async def _get_base_headers(self):
        return {
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'br, gzip, deflate',
            'Host': 'qianka.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f version=2.0.2018091401 bid=cook.chi.app',
            'Accept-Language': 'zh-cn',
        }

    async def _get_tasks_list(self) -> dict:
        '''
        拿到所有任务list
        :return:
        '''
        headers = await self._get_base_headers()
        headers.update({'Referer': 'https://qianka.com/v4/tasks/lite'})
        url = 'https://qianka.com/s4/lite.subtask.list'
        data = json_2_dict(Requests.get_url_body(url=url, headers=headers, cookies=await self._get_cookies())).get('payload', {})
        # pprint(data)
        if data == {}:
            return {}

        high_earn_tasks = data.get('highearn_list', [])
        incoming_tasks = data.get('incoming', [])
        now_tasks = data.get('tasks', [])
        res = {
            'high_earn_tasks': high_earn_tasks,     # 高赚
            'incoming_tasks': incoming_tasks,       # 预告
            'now_tasks': now_tasks,                 # 当前
        }
        # pprint(res)

        return res

    async def _action(self) -> dict:
        headers = await self._get_base_headers()
        headers.update({
            'Origin': 'https://qianka.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://qianka.com/v4/tasks/lite',
            'Content-Length': '51',
        })
        data = {
            'action_id': '120',
            'ext4': '2ded7c7731b21ec6b057351da4369f5a'
        }
        url = 'https://qianka.com/s5/user.action'
        data = json_2_dict(Requests.get_url_body(method='post', url=url, headers=headers, cookies=await self._get_cookies(), data=data))
        # pprint(data)

        return data

    async def _snatch_task(self, task_id, quality):
        '''
        抢活
        :return:
        '''
        headers = await self._get_base_headers()
        headers.update({'Referer': 'https://qianka.com/v4/tasks/lite',})
        params = (
            ('task_id', str(task_id)),
            ('quality', str(quality)),
        )

        url = 'https://qianka.com/s4/lite.subtask.start'
        data = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params, cookies=await self._get_cookies()))

        return data

    async def _fck_run(self):
        '''
        main
        :return:
        '''
        while True:
            try:
                tasks_list = await self._get_tasks_list()
                # pprint(tasks_list)
                assert tasks_list != {}, 'tasks_list为空dict!此处跳过!'
                now_tasks = [i for i in tasks_list.get('now_tasks', []) if i.get('qty', 0) != 0]
                pprint(now_tasks)

                tmp = await self._action()
                # pprint(tmp)

                _ = []
                for item in now_tasks:
                    task_id = item.get('id', '')
                    quality = item.get('qty', 0)
                    print('创建task: {}'.format(task_id))
                    _.append(self.loop.create_task(self._snatch_task(task_id=task_id, quality=quality)))

                success_jobs, fail_jobs = await wait(_)
                print('success_num: {}, fail_num: {}'.format(len(success_jobs), len(fail_jobs)))
                all_res = [r.result().get('payload', {}) for r in success_jobs]
                pprint(all_res)

            except (AssertionError,) as e:
                print(e)
            except KeyboardInterrupt:
                break
            finally:
                # await async_sleep(10)
                print('休眠{}s中...'.format(self.sleep_time))
                sleep(self.sleep_time)

        print('KeyboardInterrupt暂停!')

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = MoneyCaffeine()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())