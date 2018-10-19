# coding:utf-8

'''
@author = super_fazai
@File    : si_mu_wang_spider.py
@connect : superonesfazai@gmail.com
'''

"""
私募排排网: 私募排名抓取
"""

from requests import get
from gc import collect

from fzutils.spider.async_always import *

class SiMuSpider(object):
    def __init__(self, loop=None):
        with open('/Users/afa/myFiles/pwd/simuwang_pwd.json', 'r') as f:
            _ = json_2_dict(f.read())
        self.username = str(_.get('username', ''))
        self.pwd = str(_.get('pwd', ''))
        self.cookies = None
        self.max_dc_num = 195
        self.loop = get_event_loop()

    async def _get_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }

    async def _get_login_params(self):
        t = str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))
        return (
            ('m', 'Passport'),
            ('c', 'auth'),
            ('a', 'login'),
            # ('rz_cback', 'jQuery112408582415125247611_1537946184717'),
            ('rz_cback', 'jQuery112408582415125247611_{}'.format(t)),
            ('type', 'login'),
            ('name', self.username),
            ('pass', self.pwd),
            ('reme', '0'),
            ('rn', '1'),
            ('do_qualified', '1'),
            ('_', t),
        )

    async def _login(self) -> bool:
        '''
        模拟登陆
        :return:
        '''
        headers = await self._get_headers()
        headers.update({'Referer': 'https://www.simuwang.com/user/index.html',})
        params = await self._get_login_params()
        login_url = 'https://passport.simuwang.com/index.php'
        response = get(url=login_url, headers=headers, params=params)
        try:
            data = json_2_dict(re.compile('\((.*)\)').findall(response.text)[0])
            suc = data.get('suc') or '登录失败'
            assert suc != '登陆成功!', '模拟登陆失败!'
        except (IndexError, AssertionError) as e:
            print(e)
            return False

        print('[+] 登陆成功!')
        self.cookies = response.cookies.get_dict()
        # pprint(self.cookies)

        return True

    async def _get_one_page_private_placement_funds_rank_info(self, page_num) -> list:
        '''
        得到一页私募基金的接口data
        :return:
        '''
        async def oo():
            return json_2_dict(
                json_str=Requests.get_url_body(url='https://dc.simuwang.com/ranking/get', headers=headers, params=params, cookies=self.cookies),
                default_res={}).get('data', [])

        headers = await self._get_headers()
        headers.update({'X-Requested-With': 'XMLHttpRequest',})
        params = (
            ('page', str(page_num)),
            ('condition', 'fund_type:1,6,4,3,8,2;ret:1;rating_year:1;istiered:0;company_type:1;sort_name:profit_col2;sort_asc:desc;keyword:'),
        )

        data = await oo()
        label = '+' if data != [] else '-'
        print('[{}] {}'.format(label, page_num))
        # pprint(data)
        if data == []:
            return []

        return data

    async def _fck_run(self) -> list:
        '''
        main
        :return:
        '''
        login_res = await self._login()
        if not login_res:
            return []

        tasks = []
        for page_num in range(1, self.max_dc_num):
            print('创建task:{}'.format(page_num))
            tasks.append(self.loop.create_task(self._get_one_page_private_placement_funds_rank_info(page_num=page_num)))

        print('请耐心等待所有任务完成...')
        success_jobs, fail_jobs = await wait(tasks)
        print('success_num: {}, fail_num: {}'.format(len(success_jobs), len(fail_jobs)))
        all_res = [r.result() for r in success_jobs]
        # pprint(all_res)
        print('完毕'.center(100, '*'))
        print('总长度为: {}'.format(len(all_res)))

        return all_res

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = SiMuSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

