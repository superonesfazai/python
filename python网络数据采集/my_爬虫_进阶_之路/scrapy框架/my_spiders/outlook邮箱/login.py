# coding:utf-8

'''
@author = super_fazai
@File    : login.py
@connect : superonesfazai@gmail.com
'''

"""
outlook邮箱模拟登陆
"""

from gc import collect
from fzutils.spider.async_always import *
from requests import session
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class OutLookSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        self.usrname = 'fzupupup@outlook.com'
        self.pwd = 'xxxxxx'
        self.s = session()
        self._t = lambda : datetime_to_timestamp(get_shanghai_time())

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_csrf_params(self) -> dict:
        '''
        得到避免跨域请求的参数
        :return:
        '''
        params = (
            ('wa', 'wsignin1.0'),
            ('rpsnv', '13'),
            ('ct', self._t),
            ('rver', '7.0.6737.0'),
            ('wp', 'MBI_SSL'),
            ('wreply', 'https://outlook.live.com/owa/?ocid=MSNCNLG10-1&RpsCsrfState=b6131f1b-90e5-acef-dd3a-b238665f6b86'),
            ('id', '292841'),
            ('whr', 'outlook.com'),
            ('CBCXT', 'out'),
            ('lw', '1'),
            ('fl', 'dob,flname,wld'),
            ('cobrandid', '90015'),
        )
        response = self.s.get('https://login.live.com/login.srf', headers=await self._get_phone_headers(), params=params, cookies=None)
        body = response.text
        try:
            context_id = re.compile('contextid=(\w+)&').findall(body)[0]
            uaid = re.compile('uaid=(\w+)&').findall(body)[0]
            PPFT = re.compile('<input type=\"hidden\" name=\"PPFT\" id=\"\w+\" value=\"(.*?)\"').findall(body)[0]
            print('context_id:{}\nuaid:{}\nPPFT:{}\n'.format(context_id, uaid, PPFT))
        except IndexError as e:
            print(e)
            return {}

        return {
            'context_id': context_id,
            'uaid': uaid,
            'PPFT': PPFT,
        }

    async def _login_by_requests(self):
        '''
        通过requests模拟登陆
        :return:
        '''
        async def _get_params() -> tuple:
            nonlocal csrf_dict
            _t = self._t()
            return (
                ('wa', 'wsignin1.0'),
                ('rpsnv', '13'),
                ('ct', _t),
                ('rver', '7.0.6737.0'),
                ('wp', 'MBI_SSL'),
                ('wreply', 'https://outlook.live.com/owa/?ocid=MSNCNLG10-1&RpsCsrfState=b6131f1b-90e5-acef-dd3a-b238665f6b86'),
                ('id', '292841'),
                ('whr', 'outlook.com'),
                ('CBCXT', 'out'),
                ('lw', '1'),
                ('fl', 'dob,flname,wld'),
                ('cobrandid', '90015'),
                ('contextid', csrf_dict['context_id']),
                ('bk', _t),
                ('uaid', csrf_dict['uaid']),
                ('pid', '0'),
            )

        async def _get_form_data() -> dict:
            nonlocal csrf_dict
            return {
                'i13': '0',
                'login': self.usrname,
                'loginfmt': self.usrname,
                'type': '11',
                'LoginOptions': '3',
                'lrt': '',
                'lrtPartition': '',
                'hisRegion': '',
                'hisScaleUnit': '',
                'passwd': self.pwd,
                'ps': '2',
                'psRNGCDefaultType': '',
                'psRNGCEntropy': '',
                'psRNGCSLK': '',
                'canary': '',
                'ctx': '',
                'hpgrequestid': '',
                'PPFT': csrf_dict['PPFT'],
                'PPSX': 'PassportR',
                'NewUser': '1',
                'FoundMSAs': '',
                'fspost': '0',
                'i21': '0',
                'CookieDisclosure': '0',
                'IsFidoSupported': '1',
                'i2': '1',
                'i17': '0',
                'i18': '__ConvergedLoginPaginatedStrings|1,__OldConvergedLogin_PCore|1,',
                'i19': '64149'
            }

        # TODO: 原先采用requests模拟登陆成功后, 却返回请打开js才能继续访问, 使用login后的cookies赋值给driver, 被跳转到首页, 估计是防止跨域伪造
        # 至此直接采用模拟器进行模拟登陆 or 将答复的body在浏览器打开就会被定向到邮件内容页面
        csrf_dict = await self._get_csrf_params()
        assert csrf_dict != {}, 'csrf_dict返回空dict!'

        headers = await self._get_phone_headers()
        headers.update({
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.live.com',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        params = await _get_params()
        data = await _get_form_data()
        url = 'https://login.live.com/ppsecure/post.srf'
        response = self.s.post(url=url, headers=headers, params=params, data=data)
        body = response.text
        print(body)
        cookies = response.cookies.get_dict()
        pprint(cookies)
        # print(response.history)

        return body

    async def _fck_run(self):
        login_res = await self._login_by_requests()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = OutLookSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())