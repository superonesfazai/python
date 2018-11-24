# coding:utf-8

'''
@author = super_fazai
@File    : region_spider.py
@connect : superonesfazai@gmail.com
'''

"""
省市区爬虫
"""

import re
from gc import collect
from pprint import pprint
from scrapy.selector import Selector
from asyncio import get_event_loop
from json import dumps
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import IP_POOL_TYPE

from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import json_2_dict

class RegionSpider(object):
    def __init__(self):
        self.ame_list = None
        self.target_data = None   # 存储最终需求数据
        self.ip_pool_type = IP_POOL_TYPE

    async def _get_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_all_ame_from_office(self) -> list:
        '''
        得到全国最新区码(http://xzqh.mca.gov.cn/map)
        :return:
        '''
        body = Requests.get_url_body(url='http://xzqh.mca.gov.cn/map', headers=await self._get_headers(), cookies=None, ip_pool_type=self.ip_pool_type)
        # print(body)
        # http://www.mca.gov.cn/article/sj/tjbz/a/2018/201803131439.html
        data = json_2_dict(
            json_str=Selector(text=body).css('table.select_table td input#pyArr ::attr("value")').extract_first(),
            default_res=[])
        print('总计邮编个数: {}'.format(len(data)))
        self.ame_list = data

        return data

    async def _handle_ame(self):
        '''
        处理数据
        :return:
        '''
        # pprint(self.ame_list)
        _ = []
        for item in self.ame_list:
            item_code = item.get('code', '')
            # 匹配省直辖市 0
            if item_code[2:] == '0000':
                o = []
                for i in self.ame_list:
                    i_code = i.get('code', '')
                    # 匹配 1
                    if item_code[:2] == i_code[:2]:
                        o.append({
                            'c_name': i.get('cName'),
                            'code': i_code,
                        })
                o = o[1:]
                _.append({
                    'c_name': item.get('cName'),
                    'code': item_code,
                    'o': o,  # 子集
                })
        # pprint(_)

        tmp = _
        for item in tmp:
            o = item.get('o')
            if o == []:
                continue

            for i in o:
                i_code = i.get('code')
                if i_code[4:] == '00':
                    w = []
                    for j in o:
                        j_code = j.get('code')
                        if i_code[:4] == j_code[:4]:
                            w.append({
                                'c_name': j.get('c_name'),
                                'code': j_code,
                            })
                    w = w[1:]
                    i.update({
                        'w': w,
                    })
        # pprint(_)

        for item in _:
            o = item.get('o')
            new_o = []
            for i in o:
                i_code = i.get('code')
                if i_code[4:] == '00' and i_code[2:] != '0000':
                    new_o.append(i)
                    item.update({
                        'o': new_o,
                    })
                else:
                    pass

        pprint(_)
        # print(dumps(_))
        self.target_data = _

        return _

    async def _get_all_ame_from_tb(self) -> list:
        '''
        得到全国最新区码等级(淘宝)
        :return:
        '''
        headers = {
            'User-Agent': get_random_pc_ua(),
        }
        body = Requests.get_url_body(url='https://division-data.alicdn.com/simple/addr_3_001.js', headers=headers, ip_pool_type=self.ip_pool_type)
        _ = json_2_dict(re.compile('var tdist=(.*);window\.goldlog&&').findall(body)[0])
        # pprint(_)
        new = []
        for key, value in _.items():
            new.append({
                'cName': value[0],
                'code': str(key)
            })
        self.ame_list = new

        return new

    async def _insert_into_table(self):
        pipeline = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = 'insert into dbo.Region(c_name, code, parent_code, parent_name) values(%s, %s, %s, %s)'
        # 存储第一级别
        print('第一级别'.center(100, '-'))
        for item in self.target_data:
            c_name = item.get('c_name')
            code = item.get('code')
            parent_code = ''
            parent_name = ''
            params = (
                c_name,
                code,
                parent_code,
                parent_name,
            )
            print(params)
            pipeline._insert_into_table(sql_str=sql_str, params=params)

        # 存储第二级别
        print('第二级别'.center(100, '-'))
        for item in self.target_data:
            item_name = item.get('c_name')
            item_code = item.get('code')
            o = item.get('o')
            for i in o:
                c_name = i.get('c_name')
                code = i.get('code')
                parent_code = item_code
                parent_name = item_name
                params = (
                    c_name,
                    code,
                    parent_code,
                    parent_name,
                )
                print(params)
                pipeline._insert_into_table(sql_str=sql_str, params=params)

        # 存储第三级别
        print('第三级别'.center(100, '-'))
        for item in self.target_data:
            o = item.get('o')
            for i in o:
                i_name = i.get('c_name')
                i_code = i.get('code')
                w = i.get('w')
                if w is not None:
                    for j in w:
                        c_name = j.get('c_name')
                        code = j.get('code')
                        parent_code = i_code
                        parent_name = i_name
                        params = (
                            c_name,
                            code,
                            parent_code,
                            parent_name,
                        )
                        print(params)
                        pipeline._insert_into_table(sql_str=sql_str, params=params)
                else:   # eg: 北京市只到第二级, 第三级无
                    pass

        print('全部写入完毕!'.center(100, '*'))

        return True

    async def _fck_fun(self) -> bool:
        all_ame_list = await self._get_all_ame_from_office()
        # all_ame_list = await self._get_all_ame_from_tb()
        if all_ame_list == []:
            print('获取到的all_ame_list为空list!')
            return False

        await self._handle_ame()
        # await self._insert_into_table()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = RegionSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_fun())