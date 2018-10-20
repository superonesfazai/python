# coding:utf-8

'''
@author = super_fazai
@File    : linkedin_spider.py
@connect : superonesfazai@gmail.com
'''

"""
linkedin爬虫
"""

from gc import collect
from requests import session
from fzutils.spider.async_always import *

class LinkedinSpider(object):
    def __init__(self, username, pwd):
        self.loop = get_event_loop()
        self.username, self.pwd = username, pwd

    async def _get_headers(self):
        return {
            'origin': 'https://www.linkedin.com',
            'authority': 'www.linkedin.com',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://www.linkedin.com/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    async def _login(self) -> bool:
        '''
        登陆
        :return:
        '''
        with session() as s:
            params = (
                ('session_redirect', ''),
                ('goback', ''),
                ('trk', 'hb_signin'),
            )

            response = s.get('https://www.linkedin.com/uas/login', headers=await self._get_headers(), params=params)
            login_page_body = response.text
            try:
                loginCsrfParam = re.compile('name=\"loginCsrfParam\" value=\"(.*?)\"').findall(login_page_body)[0]
                csrfToken = re.compile('name=\"csrfToken\" value=\"(.*?)\"').findall(login_page_body)[0]
                sourceAlias = re.compile('name=\"sourceAlias\" value=\"(.*?)\"').findall(login_page_body)[0]
            except IndexError as e:
                print(e)
                return False
            print('loginCsrfParam: {}\ncsrfToken: {}\nsourceAlias: {}\n'.format(loginCsrfParam, csrfToken, sourceAlias))

            headers = await self._get_headers()
            headers.update({
                'content-type': 'application/x-www-form-urlencoded',
                'accept': 'text/plain, */*; q=0.01',
                'x-isajaxform': '1',
                'x-requested-with': 'XMLHttpRequest',
                'referer': 'https://www.linkedin.com/uas/login?session_redirect=&goback=&trk=hb_signin',
            })

            data = {
                'isJsEnabled': 'true',
                'tryCount': '',
                'source_app': '',
                'clickedSuggestion': 'false',
                'session_key': str(self.username),
                'session_password': str(self.pwd),
                'session_redirect': '',
                'trk': 'hb_signin',
                'loginCsrfParam': loginCsrfParam,
                'fromEmail': '',
                'csrfToken': csrfToken,
                'sourceAlias': sourceAlias,
            }

            response = s.post('https://www.linkedin.com/uas/login-submit', headers=headers, data=data)
            _status = json_2_dict(response.text).get('status', 'fail')
            if _status == 'ok':
                print('[+] 登陆成功!')
                return True
            else:
                print('[-] 登陆失败!')
                return False

    async def _fck_run(self):
        login_res = await self._login()

    def __del__(self):
        collect()

def main():
    with open('/Users/afa/myFiles/pwd/linkedin_pwd.json', 'r') as f:
        linkedin_info = json_2_dict(f.read())

    _ = LinkedinSpider(username=linkedin_info['username'], pwd=linkedin_info['pwd'])
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()