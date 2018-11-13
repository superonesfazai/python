# coding:utf-8

'''
@author = super_fazai
@File    : v2ex_spider.py
@connect : superonesfazai@gmail.com
'''

"""
v2ex爬虫(https://www.v2ex.com)
"""

from gc import collect
from requests import session
from fzutils.spider.async_always import *

with open('/Users/afa/myFiles/pwd/v2ex_pwd.json', 'r') as f:
    v2ex_info = json_2_dict(f.read())

class V2EXSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        self.concurrency = 10
        self.s = session()
        self.username = v2ex_info['username']
        self.pwd = v2ex_info['pwd']

    async def _get_phone_headers(self):
        return {
            'authority': 'www.v2ex.com',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    async def _get_login_necessary_params(self) -> dict:
        '''
        得到登陆所必须的参数
        :return:
        '''
        response = self.s.get('https://www.v2ex.com/signin', headers=await self._get_phone_headers())
        body = response.text
        # print(body)
        try:
            name = Selector(text=body).css('input.sl:nth-child(1) ::attr("name")').extract()[0] or ''
            pwd = Selector(text=body).css('input.sl:nth-child(2) ::attr("name")').extract_first() or ''
            once = re.compile('value=\"(\d+)\" name=\"once\" />').findall(body)[0]
            robot = Selector(text=body).css('input.sl:nth-child(1) ::attr("name")').extract()[1] or ''
            print('name:{}\npwd:{}\nonce:{}\nrobot:{}'.format(name, pwd, once, robot))
        except IndexError as e:
            print(e)
            return {}

        captcha_url = 'https://www.v2ex.com/_captcha?once={}'.format(once)

        return {
            'name': name,
            'pwd': pwd,
            'once': once,
            'robot': robot,
            'captcha_url': captcha_url,
        }

    async def _login(self) -> bool:
        '''
        登陆m站
        :return:
        '''
        _ = await self._get_login_necessary_params()
        if _ == {}:
            print('获取登陆参数失败!')
            return False

        captcha_url = _['captcha_url']
        print('验证码地址:{}'.format(captcha_url))
        captcha = input('请输入查看到的验证码:')

        headers = await self._get_phone_headers()
        headers.update({
            'cache-control': 'max-age=0',
            'origin': 'https://www.v2ex.com',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://www.v2ex.com/signin',
        })
        data = {
            'next': '/',
            _['name']: self.username,
            'once': _['once'],
            _['pwd']: self.pwd,
            _['robot']: captcha,  # 识别的验证码
        }
        pprint(data)
        # response = requests.post('https://www.v2ex.com/signin', headers=headers, data=data)
        # print(response.text)

        return True

    async def _fck_run(self):
        login_res = await self._login()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = V2EXSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())