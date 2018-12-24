# coding:utf-8

'''
@author = super_fazai
@File    : business_info_spider.py
@connect : superonesfazai@gmail.com
'''

"""
国家企业信用信息公示系统(www.gsxt.gov.cn)
"""

from gc import collect
from json import dumps
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class NECIPSSpider(AsyncCrawler):
    """基于wx small program"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool
        )
        self.keyword = None

    async def _get_wx_headers(self):
        return {
            'Host': 'app.gsxt.gov.cn',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
            # 'Referer': 'https://servicewechat.com/wx5b0ed3b8c0499950/6/page-frame.html',
            'Accept-Language': 'zh-cn',
        }

    async def _get_pc_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_pc_ua(),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Referer': 'http://www.jsgsj.gov.cn:58888/province/jiangsu.jsp?typeName=168B7D7C6BDA3B9C0A1DDFA30CBC7860&searchType=qyxx',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

    async def _get_eci_by_wx(self, keyword):
        '''
        获取接口信息
        :param keyword:
        :return:
        '''
        data = {
            'conditions': dumps({
                'excep_tab': '0',
                'ill_tab': '0',
                'area': '0',
                'cStatus': '0',
                'xzxk': '0',
                'xzcf': '0',
                'dydj': '0',
            }),
            'searchword': str(keyword),
            'sourceType': 'W'
        }
        url = 'https://app.gsxt.gov.cn/gsxt/corp-query-app-search-1.html'
        _ = json_2_dict(await unblock_request(method='post', url=url, headers=await self._get_wx_headers(), data=data, ip_pool_type=self.ip_pool_type))
        pprint(_)

        return _

    async def _get_pc_post_data_name(self):
        '''
        得到pc端加密的name
        :return:
        '''
        # checkCode
        url = 'http://www.jsgsj.gov.cn:58888/province/infoQueryServlet.json'
        params = (
            ('checkCode', 'true'),
        )
        data = {
            'verifyCode': '',
            'name': str(self.keyword),
        }
        headers = {
            'Referer': 'http://www.jsgsj.gov.cn:58888/province/jiangsu.jsp?typeName=&searchType=qyxx',      # 必带头, typeName请求一次
            'User-Agent': get_random_pc_ua(),
        }
        name = json_2_dict(await unblock_request(method='post', url=url, headers=headers, params=params, data=data, ip_pool_type=self.ip_pool_type)).get('bean', {}).get('name', '')
        # pprint(name)

        return name

    async def _get_eci_by_pc(self, keyword) -> list:
        '''
        调用pc接口
        :param keyword:
        :return:
        '''
        self.keyword = str(keyword)
        name = await self._get_pc_post_data_name()
        if name == '':
            print('获取到的name为空值!')
            return []

        print('获取到的name: {}'.format(name))
        params = (
            ('queryCinfo', 'true'),
        )
        data = {
            'name': name,
            'searchType': 'qyxx',
            'pageNo': '1',
            'pageSize': '10'
        }
        url = 'http://www.jsgsj.gov.cn:58888/province/infoQueryServlet.json'
        headers = await self._get_pc_headers()
        headers.update({
            'Origin': 'http://www.jsgsj.gov.cn:58888',
            'Referer': 'http://www.jsgsj.gov.cn:58888/province/jiangsu.jsp?typeName=&searchType=qyxx',  # 此处typeName也为空
        })
        data = json_2_dict(await unblock_request(method='post', url=url, headers=headers, params=params, data=data, ip_pool_type=self.ip_pool_type))
        pprint(data)

        return data

    def __call__(self, *args, **kwargs):
        keyword = kwargs.get('keyword')

        return self.loop.run_until_complete(self._get_eci_by_pc(keyword=keyword))

    def __del__(self):
        collect()

if __name__ == '__main__':
    keyword = '江苏凯邦'
    _ = NECIPSSpider()
    _(keyword=keyword)
