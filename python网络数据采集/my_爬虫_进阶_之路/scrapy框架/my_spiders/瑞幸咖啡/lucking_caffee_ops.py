# coding:utf-8

'''
@author = super_fazai
@File    : lucking_caffee_ops.py
@connect : superonesfazai@gmail.com
'''

"""
瑞幸caffee每日一杯
https://m.luckincoffee.com/invite/tangwei/MK20180301001
"""

from gc import collect
from fzutils.spider.async_always import *
from fzutils.register_utils import YiMaSmser

class LuckinCaffee(object):
    def __init__(self):
        self.loop = get_event_loop()
        with open('/Users/afa/myFiles/pwd/yima_pwd.json', 'r') as f:
            yima_info = json_2_dict(f.read())
        self.smser = YiMaSmser(username=yima_info['username'], pwd=yima_info['pwd'])
        self.project_id = 13665
        self._t = lambda : str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))

    async def _get_phone_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://m.luckincoffee.com/invite/tangwei/MK20180301001',
            'Connection': 'keep-alive',
        }

    async def _phone_num_get_quota(self, phone_num:str) -> bool:
        '''
        某个手机号获取名额
        :return:
        '''
        params = (
            ('q', dumps({
                'mobile': phone_num,
                'invitationCode': 'MK20180301001',
                'needOpenId': 0,
                '_': self._t()})),
        )
        url = 'https://m.luckincoffee.com/capi/resource/m/promo/activity/send'
        data = json_2_dict(Requests.get_url_body(url=url, headers=await self._get_phone_headers(), params=params))
        # pprint(data)
        if '已放入您{}luckin账户'.format(phone_num) in data.get('content', {}).get('msg', ''):
            return True

        return False

    async def _fck_run(self) -> bool:
        while True:
            phone_num = self.smser._get_phone_num(project_id=self.project_id)
            print(phone_num)
            a = input('是否可用: ')
            if a == 'y':
                break
        res = await self._phone_num_get_quota(phone_num=phone_num)
        print('[{}] {}领取{}!'.format('+' if res else '-', phone_num, '成功' if res else '失败'))

        a = input('是否继续登陆操作?(y/n):')
        if a == 'n':
            return False

        print('正在获取验证码中...请耐心等待!')
        sms_res = self.smser._get_sms(phone_num=phone_num, project_id=self.project_id, timeout=150)
        print('获取到的短信内容为: {}'.format(sms_res))

        return True

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = LuckinCaffee()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())