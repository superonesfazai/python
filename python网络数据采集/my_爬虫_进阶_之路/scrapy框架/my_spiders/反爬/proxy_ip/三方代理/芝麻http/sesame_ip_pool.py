# coding:utf-8

'''
@author = super_fazai
@File    : sesame_ip_pool.py
@connect : superonesfazai@gmail.com
'''

"""
基于芝麻http接口的异步ip pool
http://open.zhimaruanjian.com/
"""

from gc import collect
from requests import session
from random import choice
from fzutils.sql_utils import BaseRedisCli
from fzutils.data.list_utils import list_remove_repeat_dict
from fzutils.spider.async_always import *

class SesameIpPool(object):
    """芝麻http"""
    def __init__(self):
        self.ip_list = []
        self.loop = get_event_loop()
        self.redis_cli = BaseRedisCli()
        self._k = get_uuid3('sesame_ip_pool')
        self.sleep_time = 1. * 60

    async def _get_all_ip_proxy(self) -> list:
        '''
        得到redis中所有ip proxy
        :return:
        '''
        return json_2_dict(self.redis_cli.get(name=self._k) or dumps([]), default_res=[])

    async def _get_phone_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_proxies(self):
        if self.ip_list == []:
            self.ip_list = await self._get_all_ip_proxy() or []
            if self.ip_list == []:
                return {}
            else:
                pass

        one = choice(self.ip_list)
        expire_time = one.get('expire_time')
        if one.get('expire_time') is None or datetime_to_timestamp(string_to_datetime(expire_time)) < datetime_to_timestamp(get_shanghai_time()):
            return {}

        proxy = 'http://' + one.get('ip', '') + ':' + str(one.get('port', ''))

        return {
            # 'http': proxy,
            'https': proxy,
        }

    async def _request(self, url, method='get', headers=None, params=None, cookies=None, timeout=12, encoding='utf-8') -> str:
        body = ''
        proxies = await self._get_proxies()
        if proxies == {}:
            print('[-] 未使用代理!!')
        else:
            print('[+] {}'.format(proxies.get('https', '')))

        with session() as s:
            try:
                response = s.request(method=method, url=url, headers=headers, params=params, cookies=cookies, timeout=timeout, proxies=proxies)
                try:
                    body = response.content.decode(encoding)
                except:
                    body = response.text

            except Exception as e:
                print(e)

            return body

    async def _delete_expire_time_ip(self, data) -> list:
        '''
        删除过期ip
        :return:
        '''
        new = []
        for item in self.ip_list:
            expire_time = item.get('expire_time', '')
            if datetime_to_timestamp(string_to_datetime(expire_time)) > datetime_to_timestamp(get_shanghai_time()) + 2 * 60:
                # 过期时间戳 > 当前时间戳 + 2*60
                new.append(item)

        self.ip_list = new + data

        return self.ip_list

    async def _get_ip_proxy_list(self, ip_num=200) -> list:
        '''
        获取一个proxy
        :return:
        '''
        # http://webapi.http.zhimacangku.com/getip?num=200&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=
        params = (
            ('num', str(ip_num)),   # 提取ip数
            ('type', '2'),          # 数据格式：1:TXT 2:JSON 3:html
            ('pro', ''),            # 省份, 默认全国
            ('city', '0'),          # 城市, 默认全国
            ('yys', '0'),           # 0:不限 100026:联通 100017:电信
            ('port', '1'),          # IP协议 1:HTTP 2:SOCK5 11:HTTPS
            ('time', '1'),          # 稳定时长, 最小的是1, 提取数量多
            ('ts', '1'),            # 是否显示IP过期时间: 1显示 2不显示
            ('ys', '0'),            # 是否显示IP运营商: 1显示
            ('cs', '0'),            # 是否显示位置: 1显示
            ('lb', '1'),            # 分隔符(1:\r\n 2:/br 3:\r 4:\n 5:\t 6 :自定义)
            ('sb', '0'),
            ('pb', '4'),            # 端口位数（4:4位端口 5:5位端口）
            ('mr', '1'),            # 去重选择（1:360天去重 2:单日去重 3:不去重）
            ('regions', ''),        # 全国混拨地区
        )
        url = 'http://webapi.http.zhimacangku.com/getip'
        data = json_2_dict(await self._request(url=url, headers=await self._get_phone_headers(), params=params)).\
            get('data', [])
        # pprint(data)
        if data != []:
            self.ip_list = await self._delete_expire_time_ip(data=data)
            self.ip_list = list_remove_repeat_dict(target=self.ip_list, repeat_key='ip')
            self.redis_cli.set(name=self._k, value=dumps(self.ip_list))    # 先转换为json再存入

        return data

    async def _test(self) -> str:
        '''
        测试代理是否高匿
        :return:
        '''
        # 用httpbin.org检测发现还是暴露原始ip, 但是能处理其他本身自己ip池无法采集的接口
        # url = 'http://httpbin.org/get'
        # body = await self._request(url=url, headers=await self._get_phone_headers())
        # print(body)

        url = 'https://www.whatismybrowser.com/'
        body = await self._request(url=url, headers=await self._get_phone_headers())
        now_ip = Selector(text=body).css('div#ip-address:nth-child(2) .detected-column a:nth-child(1) ::text').extract_first() or ''
        print('当前真实ip: {}'.format(now_ip))

        return now_ip

    async def _add_local_ip_to_white_list(self, local_ip):
        '''
        长期爬取，需要定时将本地ip设置进白名单, 否则获取不到ip_list
        :return:
        '''
        url = 'http://web.http.cnapi.cc/index/index/save_white?neek=55393&appkey=71988e7028eb9587fac0eea29a5150fa&white={}'.format(local_ip)
        await self._request(url=url, headers=await self._get_phone_headers())

        return None

    async def _fck_run(self):
        print('芝麻http ip pool'.center(30, '@'))
        while True:
            res = await self._get_ip_proxy_list()
            # pprint(res)
            print('{} 新获取到可用ip个数: {}'.format(get_shanghai_time(), len(res)))
            print('休眠 {}s ...'.format(self.sleep_time))
            await async_sleep(self.sleep_time)

    def __del__(self):
        try:
            del self.redis_cli
        except Exception:
            pass
        collect()

if __name__ == '__main__':
    _ = SesameIpPool()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

    # 查看当前IP池ip个数
    # res = loop.run_until_complete(_._get_all_ip_proxy())
    # pprint(res)
    # print('总个数: {}'.format(len(res)))

    # print(get_uuid3('sesame_ip_pool'))  # d8f28c94-09f6-37fd-9939-64c23716d20a

