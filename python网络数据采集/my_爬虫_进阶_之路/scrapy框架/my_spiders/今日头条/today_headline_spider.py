# coding:utf-8

'''
@author = super_fazai
@File    : today_headline_spider.py
@connect : superonesfazai@gmail.com
'''

"""
今日头条m站爬虫
    # _signature
    # as
    # cp
    
    # __webpack_require__是 webpack打包后代码 可见: https://segmentfault.com/a/1190000006814420
"""

from gc import collect

from fzutils.spider.async_always import *

class TodayHeadlineSpider(object):
    def __init__(self):
        pass

    async def _get_one_api_data(self):
        '''
        获取推荐api数据
        :return:
        '''
        # TODO
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            'referer': 'https://m.toutiao.com/',
            'authority': 'm.toutiao.com',
        }
        params = (
            ('tag', '__all__'),
            ('ac', 'wap'),
            ('count', '20'),
            ('format', 'json_raw'),
            ('as', 'A1B59B7B0C715AA'),
            ('cp', '5BBCD1857A0A6E1'),
            ('max_behot_time', '1539052864'),
            ('_signature', 'LlHSKgAAdfSRJyPM71N2US5R0j'),
            ('i', '1539052864'),
        )
        url = 'https://m.toutiao.com/list/'
        body = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params))
        print(body)

    async def _fck_fun(self):
        sign = get_js_parser_res(
            js_path='./js/hook.js',
            func_name='get_sign',
        )

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = TodayHeadlineSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_fun())