# coding:utf-8

'''
@author = super_fazai
@File    : juchao_info_spider.py
@connect : superonesfazai@gmail.com
'''

"""
巨潮资讯爬虫
    http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice
"""

from gc import collect
from requests import post
from json import dumps
from fzutils.spider.async_always import *

class JuChaoInfoSpider(object):
    def __init__(self):
        self.loop = get_event_loop()
        self.json_apth = '/Users/afa/myFiles/tmp/巨潮资讯网/juchao.json'
        self.sort_dict = self._set_sort_dict()

    def _set_sort_dict(self):
        return {
            '深市': {
                'column': 'szse_latest',
            },
            '深主板': {
                'column': 'szse_main_latest',
            },
            '中小板': {
                'column': 'szse_sme_latest',
            },
            '创业板': {
                'column': 'szse_gem_latest',
            },
            '沪市': {
                'column': 'sse_latest',
            },
            '港主板': {
                'column': 'hke_main_latest',
            },
            '港创业板': {
                'column': 'hke_gem_latest',
            },
            '新三板': {
                'column': 'neeq_company_latest',
            },
            '老三板': {
                'column': 'staq_net_delisted_latest',
            },
            '基金': {
                'column': 'fund_latest',
            },
            '债券': {
                'column': 'bond_latest',
            },
            '监管': {
                'column': 'regulator_latest',
            },
            '预披露': {
                'column': 'pre_disclosure_latest',
            },
        }

    async def _get_headers(self):
        return {
            'Origin': 'http://www.cninfo.com.cn',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': get_random_phone_ua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Content-Length': '0',
        }

    async def _get_one_page_notices_data(self, column:str, page_num:int) -> list:
        '''
        获取一页公告数据
        :return:
        '''
        params = (
            ('column', column),
            ('pageNum', '3'),
            ('pageSize', '20'),
        )
        # 不能使用普通代理, 使用普通代理405
        data = json_2_dict(post('http://www.cninfo.com.cn/new/disclosure', headers=await self._get_headers(), params=params, cookies=None).text).get('classifiedAnnouncements', [])
        label = '+' if data != [] else '-'
        print('[{}] {} {}'.format(label, column, page_num))

        return data

    async def _fck_run(self):
        tasks = []
        notice_dict = {}
        for key, value in self.sort_dict.items():
            column = value.get('column')
            for page_num in range(1, 25):
                print('创建task:{} {}...'.format(key, page_num))
                one = tasks.append(self.loop.create_task(self._get_one_page_notices_data(column=column, page_num=page_num)))

            all_res_list = await async_wait_tasks_finished(tasks=tasks)
            notice_item_list = []
            # pprint(all_res_list)

            for item in all_res_list:
                if item is not None:
                    notice_item_list += item
            notice_dict.update({
                key: notice_item_list,
            })

        # pprint(notice_dict)
        print('总个数:{}'.format(len(notice_dict)))
        _json = dumps(notice_dict)
        with open(self.json_apth, 'w') as f:
            f.write(_json)

        # pdf地址: http://static.cninfo.com.cn + /xxxx

        return notice_dict

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = JuChaoInfoSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
