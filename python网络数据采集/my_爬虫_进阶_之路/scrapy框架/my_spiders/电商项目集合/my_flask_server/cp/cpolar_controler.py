# coding:utf-8

'''
@author = super_fazai
@File    : cpolar_controler.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from settings import (
    IP_POOL_TYPE,
    CPOLAR_PWD_INFO_PATH,
)

from requests import session
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import *

class CpolarControler(AsyncCrawler):
    """cpolar url 控制器"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
        )
        self.sleep_time = 3. * 60
        self.req_timeout = 15
        self.req_num_retries = 5
        self.set_user_and_pwd()

    def set_user_and_pwd(self):
        cpolar_info = ''
        with open(CPOLAR_PWD_INFO_PATH, 'r') as f:
            for line in f:
                cpolar_info += line.replace('\n', '').replace('  ', '')
        self.cpolar_info = json_2_dict(json_str=cpolar_info)
        self.username = self.cpolar_info['username']
        self.pwd = self.cpolar_info['pwd']
        print('cpolar user: {}, pwd: {}'.format(self.username, self.pwd))

    async def _fck_run(self):
        while True:
            try:
                print('now_time: {}'.format(get_shanghai_time()))
                self._s = session()
                login_res = self.login()
                assert login_res is True
                cpolar_url = self.get_cpolar_url()
                assert cpolar_url != ''
                self.set_new_cpolar_url(cpolar_url=cpolar_url)
            except Exception as e:
                print(e)

            print('休眠{}s ...\n'.format(self.sleep_time))
            sleep(self.sleep_time)

    def login(self) -> bool:
        """
        登录
        :return:
        """
        # 先获取csrf_token
        headers = get_random_headers(
            cache_control='', )
        body = self._s.request(
            method='get',
            url='https://dashboard.cpolar.com/login',
            headers=headers,
            proxies=Requests._get_proxies(
                ip_pool_type=self.ip_pool_type,
                proxy_type=PROXY_TYPE_HTTPS,),
            timeout=self.req_timeout,).text
        # print(body)
        csrf_token_sel = {
            'method': 're',
            'selector': 'name=\"csrf_token\" value=\"(.*?)\"',
        }
        csrf_token = parse_field(
            parser=csrf_token_sel,
            target_obj=body, )
        assert csrf_token != ''
        print('获取到csrf_token: {}'.format(csrf_token))

        # 再登录
        login_headers = get_random_headers(
            cache_control='', )
        login_headers.update({
            'Referer': 'https://dashboard.cpolar.com/login',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        data = {
            'login': self.username,
            'password': self.pwd,
            'csrf_token': csrf_token,
        }
        body = self._s.request(
            method='post',
            url='https://dashboard.cpolar.com/login',
            headers=headers,
            data=data,
            proxies=Requests._get_proxies(
                ip_pool_type=self.ip_pool_type,
                proxy_type=PROXY_TYPE_HTTPS),
            timeout=self.req_timeout,).text
        assert body != ''
        # print(body)

        if '<h3 class=\"first\">设置与安装</h3>' in body:
            print('login success')
            return True
        else:
            print('login fail')
            return False

    def get_cpolar_url(self) -> str:
        """
        获取新cpolar_url
        :return:
        """
        headers = get_random_headers(
            cache_control='', )
        headers.update({
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'referer': 'https://dashboard.cpolar.com/get-started',
        })
        url = 'https://dashboard.cpolar.com/status'
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,
            _session=self._s,)
        assert body != ''
        # print(body)

        cpolar_url_sel = {
            'method': 'css',
            'selector': 'th a:nth-child(1) ::text',
        }
        cpolar_url = parse_field(
            parser=cpolar_url_sel,
            target_obj=body, )
        print('cpolar_url: {}'.format(cpolar_url))

        return cpolar_url

    def set_new_cpolar_url(self, cpolar_url: str):
        """
        :param cpolar_url:
        :return:
        """
        body = self._s.request(
            method='get',
            url='http://118.31.39.97/set_local_server_url',
            params=(
                ('url', cpolar_url),
            ),).text
        print(body)

    def __del__(self):
        try:
            del self.loop
            del self.ip_pool_type
            del self._s
        except:
            pass
        collect()

if __name__ == '__main__':
    cpolar_controler = CpolarControler()
    loop = get_event_loop()
    loop.run_until_complete(cpolar_controler._fck_run())