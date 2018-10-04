# coding:utf-8

'''
@author = super_fazai
@File    : china_adjue_docs_spider.py
@connect : superonesfazai@gmail.com
'''

"""
裁判文书网
"""

from asyncio import get_event_loop
from gc import collect
import urllib3
# 设置不进行安全提醒
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import execjs
from pprint import pprint
from urllib.parse import quote_plus
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.ip_pools import IpPools

class ChinaAdjueDocsSpider(object):
    def __init__(self):
        self.loop = get_event_loop()

    async def _get_headers(self):
        self.headers = {
            'Origin': 'https://wenshu.court.gov.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            # 'Referer': 'https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

        return self.headers

    async def _get_cookie(self) -> dict:
        return {
            '_gscu_2116842793': '38032346hapx8711',
            '_gscbrs_2116842793': '1',
            'Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2': '1538032347,1538033641,1538036233',
            'Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2': '1538036233',
            '_gscs_2116842793': 't38036233ti43gd11|pv:1',
            'vjkl5': '452b08fde99ff271a1601a11831f77c020f8e29d',
        }

    async def _get_js_parser_res(self, js_path, func_name, **args):
        '''
        python调用js, 并返回结果
        :param js_path: js文件路径
        :param func_name: 待调用的函数名
        :param args: 该函数待传递的参数
        :return: res
        '''
        with open(js_path, 'r') as f:
            js_code = f.read()

        js_parser = execjs.compile(js_code)
        res = js_parser.call(func_name, *args)

        return res

    async def _get_vl5x(self, vjkl5):
        # 查看ListContent接口所在js源码
        # 1. vl5x 生成方式(找到)(狗血，层层加密!)
        random_vl5x = await self._get_js_parser_res(
            js_path='./js/get_vl5x.js',
            func_name='get_vl5x',
            vjkl5=vjkl5,
        )
        o_random_vl5x = await self._get_js_parser_res(
            js_path='./js/o_get_vl5x.js',
            func_name='GetVl5x',
            cookie=vjkl5,
        )
        print('得到vl5x: {}'.format(random_vl5x))
        print('得到o_vl5x: {}'.format(o_random_vl5x))

        return o_random_vl5x

    async def _get_guid(self) -> str:
        guid = await self._get_js_parser_res(
            js_path='./js/get_guid.js',
            func_name='get_guid',
            func_params=None,
        )
        print('得到guid: {}'.format(guid))

        return guid

    async def _get_number(self, proxies) -> str:
        '''
        先请求一次, 获取到下次拿数据的验证码
        :return:
        '''
        data = {
            'guid': await self._get_guid(),
        }
        url = 'https://wenshu.court.gov.cn/ValiCode/GetCode'
        # body = self.session.get_url_body(method='post', url=url, headers=self.headers, cookies=None, data=data, verify=False, proxies=proxies)
        response = self.session.post(url=url, headers=self.headers, data=data, verify=False, proxies=proxies)
        body = response.text
        print('获取到的captcha: {}'.format(body))

        return body

    async def _get_random_proxy(self) -> dict:
        _ = IpPools()
        proxies = _.get_proxy_ip_from_ip_pool()

        return proxies

    async def _fck_run(self):
        '''
        main
        :return:
        '''
        await self._get_headers()
        proxies = await self._get_random_proxy()
        self.session = requests.Session()

        # url = 'https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
        data_param = '案件类型:刑事案件'.split(':')
        url = 'https://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2++{}+{}:{}'.format(quote_plus('刑事案件'), quote_plus(data_param[0]), quote_plus(data_param[1]))
        response = self.session.get(url=url, headers=self.headers, verify=False, proxies=proxies)
        response_cookies = response.cookies.get_dict()
        # pprint(response_cookies)
        if 'vjkl5' not in response_cookies:
            raise ValueError('vjkl5没在cookies中返回!')
        else:
            vjkl5 = response_cookies.get('vjkl5')
            print('得到的vjkl5: {}'.format(vjkl5))

        random_vl5x = await self._get_vl5x(vjkl5)
        data = {
          'Param': ':'.join(data_param),
          'Index': '3',
          'Page': '10',
          'Order': '法院层级',
          'Direction': 'asc',
          'vl5x': random_vl5x,
          'number': await self._get_number(proxies=proxies),
          'guid': await self._get_guid(),
        }
        pprint(data)
        cookies = await self._get_cookie()
        cookies.update({
            'vl5x': random_vl5x
        })

        url = 'https://wenshu.court.gov.cn/List/ListContent'
        # 设置verify不校验证书
        # response = self.session.post(url=url, headers=headers, cookies=cookies, data=data, verify=False)
        # print(response.text)    # 返回 "remind key" -> 说明某个参数提交错误

        # body = self.session.get_url_body(method='post', url=url, headers=await self._get_headers(), cookies=cookies, data=data, verify=False)
        body = self.session.post(url=url, headers=await self._get_headers(), cookies=None, data=data, verify=False, proxies=proxies).text
        print(body)

        return

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = ChinaAdjueDocsSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())