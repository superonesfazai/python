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
from fzutils.time_utils import fz_set_timeout
from fzutils.sms_utils import sms_2_somebody_by_twilio
from fzutils.safe_utils import get_uuid1

with open('/Users/afa/myFiles/pwd/twilio_pwd.json', 'r') as f:
    twilio_pwd_info = json_2_dict(f.read())

class MoneyCaffeine(object):
    """钱咖"""
    def __init__(self):
        self.loop = get_event_loop()
        self.sleep_time = 1.3
        self.account_sid = twilio_pwd_info['account_sid']
        self.auth_token = twilio_pwd_info['auth_token']

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

    @fz_set_timeout(11*60)
    def do_tasking(self):
        '''
        doing task
        :param auth_token:
        :return:
        '''
        sms_body = '抢到一个任务(uuid:{})请抓紧完成!'.format(get_uuid1())
        sms_res = sms_2_somebody_by_twilio(
            account_sid=self.account_sid,
            auth_token=self.auth_token,
            body=sms_body)
        label = '+' if sms_res else '-'
        print('[{}] 短信发送{}'.format(label, '成功!' if sms_res else '失败!'))

        while True:
            completed = input('已完成该任务请输入(y):')
            if completed in ('y', 'Y',):
                break
            else:
                print('输入有误!请重新输入!')
                pass

        return

    async def _fck_run(self):
        '''
        main
        :return:
        '''
        index = 1
        while True:
            try:
                tasks_list = await self._get_tasks_list()
                # pprint(tasks_list)
                assert tasks_list != {}, 'tasks_list为空dict!此处跳过!'
                now_tasks = [i for i in tasks_list.get('now_tasks', []) if i.get('qty', 0) != 0]
                # pprint(now_tasks)
                print('--->>> 发现任务个数: {}'.format(len(now_tasks)))
                tmp = await self._action()
                # pprint(tmp)

                _ = []
                for item in now_tasks:
                    task_id = item.get('id', '')
                    quality = item.get('qty', 0)
                    print('创建task: {}'.format(task_id))
                    _.append(self.loop.create_task(self._snatch_task(task_id=task_id, quality=quality)))

                try:
                    success_jobs, fail_jobs = await wait(_)
                except ValueError as e:
                    # assert e.args[0]
                    sleep(self.sleep_time)
                    continue

                print('success_num: {}, fail_num: {}'.format(len(success_jobs), len(fail_jobs)))
                # all_res为空则休眠
                all_res = []
                for r in success_jobs:
                    one = r.result().get('payload', {})
                    if one != {}:
                        all_res.append(one)
                pprint(all_res)
                assert all_res != [], 'all_res为空list!'

                for item in all_res:
                    message = item.get('message', '')
                    if '进行中' in message or '已抢到' in message:
                        print('抢到一个任务, 请抓紧完成!'.center(120, '@'))
                        try:
                            self.do_tasking()
                        except Exception as e:
                            print(e)
                        finally:
                            break
                    else:
                        pass

            except (AssertionError,) as e:
                print(e)
                ss = 5
                print('休眠{}s中...'.format(ss))
                sleep(ss)
            except KeyboardInterrupt:
                break
            finally:
                # await async_sleep(10)
                print('休眠{}s中...'.format(self.sleep_time))
                sleep(self.sleep_time)
                print('第 {} 次扫描结束...'.format(index).center(60, '-'))
                index += 1

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
