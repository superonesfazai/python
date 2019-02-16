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
from requests import post

from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

with open('/Users/afa/myFiles/pwd/twilio_pwd.json', 'r') as f:
    twilio_pwd_info = json_2_dict(f.read())
with open('/Users/afa/myFiles/pwd/server_sauce_sckey.json', 'r') as f:
    sc_key_info = json_2_dict(f.read())

class MoneyCaffeine(AsyncCrawler):
    """钱咖"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,)
        self.sleep_time = 1.
        self.account_sid = twilio_pwd_info['account_sid']
        self.auth_token = twilio_pwd_info['auth_token']
        self.sc_key = sc_key_info['sckey']

    async def _fck_run(self):
        '''
        main
        :return:
        '''
        index = 1
        while True:
            now_time = get_shanghai_time()
            if now_time.hour > 0 and now_time.hour < 6:
                print('{}不在工作范围...'.format(str(now_time)))
                sleep(60)
                continue

            try:
                tasks_list = await self._get_tasks_list()
                # pprint(tasks_list)
                assert tasks_list != {}, 'tasks_list为空dict!此处跳过!'
                now_tasks = [i for i in tasks_list.get('now_tasks', []) if i.get('qty', 0) != 0]
                # pprint(now_tasks)
                print('--->>> 发现任务个数: {}'.format(len(now_tasks)))
                tmp = await self._action()
                # pprint(tmp)

                tasks = []
                for item in now_tasks:
                    task_id = item.get('id', '')
                    quality = item.get('qty', 0)
                    print('创建task: {}'.format(task_id))
                    tasks.append(self.loop.create_task(self._snatch_task(task_id=task_id, quality=quality)))

                try:
                    success_jobs, fail_jobs = await wait(tasks)
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
                            with async_timeout(timeout=60*4):
                                await self.do_tasking()
                        except (AsyncTimeoutError, Exception) as e:
                            print(e)
                        finally:
                            break
                    else:
                        pass

            except (AssertionError,) as e:
                print(e)
                ss = 4.5
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
        data = json_2_dict(
            json_str=Requests.get_url_body(
                url=url,
                headers=headers,
                cookies=await self._get_cookies(),
                ip_pool_type=self.ip_pool_type,)
            ).get('payload', {})
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
        body = Requests.get_url_body(
            method='post',
            url=url,
            headers=headers,
            cookies=await self._get_cookies(),
            data=data,
            ip_pool_type=self.ip_pool_type,)
        # print(body)
        data = json_2_dict(body)
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
        # 阻塞
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            cookies=await self._get_cookies(),
            ip_pool_type=self.ip_pool_type,)
        data = json_2_dict(body)
        # pprint(data)

        return data

    async def real_time_remind_by_china_unicom(self, phone_num=18698570079) -> bool:
        '''
        通过联通提醒抢到任务(免费)
        :param phone_num:
        :return:
        '''
        res = False
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Referer': 'https://uac.10010.com/portal/homeLoginNew',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        print(t)
        params = (
            ('callback', 'jQuery172017190182360065043_{}'.format(t)),
            ('req_time', t),
            ('mobile', str(phone_num)),
            ('_', t),
        )
        # resultCode 0000 表示发送成功
        url = 'https://uac.10010.com/portal/Service/SendMSG'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            params=params,
            cookies=None,
            ip_pool_type=self.ip_pool_type,)
        try:
            body = re.compile('\((.*)\)').findall(body)[0]
            res_code = json_2_dict(body).get('resultCode', '0')
            if res_code == '0000':
                res = True
        except IndexError:
            pass

        return res

    async def _send_msg_to_wx(self):
        '''
        发送内容给微信
        :return:
        '''
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://sc.ftqq.com/?c=code',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        data = {
            'text': '钱咖新任务!!',                     # title
            'desp': get_uuid1(),    # content
        }
        url = 'http://sc.ftqq.com/{}.send'.format(self.sc_key)
        with post(url=url, headers=headers, data=data) as resp:
            send_res = json_2_dict(resp.text).get('errmsg', 'success')

        if send_res == 'success':
            return True
        else:
            return False

    async def do_tasking(self):
        '''
        doing task
        :return:
        '''
        # send sms by twilio
        # sms_body = '抢到一个任务(uuid:{})请抓紧完成!'.format(get_uuid1())
        # sms_res = sms_2_somebody_by_twilio(
        #     account_sid=self.account_sid,
        #     auth_token=self.auth_token,
        #     body=sms_body)

        # send sms by 联通
        # sms_res = await self.real_time_remind_by_china_unicom()
        # label = '+' if sms_res else '-'
        # print('[{}] 短信发送{}'.format(label, '成功!' if sms_res else '失败!'))

        # send msg to wx
        sms_res = await self._send_msg_to_wx()
        print('[{}] 推送到微信{}!'.format('+' if sms_res else '-', '成功' if sms_res else '失败'))
        while True:
            completed = input('已完成该任务请输入(y):')
            if completed == 'y':
                break

        return

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

